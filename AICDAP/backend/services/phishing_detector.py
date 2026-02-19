import os
import csv
import logging
from urllib.parse import urlparse
from typing import Dict, Any
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from utils.feature_extractor import url_features

logger = logging.getLogger(__name__)


class PhishingDetector:
    """Service for detecting phishing URLs using ML model"""

    def __init__(self):
        self.model = None

        base_dir = os.path.dirname(__file__)

        # dataset path only (NO MODEL FILE)
        self.dataset_path = os.path.join(base_dir, "..", "data", "URL dataset.csv")
        self.logfile = os.path.join(base_dir, "..", "fp_log.csv")

        self.threshold = 0.7

        # Whitelist of trusted domains
        self.whitelist = {
            "facebook.com","google.com","github.com","microsoft.com","linkedin.com",
            "amazon.com","apple.com","instagram.com","twitter.com","whatsapp.com",
            "paypal.com","yahoo.com","zoom.us","cloudflare.com","stackoverflow.com",
        }

    # =====================================================
    # INITIALIZE → ALWAYS TRAIN
    # =====================================================
    async def initialize(self):
        """Always train model from dataset"""
        try:
            logger.info("Training phishing detection model from dataset...")
            self._train_model()
            logger.info("Model training complete")
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise

    # =====================================================
    # TRAIN MODEL
    # =====================================================
    def _train_model(self):

        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")

        df = pd.read_csv(self.dataset_path)

        if "url" not in df.columns or "type" not in df.columns:
            raise ValueError("Dataset must contain columns: url, type")

        # convert labels
        df["label"] = df["type"].map({"legitimate": 0, "phishing": 1})
        df = df.dropna(subset=["url", "label"])

        logger.info(f"Dataset loaded: {len(df)} samples")

        # extract features
        X = df["url"].apply(lambda u: url_features(u)).tolist()
        y = df["label"]

        # split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )

        # train model
        self.model = RandomForestClassifier(n_estimators=200, random_state=42)
        self.model.fit(X_train, y_train)

        # evaluate
        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        logger.info(f"Training Accuracy: {acc:.4f}")

    # =====================================================
    # DOMAIN NORMALIZATION
    # =====================================================
    def get_registered_domain(self, netloc: str) -> str:
        host = netloc.split(":")[0].lower()
        if host.startswith("www."):
            host = host[4:]
        return host

    # =====================================================
    # LOG CASES
    # =====================================================
    def log_case(self, url: str, features: list, pred: int, prob: float):
        try:
            write_header = not os.path.exists(self.logfile)
            with open(self.logfile, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if write_header:
                    writer.writerow(["url", "pred", "prob"] + [f"f{i}" for i in range(len(features))])
                writer.writerow([url, pred, prob] + list(features))
        except Exception as e:
            logger.warning(f"Failed to log case: {e}")

    # =====================================================
    # ANALYZE URL
    # =====================================================
    async def analyze_url(self, url: str) -> Dict[str, Any]:

        if not self.model:
            raise RuntimeError("Model not initialized")

        parsed = urlparse(url)
        if not parsed.netloc:
            raise ValueError("Invalid URL provided")

        reg_dom = self.get_registered_domain(parsed.netloc)

        # whitelist check
        if reg_dom in self.whitelist:
            return {
                "url": url,
                "is_phishing": False,
                "confidence_score": 0.0,
                "risk_level": "low",
                "reason": "Domain is in trusted whitelist",
                "details": {
                    "domain": reg_dom,
                    "whitelisted": True,
                    "raw_prediction": 0,
                    "threshold": self.threshold,
                },
            }

        # extract features
        features = url_features(url)

        prob = float(self.model.predict_proba([features])[0][1])
        pred_raw = int(self.model.predict([features])[0])
        pred = 1 if prob >= self.threshold else 0

        # log borderline
        if pred == 1 and prob < 0.9:
            self.log_case(url, features, pred, prob)

        risk_level = self._get_risk_level(prob)
        reason = self._generate_explanation(prob, pred_raw, reg_dom)

        return {
            "url": url,
            "is_phishing": bool(pred),
            "confidence_score": round(prob, 4),
            "risk_level": risk_level,
            "reason": reason,
            "details": {
                "domain": reg_dom,
                "whitelisted": False,
                "raw_prediction": pred_raw,
                "threshold": self.threshold,
                "features_extracted": len(features),
            },
        }

    # =====================================================
    # RISK LEVEL
    # =====================================================
    def _get_risk_level(self, probability: float) -> str:
        if probability >= 0.8:
            return "high"
        elif probability >= 0.5:
            return "medium"
        elif probability >= 0.3:
            return "low-medium"
        else:
            return "low"

    # =====================================================
    # EXPLANATION
    # =====================================================
    def _generate_explanation(self, probability: float, prediction: int, domain: str) -> str:
        if prediction == 1:
            if probability >= 0.9:
                return "High confidence phishing detection - URL shows strong malicious patterns"
            elif probability >= 0.7:
                return "Likely phishing URL - suspicious characteristics detected"
            else:
                return "Potentially suspicious URL - proceed with caution"
        else:
            if probability <= 0.2:
                return "URL appears safe - no significant threat indicators found"
            else:
                return "URL appears legitimate but shows some minor suspicious characteristics"

    # =====================================================
    # HEALTH CHECK
    # =====================================================
    async def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy" if self.model else "unhealthy",
            "model_loaded": self.model is not None,
            "dataset_exists": os.path.exists(self.dataset_path),
            "whitelist_domains": len(self.whitelist),
            "threshold": self.threshold,
        }
    