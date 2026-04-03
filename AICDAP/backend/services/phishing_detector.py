import os
import csv
import logging
from urllib.parse import urlparse
from typing import Dict, Any

import pandas as pd
import joblib

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from utils.feature_extractor import url_features

logger = logging.getLogger(__name__)


class PhishingDetector:
    """Phishing URL detection service using CatBoost"""

    def __init__(self):

        self.model = None

        base_dir = os.path.dirname(__file__)

        self.dataset_path = os.path.abspath(
            os.path.join(base_dir, "..", "data", "URL dataset.csv")
        )

        self.model_path = os.path.abspath(
            os.path.join(base_dir, "..", "models", "phishing_model.pkl")
        )

        self.logfile = os.path.join(base_dir, "..", "fp_log.csv")

        self.threshold = 0.7

        self.whitelist = {
            "facebook.com", "google.com", "github.com", "microsoft.com",
            "linkedin.com", "amazon.com", "apple.com", "instagram.com",
            "twitter.com", "whatsapp.com", "paypal.com", "yahoo.com",
            "zoom.us", "cloudflare.com", "stackoverflow.com",
        }

    # =====================================================
    # INITIALIZE
    # =====================================================

    async def initialize(self):

        try:
            logger.info("Initializing phishing detector...")

            # Load model if already trained
            if os.path.exists(self.model_path):
                logger.info("Loading existing phishing model...")
                self.model = joblib.load(self.model_path)
                return

            logger.info("No trained model found → training new model")

            if not os.path.exists(self.dataset_path):
                raise FileNotFoundError(
                    f"Dataset not found at {self.dataset_path}"
                )

            self._train_model()

            logger.info("Phishing detection model ready")

        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise

    # =====================================================
    # TRAIN MODEL
    # =====================================================

    def _train_model(self):

        logger.info("Loading dataset...")
        df = pd.read_csv(self.dataset_path)

        if "url" not in df.columns or "type" not in df.columns:
            raise ValueError("Dataset must contain columns: url, type")

        df["label"] = df["type"].map({
            "legitimate": 0,
            "phishing": 1
        })

        df = df.dropna(subset=["url", "label"])

        logger.info(f"Dataset size: {len(df)} samples")

        # Extract features
        logger.info("Extracting features...")
        X = df["url"].apply(url_features).tolist()
        y = df["label"]

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            stratify=y,
            random_state=42
        )

        # CatBoost model
        logger.info("Training CatBoost model...")

        self.model = CatBoostClassifier(
            iterations=300,
            depth=6,
            learning_rate=0.1,
            loss_function="Logloss",
            verbose=False,
            random_seed=42
        )

        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_test)

        acc = accuracy_score(y_test, preds)
        cm = confusion_matrix(y_test, preds)
        report = classification_report(
            y_test,
            preds,
            target_names=["Legitimate", "Phishing"]
        )

        cv_scores = cross_val_score(self.model, X, y, cv=5)

        logger.info(f"\nAccuracy: {acc:.4f}")
        logger.info("\nConfusion Matrix:\n" + str(cm))
        logger.info("\nClassification Report:\n" + report)
        logger.info(f"\nCV Accuracy: {cv_scores.mean():.4f}")

        # Save trained model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

        joblib.dump(self.model, self.model_path)

        logger.info(f"Model saved → {self.model_path}")

    # =====================================================
    # DOMAIN CLEANING
    # =====================================================

    def get_registered_domain(self, netloc: str) -> str:

        host = netloc.split(":")[0].lower()

        if host.startswith("www."):
            host = host[4:]

        return host

    # =====================================================
    # LOG BORDERLINE CASES
    # =====================================================

    def log_case(self, url: str, features: list, pred: int, prob: float):

        try:
            write_header = not os.path.exists(self.logfile)

            with open(self.logfile, "a", newline="", encoding="utf-8") as f:

                writer = csv.writer(f)

                if write_header:
                    writer.writerow(
                        ["url", "pred", "prob"] +
                        [f"f{i}" for i in range(len(features))]
                    )

                writer.writerow([url, pred, prob] + list(features))

        except Exception as e:
            logger.warning(f"Failed to log case: {e}")

    # =====================================================
    # URL ANALYSIS
    # =====================================================

    async def analyze_url(self, url: str) -> Dict[str, Any]:

        if not self.model:
            raise RuntimeError("Model not initialized")

        parsed = urlparse(url)

        if not parsed.netloc:
            raise ValueError("Invalid URL provided")

        reg_dom = self.get_registered_domain(parsed.netloc)

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
                    "threshold": self.threshold
                },
            }

        features = url_features(url)

        prob = float(self.model.predict_proba([features])[0][1])

        pred_raw = int(self.model.predict([features])[0])

        pred = 1 if prob >= self.threshold else 0

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
                "threshold": self.threshold
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

        return "low"

    # =====================================================
    # EXPLANATION
    # =====================================================

    def _generate_explanation(self, probability: float, prediction: int, domain: str) -> str:

        if prediction == 1:

            if probability >= 0.9:
                return "High confidence phishing detection"

            elif probability >= 0.7:
                return "Likely phishing URL"

            return "Potentially suspicious URL"

        else:

            if probability <= 0.2:
                return "URL appears safe"

            return "URL appears mostly legitimate"

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    async def health_check(self) -> Dict[str, Any]:

        return {
            "status": "healthy" if self.model else "unhealthy",
            "model_loaded": self.model is not None,
            "dataset_exists": os.path.exists(self.dataset_path),
            "threshold": self.threshold,
        }