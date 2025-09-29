#!/usr/bin/env python3
"""
Test runner script for WaterPlantOperator project.
"""
import sys
import subprocess
import os
from pathlib import Path


def install_test_dependencies():
    """Install test dependencies."""
    print("Installing test dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"
        ])
        print("✓ Test dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install test dependencies: {e}")
        return False


def run_unit_tests():
    """Run unit tests."""
    print("\n" + "="*50)
    print("Running Unit Tests")
    print("="*50)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/unit/", 
            "--ignore=tests/unit/sensor/",  # Exclude hardware-dependent tests
            "-v", 
            "--tb=short",
            "--cov=run",
            "--cov-report=term-missing"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✓ Unit tests passed successfully")
            return True
        else:
            print("✗ Unit tests failed")
            return False
            
    except Exception as e:
        print(f"✗ Error running unit tests: {e}")
        return False


def run_integration_tests():
    """Run integration tests."""
    print("\n" + "="*50)
    print("Running Integration Tests")
    print("="*50)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/integration/", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✓ Integration tests passed successfully")
            return True
        else:
            print("✗ Integration tests failed")
            return False
            
    except Exception as e:
        print(f"✗ Error running integration tests: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running All Tests")
    print("="*50)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "--ignore=tests/unit/sensor/",  # Exclude hardware-dependent tests
            "-v", 
            "--tb=short",
            "--cov=run",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✓ All tests passed successfully")
            return True
        else:
            print("✗ Some tests failed")
            return False
            
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        return False


def main():
    """Main test runner function."""
    print("WaterPlantOperator Test Suite")
    print("="*50)
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Install test dependencies
    if not install_test_dependencies():
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "unit":
            success = run_unit_tests()
        elif test_type == "integration":
            success = run_integration_tests()
        elif test_type == "all":
            success = run_all_tests()
        else:
            print(f"Unknown test type: {test_type}")
            print("Usage: python run_tests.py [unit|integration|all]")
            sys.exit(1)
    else:
        # Run all tests by default
        success = run_all_tests()
    
    if success:
        print("\n" + "="*50)
        print("🎉 All tests completed successfully!")
        print("="*50)
        sys.exit(0)
    else:
        print("\n" + "="*50)
        print("❌ Some tests failed!")
        print("="*50)
        sys.exit(1)


if __name__ == "__main__":
    main()
