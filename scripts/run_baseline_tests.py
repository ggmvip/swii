#!/usr/bin/env python3
"""
Run all baseline tests
"""

import subprocess
import sys


def run_test(test_name, command):
    """Run a test script"""
    print(f"{'='*60}")
    print(f"Running: {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"{test_name} PASSED")
        return True
    except subprocess.CalledProcessError:
        print(f"{test_name} FAILED")
        return False


def main():
    tests = [
        ("Camera Validation", "python3 tests/test_camera.py"),
        ("PyZbar Baseline", "python3 tests/test_pyzbar_baseline.py"),
        ("API Client Test", "python3 -m pytest tests/test_api.py -v"),
    ]
    
    results = []
    for name, cmd in tests:
        results.append(run_test(name, cmd))
    
    print(f"{'='*60}")
    print("BASELINE TEST SUMMARY")
    print(f"{'='*60}")
    
    for (name, _), passed in zip(tests, results):
        status = "PASSED" if passed else "FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(results)
    print(f"Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
