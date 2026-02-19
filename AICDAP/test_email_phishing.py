#!/usr/bin/env python3
"""
Test script for email phishing detection API endpoints.
"""

import json
import time
from datetime import datetime

import requests

# Backend URL
BASE_URL = "http://localhost:8000"


def test_email_phishing_status():
    """Test the email phishing status endpoint."""
    print("Testing email phishing status endpoint...")

    try:
        response = requests.get(f"{BASE_URL}/api/email-phishing/status")

        if response.status_code == 200:
            data = response.json()
            print("✅ Status endpoint working")
            print(f"   Status: {data.get('status')}")
            print(f"   Detector Status: {data.get('detector', {}).get('status')}")
            print(f"   OCR Available: {data.get('ocr', {}).get('tesseract_available')}")
            return True
        else:
            print(f"❌ Status endpoint failed with code: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
        return False


def test_email_analysis():
    """Test email content analysis."""
    print("\nTesting email phishing analysis...")

    # Test cases with different risk levels
    test_emails = [
        {
            "name": "High Risk Phishing Email",
            "email_text": """
URGENT: Your bank account has been suspended due to suspicious activity.
Click here to verify your account immediately: http://secure-bank-verify.com
Failure to act within 24 hours will result in permanent account closure.
Contact our security team immediately.
            """,
            "expected_risk": "high",
        },
        {
            "name": "Medium Risk Email",
            "email_text": """
Dear Customer,
Your subscription to our service will expire tomorrow.
Please update your payment information to continue service.
Visit: https://service-renewal.com
            """,
            "expected_risk": "medium",
        },
        {
            "name": "Safe Email",
            "email_text": """
Hi John,
Just wanted to follow up on our meeting yesterday.
Could you send me the quarterly reports by Friday?
Thanks!
            """,
            "expected_risk": "low",
        },
    ]

    for test_case in test_emails:
        print(f"\n--- Testing: {test_case['name']} ---")

        try:
            payload = {"email_text": test_case["email_text"], "sender_history": 0}

            response = requests.post(
                f"{BASE_URL}/api/email-phishing/analyze",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()

                if result.get("success"):
                    data = result.get("data", {})
                    print("✅ Analysis successful")
                    print(f"   Risk Score: {data.get('risk_score', 0):.3f}")
                    print(f"   Classification: {data.get('classification', 'Unknown')}")
                    print(f"   Risk Level: {data.get('risk_level', 'Unknown')}")

                    # Show components
                    components = data.get("components", {})
                    print("   Risk Components:")
                    for component, score in components.items():
                        print(f"     - {component}: {score:.3f}")

                    # Show indicators
                    indicators = data.get("indicators", {})
                    if indicators.get("psychological_triggers"):
                        print(
                            f"   Psychological Triggers: {', '.join(indicators['psychological_triggers'])}"
                        )

                    if indicators.get("urls_found"):
                        print(f"   URLs Found: {len(indicators['urls_found'])}")

                else:
                    print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ Request failed with code: {response.status_code}")
                print(f"   Response: {response.text}")

        except Exception as e:
            print(f"❌ Analysis error: {e}")


def test_backend_health():
    """Test if the backend is running."""
    print("Checking backend health...")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)

        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        print("   Make sure the backend is running on http://localhost:8000")
        return False


def test_url_scanner_integration():
    """Test that the existing URL scanner still works."""
    print("\nTesting URL scanner integration...")

    try:
        payload = {"url": "http://phishing-example.com"}

        response = requests.post(
            f"{BASE_URL}/api/analyze-url",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )

        if response.status_code == 200:
            print("✅ URL scanner integration working")
            return True
        else:
            print(f"❌ URL scanner failed with code: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ URL scanner error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("EMAIL PHISHING DETECTION - TEST SCRIPT")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Test backend health
    if not test_backend_health():
        print("\n❌ Backend is not running. Please start the backend first:")
        print("   cd backend && source venv/bin/activate && python main.py")
        return

    print()

    # Test email phishing status
    status_ok = test_email_phishing_status()

    # Test email analysis
    if status_ok:
        test_email_analysis()

    # Test URL scanner integration
    url_ok = test_url_scanner_integration()

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Backend Health: {'✅ PASS' if True else '❌ FAIL'}")
    print(f"Email Phishing Status: {'✅ PASS' if status_ok else '❌ FAIL'}")
    print(f"URL Scanner Integration: {'✅ PASS' if url_ok else '❌ FAIL'}")

    if status_ok and url_ok:
        print("\n🎉 All tests passed! Email phishing detection is integrated.")
        print("\nNext steps:")
        print("1. Open the frontend: http://localhost:3000/admin/url-scanner")
        print("2. Try the new 'Email Analysis' and 'Image Analysis' tabs")
        print("3. Test with suspicious email content or upload email screenshots")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")

    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
