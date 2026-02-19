#!/usr/bin/env python3
"""
Test script for the insider threat detection endpoint.
This script tests the API endpoint and verifies that the graph analysis works correctly.
"""

import asyncio
import json
import time
from datetime import datetime

import requests

# Backend URL
BASE_URL = "http://localhost:8000"


def test_insider_threat_status():
    """Test the insider threat status endpoint."""
    print("Testing insider threat status endpoint...")

    try:
        response = requests.get(f"{BASE_URL}/api/insider-threat/status")

        if response.status_code == 200:
            data = response.json()
            print("✅ Status endpoint working")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Features: {', '.join(data.get('features', []))}")
            return True
        else:
            print(f"❌ Status endpoint failed with code: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
        return False


def test_insider_threat_analysis():
    """Test the insider threat analysis endpoint."""
    print("\nTesting insider threat analysis endpoint...")
    print("This may take a moment as it involves training a neural network...")

    start_time = time.time()

    try:
        response = requests.post(
            f"{BASE_URL}/api/insider-threat/analyze",
            headers={"Content-Type": "application/json"},
            timeout=120,  # 2 minutes timeout
        )

        end_time = time.time()
        duration = end_time - start_time

        if response.status_code == 200:
            data = response.json()

            if data.get("success"):
                analysis_data = data.get("data", {})

                print("✅ Analysis completed successfully")
                print(f"   Duration: {duration:.2f} seconds")
                print(f"   Analysis Date: {analysis_data.get('analysis_date')}")

                # Check summary data
                summary = analysis_data.get("summary", {})
                print(f"   Total Nodes: {summary.get('total_nodes', 0)}")
                print(f"   Total Edges: {summary.get('total_edges', 0)}")
                print(f"   Users Analyzed: {summary.get('users_analyzed', 0)}")
                print(f"   Known Malicious: {summary.get('known_malicious', 0)}")

                # Check suspicious users
                suspicious_users = analysis_data.get("suspicious_users", [])
                print(f"   Suspicious Users Found: {len(suspicious_users)}")

                if suspicious_users:
                    print("   Top 3 Suspicious Users:")
                    for i, user in enumerate(suspicious_users[:3], 1):
                        score = user.get("score", 0) * 100
                        is_known = user.get("is_known_malicious", False)
                        print(
                            f"     {i}. {user.get('user')}: {score:.1f}% {'(Known Threat)' if is_known else ''}"
                        )

                # Check graph data
                graph_data = analysis_data.get("graph_data")
                if graph_data:
                    stats = graph_data.get("stats", {})
                    print(f"   Graph Nodes: {stats.get('total_nodes', 0)}")
                    print(f"   Graph Edges: {stats.get('total_edges', 0)}")
                    print(
                        f"   Malicious Users in Graph: {stats.get('malicious_users', 0)}"
                    )

                # Check training metrics
                training_losses = analysis_data.get("training_losses", [])
                if training_losses:
                    print(f"   Training Epochs: {len(training_losses)}")
                    print(f"   Initial Loss: {training_losses[0]:.4f}")
                    print(f"   Final Loss: {training_losses[-1]:.4f}")
                    print(
                        f"   Loss Improvement: {((training_losses[0] - training_losses[-1]) / training_losses[0] * 100):.1f}%"
                    )

                return True
            else:
                print(f"❌ Analysis failed: {data.get('message', 'Unknown error')}")
                return False

        else:
            print(f"❌ Analysis endpoint failed with code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Analysis timeout - the request took longer than 2 minutes")
        return False
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False


def test_backend_health():
    """Test if the backend is running."""
    print("Checking backend health...")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is running")
            print(f"   Status: {data.get('status')}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        print("   Make sure the backend is running on http://localhost:8000")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("INSIDER THREAT DETECTION - TEST SCRIPT")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Test backend health
    if not test_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        return

    print()

    # Test status endpoint
    status_ok = test_insider_threat_status()

    # Test analysis endpoint
    analysis_ok = test_insider_threat_analysis()

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Backend Health: {'✅ PASS' if True else '❌ FAIL'}")
    print(f"Status Endpoint: {'✅ PASS' if status_ok else '❌ FAIL'}")
    print(f"Analysis Endpoint: {'✅ PASS' if analysis_ok else '❌ FAIL'}")

    if status_ok and analysis_ok:
        print(
            "\n🎉 All tests passed! The insider threat detection system is working correctly."
        )
        print("\nNext steps:")
        print("1. Start the frontend: cd frontend && npm start")
        print("2. Navigate to: http://localhost:3000/admin/insider")
        print("3. Click 'Start Analysis' to test the full UI integration")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")

    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
