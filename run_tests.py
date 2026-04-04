#!/usr/bin/env python3
"""Test runner with error handling"""

import sys
import subprocess
import os


def run_tests():
    """Run all tests with error handling"""
    print("=" * 60)
    print("NASA Mars Weather Integration - Test Suite")
    print("=" * 60)
    
    # Set environment variable for tests
    os.environ["NASA_API_KEY"] = "test_key"
    
    try:
        # Run pytest with verbose output and coverage
        cmd = [
            "python", "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "-ra"
        ]
        
        print(f"\nRunning: {' '.join(cmd)}\n")
        
        result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode != 0:
            print("\n" + "=" * 60)
            print("⚠ Some tests failed")
            print("=" * 60)
            return 1
        else:
            print("\n" + "=" * 60)
            print("✓ All tests passed!")
            print("=" * 60)
            return 0
            
    except FileNotFoundError:
        print("Error: pytest not found. Install it with: pip install pytest")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
