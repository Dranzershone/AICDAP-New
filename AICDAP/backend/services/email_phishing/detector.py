import asyncio
import logging
import os
import re
from typing import Dict, List, Optional, Tuple

import joblib
import nltk
import numpy as np
import pandas as pd
import tldextract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

from nltk.corpus import stopwords


class EmailPhishingDetector:
    def __init__(self, model_dir: str = None):
        self.model_dir = model_dir or os.path.dirname(os.path.abspath(__file__))
        self.model = None
        self.vectorizer = None
        self.model_path = os.path.join(self.model_dir, "phishing_model.pkl")
        self.vectorizer_path = os.path.join(self.model_dir, "vectorizer.pkl")

        # UPDATED → dataset path
        self.dataset_path = os.path.join(self.model_dir, "phishing_email.csv")

        # Psychological trigger patterns
        self.psychological_triggers = {
            "urgency": [
                "urgent","immediately","within","expire","expires","expiring","deadline",
                "time sensitive","act now","hurry","limited time","don't delay","right now","asap",
            ],
            "fear": [
                "suspended","blocked","compromised","hacked","virus","malware",
                "security breach","unauthorized","locked","frozen","terminated",
                "cancelled","deactivated","threat","danger","risk","fraud",
            ],
            "authority": [
                "bank","security team","it department","administrator","manager",
                "support team","customer service","official","government","irs",
                "fbi","police","court","legal","law enforcement",
            ],
            "reward": [
                "won","prize","bonus","reward","gift","free","congratulations",
                "winner","lottery","jackpot","promotion","discount","offer",
                "deal","money","cash","refund",
            ],
            "trust": [
                "verify","confirm","update","secure","protect","safety",
                "trusted","certified","guaranteed","authentic","legitimate",
            ],
        }

        self.suspicious_patterns = [
            "securelogin","verifyaccount","updateinfo","bankverify","paypalverify",
            "amazonverify","googleverify","microsoftverify","appleaccount",
            "securityalert","accountsecurity","urgentupdate","accountupdate",
        ]

    async def initialize(self):
        logger.info("Initializing Email Phishing Detector...")

        if self._load_model():
            logger.info("Loaded existing phishing detection model")
        else:
            logger.info("Training new phishing detection model...")
            await self._train_model()

        return True

    def _load_model(self) -> bool:
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                return True
        except Exception as e:
            logger.warning(f"Failed to load existing model: {e}")
        return False

    def _save_model(self):
        try:
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)
            logger.info("Model and vectorizer saved successfully")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")

    async def _train_model(self):
        try:
            # UPDATED → load phishing_email.csv
            if os.path.exists(self.dataset_path):
                data = pd.read_csv(self.dataset_path)
            else:
                logger.warning("phishing_email.csv not found, using default dataset")
                data = self._create_default_dataset()

            data["text"] = data["text"].apply(self._clean_text)

            X_train, X_test, y_train, y_test = train_test_split(
                data["text"], data["label"], test_size=0.2, random_state=42
            )

            self.vectorizer = TfidfVectorizer(
                stop_words=stopwords.words("english"),
                max_features=5000,
                ngram_range=(1, 2),
                lowercase=True,
            )

            X_train_vec = self.vectorizer.fit_transform(X_train)
            X_test_vec = self.vectorizer.transform(X_test)

            self.model = LogisticRegression(
                random_state=42, max_iter=1000, class_weight="balanced"
            )
            self.model.fit(X_train_vec, y_train)

            y_pred = self.model.predict(X_test_vec)
            accuracy = accuracy_score(y_test, y_pred)
            logger.info(f"Content Model Accuracy: {accuracy:.2f}")

            self._save_model()

        except Exception as e:
            logger.error(f"Model training failed: {e}")
            self._create_fallback_model()

    def _create_fallback_model(self):
        logger.info("Creating fallback model...")
        self.vectorizer = TfidfVectorizer(stop_words=stopwords.words("english"))
        self.model = LogisticRegression()

        texts = [
            "urgent verify your account",
            "click here to update information",
            "your account has been suspended",
            "normal business email content",
            "meeting scheduled for tomorrow",
            "your order has been shipped",
        ]
        labels = [1, 1, 1, 0, 0, 0]

        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def _create_default_dataset(self) -> pd.DataFrame:
        data = {
            "text": [
                "Dear Customer, Your account has been suspended due to suspicious activity",
                "Hi there! Thanks for your order. Your package will be delivered tomorrow",
                "URGENT: Your PayPal account will be closed in 24 hours",
                "Meeting scheduled for tomorrow at 3 PM in Conference Room B",
                "Congratulations! You have won $1,000,000 in our lottery",
                "Your subscription to Netflix will expire tomorrow",
            ],
            "label": [1, 0, 1, 0, 1, 0],
        }
        return pd.DataFrame(data)

    def _clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"http\S+|www\.\S+", "[URL]", text)
        text = re.sub(r"[^a-z\s\.\!\?\,]", "", text)
        return text.strip()

    def _calculate_content_risk(self, email_text: str) -> float:
        if not self.model or not self.vectorizer:
            return 0.5
        try:
            cleaned_text = self._clean_text(email_text)
            vectorized = self.vectorizer.transform([cleaned_text])
            probability = self.model.predict_proba(vectorized)[0][1]
            return float(probability)
        except Exception as e:
            logger.warning(f"Content risk calculation failed: {e}")
            return 0.5

    def _calculate_url_risk(self, email_text: str) -> float:
        urls = re.findall(r"https?://\S+|www\.\S+", email_text)
        if not urls:
            return 0.0

        risk_score = 0.0
        total_urls = len(urls)

        for url in urls:
            url_risk = 0.0

            if re.search(r"\d+\.\d+\.\d+\.\d+", url):
                url_risk += 0.4

            if "@" in url or "-" in url.count("-") > 3:
                url_risk += 0.2

            if any(short in url for short in ["bit.ly", "tinyurl", "t.co", "goo.gl"]):
                url_risk += 0.3

            try:
                extracted = tldextract.extract(url)
                domain = extracted.domain.lower()

                for pattern in self.suspicious_patterns:
                    if pattern in domain:
                        url_risk += 0.3
                        break

                if any(char in domain for char in ["0", "1", "rn", "cl"]):
                    url_risk += 0.1

            except Exception:
                url_risk += 0.2

            risk_score += min(url_risk, 1.0)

        return min(risk_score / total_urls, 1.0)

    def _calculate_sender_risk(self, sender_history_count: int = 0) -> float:
        if sender_history_count == 0:
            return 0.6
        elif sender_history_count < 5:
            return 0.3
        elif sender_history_count < 20:
            return 0.1
        else:
            return 0.05

    def _calculate_psychology_risk(self, email_text: str) -> Tuple[float, List[str]]:
        email_lower = email_text.lower()
        score = 0.0
        detected_triggers = []

        for category, triggers in self.psychological_triggers.items():
            category_detected = False
            for trigger in triggers:
                if trigger in email_lower:
                    if not category_detected:
                        score += 0.2
                        detected_triggers.append(category)
                        category_detected = True
                    break

        if email_text.count("!") > 2:
            score += 0.1
            detected_triggers.append("excessive_emphasis")

        caps_words = re.findall(r"\b[A-Z]{3,}\b", email_text)
        if len(caps_words) > 2:
            score += 0.1
            detected_triggers.append("shouting")

        if re.search(r"\$[\d,]+|\d+\s*(?:dollars?|USD|€|£)", email_text, re.IGNORECASE):
            score += 0.1
            detected_triggers.append("financial_lure")

        return min(score, 1.0), list(set(detected_triggers))

    def _calculate_technical_indicators(
        self, email_text: str
    ) -> Tuple[float, List[str]]:
        score = 0.0
        indicators = []

        suspicious_extensions = [".exe", ".scr", ".bat", ".com", ".pif", ".zip", ".rar"]
        for ext in suspicious_extensions:
            if ext in email_text.lower():
                score += 0.2
                indicators.append(f"suspicious_attachment_{ext}")

        sensitive_requests = [
            "password","ssn","social security","credit card","bank account",
            "pin number","security code","personal information",
        ]
        for request in sensitive_requests:
            if request in email_text.lower():
                score += 0.15
                indicators.append("sensitive_info_request")
                break

        if re.search(r"xn--", email_text):
            score += 0.3
            indicators.append("punycode_attack")

        if re.search(r"[A-Za-z0-9+/]{20,}=?", email_text):
            score += 0.1
            indicators.append("encoded_content")

        return min(score, 1.0), indicators

    async def analyze_email(
        self, email_text: str, sender_history_count: int = 0, sender_email: str = None
    ) -> Dict:
        if not email_text.strip():
            return {"error": "Email text is empty", "risk_score": 0.0, "classification": "UNKNOWN"}

        try:
            content_score = self._calculate_content_risk(email_text)
            url_score = self._calculate_url_risk(email_text)
            sender_score = self._calculate_sender_risk(sender_history_count)
            psych_score, psych_reasons = self._calculate_psychology_risk(email_text)
            tech_score, tech_indicators = self._calculate_technical_indicators(email_text)

            final_score = (
                0.30 * content_score
                + 0.25 * url_score
                + 0.20 * sender_score
                + 0.15 * psych_score
                + 0.10 * tech_score
            )

            if final_score < 0.3:
                classification = "SAFE"
                risk_level = "low"
            elif final_score < 0.6:
                classification = "SUSPICIOUS"
                risk_level = "medium"
            else:
                classification = "HIGH-RISK PHISHING"
                risk_level = "high"

            urls_found = re.findall(r"https?://\S+|www\.\S+", email_text)

            return {
                "success": True,
                "risk_score": round(final_score, 3),
                "classification": classification,
                "risk_level": risk_level,
                "components": {
                    "content_risk": round(content_score, 3),
                    "url_risk": round(url_score, 3),
                    "sender_risk": round(sender_score, 3),
                    "psychological_risk": round(psych_score, 3),
                    "technical_risk": round(tech_score, 3),
                },
                "indicators": {
                    "psychological_triggers": psych_reasons,
                    "technical_indicators": tech_indicators,
                    "urls_found": urls_found,
                    "url_count": len(urls_found),
                },
                "details": {
                    "total_characters": len(email_text),
                    "word_count": len(email_text.split()),
                    "sender_history": sender_history_count,
                    "sender_email": sender_email,
                },
            }

        except Exception as e:
            logger.error(f"Email analysis failed: {e}")
            return {"error": f"Analysis failed: {str(e)}","risk_score": 0.5,"classification": "ERROR"}

    async def health_check(self) -> Dict:
        return {
            "status": "healthy" if self.model and self.vectorizer else "unhealthy",
            "model_loaded": self.model is not None,
            "vectorizer_loaded": self.vectorizer is not None,
            "model_path_exists": os.path.exists(self.model_path),
            "vectorizer_path_exists": os.path.exists(self.vectorizer_path),
            "dataset_exists": os.path.exists(self.dataset_path),
        }


detector = EmailPhishingDetector()


async def initialize_email_detector():
    return await detector.initialize()


async def analyze_email_content(email_text: str, sender_history: int = 0, sender_email: str = None):
    return await detector.analyze_email(email_text, sender_history, sender_email)


async def get_detector_health():
    return await detector.health_check()