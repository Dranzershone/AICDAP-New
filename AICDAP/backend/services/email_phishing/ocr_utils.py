import logging
import os
import tempfile
from typing import Optional, Tuple

import cv2
import numpy as np
from PIL import Image

# Try importing pytesseract safely
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except Exception as e:
    pytesseract = None
    TESSERACT_AVAILABLE = False

# Configure logging
logger = logging.getLogger(__name__)


class OCRTextExtractor:
    def __init__(self):
        """Initialize OCR text extractor safely."""
        self.tesseract_enabled = False

        if TESSERACT_AVAILABLE:
            try:
                self._configure_tesseract()
                self.tesseract_enabled = True
            except Exception as e:
                logger.warning(f"OCR setup failed: {e}")
                self.tesseract_enabled = False
        else:
            logger.warning("pytesseract not installed. OCR disabled.")

    def _configure_tesseract(self):
        """Configure Tesseract safely."""
        try:
            env_path = os.getenv("TESSERACT_PATH")
            if env_path and os.path.exists(env_path):
                pytesseract.pytesseract.tesseract_cmd = env_path
                logger.info(f"Tesseract configured from ENV: {env_path}")
                return

            linux_path = "/usr/bin/tesseract"
            if os.path.exists(linux_path):
                pytesseract.pytesseract.tesseract_cmd = linux_path
                logger.info(f"Tesseract configured at: {linux_path}")
                return

            windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(windows_path):
                pytesseract.pytesseract.tesseract_cmd = windows_path
                logger.info(f"Tesseract configured at: {windows_path}")
                return

            logger.warning("Tesseract not found. OCR will be disabled.")

        except Exception as e:
            logger.warning(f"Tesseract configuration failed: {e}")

    def preprocess_image(self, image_path: str) -> Tuple[np.ndarray, str]:
        """Preprocess image for OCR."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            preprocessing_methods = [
                ("original", gray),
                ("binary_threshold", self._apply_binary_threshold(gray)),
                ("adaptive_threshold", self._apply_adaptive_threshold(gray)),
                ("gaussian_blur", self._apply_gaussian_blur(gray)),
                ("morphology", self._apply_morphology(gray)),
                ("noise_removal", self._remove_noise(gray)),
            ]

            processed_image, method = preprocessing_methods[2]
            return processed_image, method

        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            return image, "fallback"

    def _apply_binary_threshold(self, image):
        _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
        return binary

    def _apply_adaptive_threshold(self, image):
        return cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

    def _apply_gaussian_blur(self, image):
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def _apply_morphology(self, image):
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)
        return cv2.morphologyEx(binary, cv2.MORPH_OPENING, kernel)

    def _remove_noise(self, image):
        denoised = cv2.medianBlur(image, 3)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def extract_text_from_file(self, file_path: str) -> dict:
        """Extract text from image safely."""
        if not self.tesseract_enabled:
            return {
                "success": False,
                "error": "OCR not available in this environment",
                "text": "",
                "confidence": 0,
            }

        try:
            if not os.path.exists(file_path):
                return {"success": False, "error": "File not found", "text": ""}

            processed_image, method = self.preprocess_image(file_path)

            text = pytesseract.image_to_string(processed_image)

            return {
                "success": True,
                "text": text.strip(),
                "confidence": 80,
                "preprocessing_method": method,
            }

        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return {"success": False, "error": str(e), "text": ""}

    def extract_text_from_bytes(self, image_bytes: bytes, filename="image"):
        """Handle OCR from bytes."""
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(image_bytes)
                path = tmp.name

            result = self.extract_text_from_file(path)
            os.unlink(path)
            return result

        except Exception as e:
            return {"success": False, "error": str(e), "text": ""}


# Global instance
ocr_extractor = OCRTextExtractor()


def extract_text_from_image(image_path: str):
    return ocr_extractor.extract_text_from_file(image_path)


def extract_text_from_image_bytes(image_bytes: bytes, filename="image"):
    return ocr_extractor.extract_text_from_bytes(image_bytes, filename)


def get_ocr_health():
    return {
        "tesseract_enabled": ocr_extractor.tesseract_enabled
    }