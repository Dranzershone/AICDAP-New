import logging
import os
import tempfile
from typing import Optional, Tuple

import cv2
import numpy as np
import pytesseract
from PIL import Image

# Configure logging
logger = logging.getLogger(__name__)


class OCRTextExtractor:
    def __init__(self):
        """Initialize OCR text extractor."""
        # Try to configure tesseract path for different operating systems
        self._configure_tesseract()

    def _configure_tesseract(self):
        """Configure tesseract executable path."""
        # Common tesseract paths for different systems
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",  # Windows
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",  # Windows 32-bit
            "/usr/bin/tesseract",  # Linux
            "/usr/local/bin/tesseract",  # macOS with Homebrew
            "/opt/homebrew/bin/tesseract",  # macOS Apple Silicon
        ]

        # Try to find tesseract executable
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.info(f"Tesseract configured at: {path}")
                return

        # Check if tesseract is in PATH
        try:
            import subprocess

            subprocess.run(["tesseract", "--version"], capture_output=True, check=True)
            logger.info("Tesseract found in PATH")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Tesseract not found. OCR functionality may not work.")
            logger.warning("Please install Tesseract OCR:")
            logger.warning(
                "- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
            )
            logger.warning("- macOS: brew install tesseract")
            logger.warning("- Ubuntu/Debian: sudo apt-get install tesseract-ocr")

    def preprocess_image(self, image_path: str) -> Tuple[np.ndarray, str]:
        """
        Preprocess image for better OCR accuracy.

        Args:
            image_path: Path to the input image

        Returns:
            Tuple of processed image and preprocessing method used
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply multiple preprocessing techniques and choose the best one
            preprocessing_methods = [
                ("original", gray),
                ("binary_threshold", self._apply_binary_threshold(gray)),
                ("adaptive_threshold", self._apply_adaptive_threshold(gray)),
                ("gaussian_blur", self._apply_gaussian_blur(gray)),
                ("morphology", self._apply_morphology(gray)),
                ("noise_removal", self._remove_noise(gray)),
            ]

            # For now, use adaptive threshold as it generally works well
            processed_image, method = preprocessing_methods[2]

            return processed_image, method

        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            # Return original image if preprocessing fails
            try:
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                return image, "fallback"
            except:
                raise ValueError(f"Failed to process image: {e}")

    def _apply_binary_threshold(self, image: np.ndarray) -> np.ndarray:
        """Apply binary thresholding."""
        _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
        return binary

    def _apply_adaptive_threshold(self, image: np.ndarray) -> np.ndarray:
        """Apply adaptive thresholding."""
        adaptive = cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return adaptive

    def _apply_gaussian_blur(self, image: np.ndarray) -> np.ndarray:
        """Apply Gaussian blur and threshold."""
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def _apply_morphology(self, image: np.ndarray) -> np.ndarray:
        """Apply morphological operations."""
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPENING, kernel)
        return opening

    def _remove_noise(self, image: np.ndarray) -> np.ndarray:
        """Remove noise using median blur."""
        denoised = cv2.medianBlur(image, 3)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary

    def extract_text_from_file(self, file_path: str) -> dict:
        """
        Extract text from an image file.

        Args:
            file_path: Path to the image file

        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "text": "",
                    "confidence": 0,
                }

            # Check if file is an image
            valid_extensions = {
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".bmp",
                ".tiff",
                ".webp",
            }
            file_ext = os.path.splitext(file_path.lower())[1]
            if file_ext not in valid_extensions:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_ext}",
                    "text": "",
                    "confidence": 0,
                }

            # Preprocess image
            processed_image, preprocessing_method = self.preprocess_image(file_path)

            # Extract text using Tesseract
            text = pytesseract.image_to_string(processed_image, lang="eng")

            # Get confidence scores
            try:
                data = pytesseract.image_to_data(
                    processed_image, output_type=pytesseract.Output.DICT
                )
                confidences = [int(conf) for conf in data["conf"] if int(conf) > 0]
                avg_confidence = np.mean(confidences) if confidences else 0
            except:
                avg_confidence = 50  # Default confidence

            # Clean extracted text
            cleaned_text = self._clean_extracted_text(text)

            return {
                "success": True,
                "text": cleaned_text,
                "raw_text": text,
                "confidence": round(avg_confidence, 2),
                "preprocessing_method": preprocessing_method,
                "character_count": len(cleaned_text),
                "word_count": len(cleaned_text.split()) if cleaned_text else 0,
                "error": None,
            }

        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return {"success": False, "error": str(e), "text": "", "confidence": 0}

    def extract_text_from_bytes(
        self, image_bytes: bytes, filename: str = "image"
    ) -> dict:
        """
        Extract text from image bytes.

        Args:
            image_bytes: Image data as bytes
            filename: Original filename for validation

        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=os.path.splitext(filename)[1]
            ) as tmp_file:
                tmp_file.write(image_bytes)
                tmp_path = tmp_file.name

            try:
                # Extract text from temporary file
                result = self.extract_text_from_file(tmp_path)
                result["original_filename"] = filename
                return result
            finally:
                # Clean up temporary file
                try:
                    os.unlink(tmp_path)
                except:
                    pass

        except Exception as e:
            logger.error(f"OCR extraction from bytes failed: {e}")
            return {"success": False, "error": str(e), "text": "", "confidence": 0}

    def _clean_extracted_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""

        # Remove excessive whitespace
        cleaned = " ".join(text.split())

        # Remove obviously wrong characters that OCR sometimes produces
        # Keep only printable ASCII and common unicode characters
        cleaned = "".join(
            char for char in cleaned if ord(char) < 127 or char.isprintable()
        )

        return cleaned.strip()

    def is_tesseract_available(self) -> bool:
        """Check if Tesseract is available and working."""
        try:
            # Create a simple test image
            test_image = np.ones((100, 300), dtype=np.uint8) * 255
            cv2.putText(test_image, "TEST", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)

            # Try to extract text
            text = pytesseract.image_to_string(test_image)
            return "TEST" in text.upper()

        except Exception as e:
            logger.warning(f"Tesseract availability check failed: {e}")
            return False

    def get_supported_languages(self) -> list:
        """Get list of supported languages for OCR."""
        try:
            langs = pytesseract.get_languages()
            return langs
        except:
            return ["eng"]  # Default to English

    def health_check(self) -> dict:
        """Perform health check for OCR functionality."""
        return {
            "tesseract_available": self.is_tesseract_available(),
            "supported_languages": self.get_supported_languages(),
            "tesseract_version": self._get_tesseract_version(),
            "opencv_available": self._check_opencv(),
            "pil_available": self._check_pil(),
        }

    def _get_tesseract_version(self) -> str:
        """Get Tesseract version."""
        try:
            version = pytesseract.get_tesseract_version()
            return str(version)
        except:
            return "unknown"

    def _check_opencv(self) -> bool:
        """Check if OpenCV is working."""
        try:
            test_array = np.zeros((10, 10), dtype=np.uint8)
            cv2.threshold(test_array, 127, 255, cv2.THRESH_BINARY)
            return True
        except:
            return False

    def _check_pil(self) -> bool:
        """Check if PIL is working."""
        try:
            test_image = Image.new("RGB", (10, 10))
            return True
        except:
            return False


# Global OCR extractor instance
ocr_extractor = OCRTextExtractor()


def extract_text_from_image(image_path: str) -> dict:
    """
    Extract text from an image file.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary with extracted text and metadata
    """
    return ocr_extractor.extract_text_from_file(image_path)


def extract_text_from_image_bytes(image_bytes: bytes, filename: str = "image") -> dict:
    """
    Extract text from image bytes.

    Args:
        image_bytes: Image data as bytes
        filename: Original filename

    Returns:
        Dictionary with extracted text and metadata
    """
    return ocr_extractor.extract_text_from_bytes(image_bytes, filename)


def get_ocr_health() -> dict:
    """Get OCR system health status."""
    return ocr_extractor.health_check()
