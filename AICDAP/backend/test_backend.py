#!/usr/bin/env python3
"""
Simple backend test script to verify the insider threat detection system works.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.insider_threat.graph_analyzer import InsiderThreatDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_insider_threat_system():
    """Test the insider threat detection system."""
    print("=" * 60)
    print("INSIDER THREAT DETECTION SYSTEM - BACKEND TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        # Initialize the detector
        logger.info("Initializing InsiderThreatDetector...")
        detector = InsiderThreatDetector()

        # Test data loading
        logger.info("Testing data loading...")
        logon, device, http = await detector.load_background_logs()

        print(f"✅ Data loaded successfully:")
        print(f"   Logon records: {len(logon)}")
        print(f"   Device records: {len(device)}")
        print(f"   HTTP records: {len(http)}")

        # Test malicious data loading
        logger.info("Testing malicious data loading...")
        await detector.load_malicious_data()

        print(f"✅ Malicious data loaded:")
        print(f"   Malicious users: {len(detector.malicious_users)}")
        print(f"   Malicious days: {len(detector.malicious_days)}")
        if detector.malicious_users:
            print(f"   Sample users: {list(detector.malicious_users)[:5]}")

        # Test analysis
        logger.info("Running full analysis...")
        start_time = datetime.now()

        result = await detector.run_analysis()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print(f"✅ Analysis completed in {duration:.2f} seconds")

        if result["status"] == "success":
            print("✅ Analysis successful!")

            summary = result["summary"]
            print(f"   Total nodes: {summary.get('total_nodes', 0)}")
            print(f"   Total edges: {summary.get('total_edges', 0)}")
            print(f"   Users analyzed: {summary.get('users_analyzed', 0)}")
            print(f"   Known malicious: {summary.get('known_malicious', 0)}")
            print(f"   Analysis date: {result.get('analysis_date')}")

            suspicious_users = result.get("suspicious_users", [])
            print(f"   Suspicious users found: {len(suspicious_users)}")

            if suspicious_users:
                print("   Top 5 suspicious users:")
                for i, user in enumerate(suspicious_users[:5], 1):
                    score = user.get("score", 0) * 100
                    is_known = user.get("is_known_malicious", False)
                    status = " (Known threat)" if is_known else ""
                    print(f"     {i}. {user.get('user')}: {score:.1f}%{status}")

            # Check training metrics
            losses = result.get("training_losses", [])
            if losses:
                print(f"   Training epochs: {len(losses)}")
                print(f"   Initial loss: {losses[0]:.4f}")
                print(f"   Final loss: {losses[-1]:.4f}")
                improvement = (losses[0] - losses[-1]) / losses[0] * 100
                print(f"   Loss improvement: {improvement:.1f}%")

            return True
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        logger.exception("Test failed")
        return False


def check_dependencies():
    """Check if all required dependencies are available."""
    print("Checking dependencies...")

    required_modules = ["torch", "torch_geometric", "pandas", "networkx", "fastapi"]

    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing_modules.append(module)

    if missing_modules:
        print(f"\n❌ Missing dependencies: {', '.join(missing_modules)}")
        print("Please install them with:")
        print("pip install torch torch-geometric pandas networkx fastapi")
        return False

    print("✅ All dependencies available")
    return True


def check_data_files():
    """Check if data files are available."""
    print("\nChecking data files...")

    base_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(base_path, "..")

    data_paths = [
        os.path.join(
            project_root, "model", "data_r3.2", "processed", "logon_edges_day.csv"
        ),
        os.path.join(
            project_root, "model", "data_r3.2", "processed", "device_edges_day.csv"
        ),
        os.path.join(
            project_root, "model", "data_r3.2", "processed", "http_edges_day.csv"
        ),
    ]

    answer_paths = [
        os.path.join(project_root, "model", "answers", "r3.2-1.csv"),
        os.path.join(project_root, "model", "answers", "r3.2-2.csv"),
    ]

    data_available = True
    for path in data_paths:
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"✅ {os.path.basename(path)} ({size_mb:.1f} MB)")
        else:
            print(f"❌ {os.path.basename(path)} (not found)")
            data_available = False

    print("\nChecking answer files...")
    answer_available = True
    for path in answer_paths:
        if os.path.exists(path):
            print(f"✅ {os.path.basename(path)}")
        else:
            print(f"❌ {os.path.basename(path)} (not found)")
            answer_available = False

    if not data_available:
        print("\n⚠️  Some data files are missing. The system will use mock data.")

    if not answer_available:
        print("⚠️  Some answer files are missing. Limited malicious user detection.")

    return data_available


async def main():
    """Main test function."""
    print("AICDAP Backend Test Suite")
    print("=" * 40)

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing modules.")
        return False

    # Check data files
    check_data_files()

    print("\n" + "=" * 60)

    # Run the main test
    success = await test_insider_threat_system()

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    if success:
        print("🎉 All tests passed! The insider threat detection system is working.")
        print("\nNext steps:")
        print("1. Start the backend server: python main.py")
        print("2. Start the frontend: cd ../frontend && npm start")
        print("3. Open browser: http://localhost:3000/admin/insider")
    else:
        print("❌ Tests failed. Please check the error messages above.")

    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return success


if __name__ == "__main__":
    asyncio.run(main())
