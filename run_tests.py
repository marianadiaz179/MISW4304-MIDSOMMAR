#!/usr/bin/env python3
"""
Comprehensive Test Runner for Blacklist Microservice
Universidad de los Andes - MISW4304

This script provides both unit tests and integration tests for the API endpoints.
"""

import unittest
import requests
import json
import uuid
import time
import sys
import os
from datetime import datetime

# Add the api directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'api', 'src'))

class TestBlacklistMicroservice(unittest.TestCase):
    """Test cases for the Blacklist Microservice API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration"""
        cls.base_url = "http://localhost:3000"
        cls.secret_token = "test_secret_token_123"
        cls.headers = {
            "Authorization": f"Bearer {cls.secret_token}",
            "Content-Type": "application/json"
        }
        cls.test_email = f"test_{int(time.time())}@example.com"
        cls.test_uuid = str(uuid.uuid4())
        
        # Check if server is running
        try:
            response = requests.get(f"{cls.base_url}/blacklists/ping", timeout=5)
            if response.status_code != 200:
                raise Exception("Server health check failed")
        except requests.exceptions.RequestException:
            raise Exception(f"Server is not running at {cls.base_url}. Please start the server first.")
    
    def test_01_health_check(self):
        """Test the health check endpoint"""
        print("\n🔍 Testing health check endpoint...")
        response = requests.get(f"{self.base_url}/blacklists/ping")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "pong")
        self.assertLess(response.elapsed.total_seconds(), 1.0)
        print("✅ Health check passed")
    
    def test_02_add_email_success(self):
        """Test adding an email to blacklist successfully"""
        print(f"\n📧 Testing add email to blacklist: {self.test_email}")
        
        data = {
            "email": self.test_email,
            "app_uuid": self.test_uuid,
            "blocked_reason": "Test reason for blacklisting"
        }
        
        response = requests.post(
            f"{self.base_url}/blacklists",
            headers=self.headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["msg"], "Email added to the blacklist")
        self.assertLess(response.elapsed.total_seconds(), 2.0)
        print("✅ Add email to blacklist passed")
    
    def test_03_check_email_blacklisted(self):
        """Test checking if an email is blacklisted"""
        print(f"\n🔍 Testing check email blacklist: {self.test_email}")
        
        response = requests.get(
            f"{self.base_url}/blacklists/{self.test_email}",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data["blacklisted"])
        self.assertIn("blocked_reason", response_data)
        self.assertLess(response.elapsed.total_seconds(), 1.0)
        print("✅ Check email blacklist passed")
    
    def test_04_add_duplicate_email(self):
        """Test adding a duplicate email"""
        print(f"\n🔄 Testing duplicate email: {self.test_email}")
        
        data = {
            "email": self.test_email,
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": "Duplicate test"
        }
        
        response = requests.post(
            f"{self.base_url}/blacklists",
            headers=self.headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 409)
        response_data = response.json()
        self.assertEqual(response_data["msg"], "Email is already in the blacklist")
        print("✅ Duplicate email test passed")
    
    def test_05_missing_parameters(self):
        """Test missing required parameters"""
        print("\n❌ Testing missing parameters...")
        
        data = {"email": "test2@example.com"}
        
        response = requests.post(
            f"{self.base_url}/blacklists",
            headers=self.headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("Missing parameter", response_data["msg"])
        print("✅ Missing parameters test passed")
    
    def test_06_invalid_email(self):
        """Test invalid email format"""
        print("\n❌ Testing invalid email format...")
        
        data = {
            "email": "invalid-email",
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": "Test with invalid email"
        }
        
        response = requests.post(
            f"{self.base_url}/blacklists",
            headers=self.headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("not a valid email", response_data["msg"])
        print("✅ Invalid email test passed")
    
    def test_07_invalid_uuid(self):
        """Test invalid UUID format"""
        print("\n❌ Testing invalid UUID format...")
        
        data = {
            "email": "test3@example.com",
            "app_uuid": "invalid-uuid",
            "blocked_reason": "Test with invalid UUID"
        }
        
        response = requests.post(
            f"{self.base_url}/blacklists",
            headers=self.headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("not a valid UUID", response_data["msg"])
        print("✅ Invalid UUID test passed")
    
    def test_08_invalid_token(self):
        """Test invalid authorization token"""
        print("\n🔒 Testing invalid token...")
        
        invalid_headers = {
            "Authorization": "Bearer invalid_token",
            "Content-Type": "application/json"
        }
        
        data = {
            "email": "test4@example.com",
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": "Test with invalid token"
        }
        
        response = requests.post(
            f"{self.base_url}/blacklists",
            headers=invalid_headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        self.assertEqual(response_data["msg"], "Invalid token")
        print("✅ Invalid token test passed")
    
    def test_09_missing_authorization(self):
        """Test missing authorization header"""
        print("\n🔒 Testing missing authorization...")
        
        headers = {"Content-Type": "application/json"}
        
        data = {
            "email": "test5@example.com",
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": "Test without authorization"
        }
        
        response = requests.post(
            f"{self.base_url}/blacklists",
            headers=headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 403)
        response_data = response.json()
        self.assertEqual(response_data["msg"], "Authorization header is required")
        print("✅ Missing authorization test passed")
    
    def test_10_check_nonexistent_email(self):
        """Test checking a non-existent email"""
        print("\n🔍 Testing non-existent email...")
        
        nonexistent_email = f"nonexistent_{int(time.time())}@example.com"
        
        response = requests.get(
            f"{self.base_url}/blacklists/{nonexistent_email}",
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data["blacklisted"])
        self.assertLess(response.elapsed.total_seconds(), 1.0)
        print("✅ Non-existent email test passed")
    
    def test_11_blocked_reason_too_long(self):
        """Test blocked reason exceeding 255 characters"""
        print("\n❌ Testing blocked reason too long...")
        
        long_reason = "x" * 256  # 256 characters
        
        data = {
            "email": f"test6_{int(time.time())}@example.com",
            "app_uuid": str(uuid.uuid4()),
            "blocked_reason": long_reason
        }
        
        response = requests.post(
            f"{self.base_url}/blacklists",
            headers=self.headers,
            json=data
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("maximum of 255 characters", response_data["msg"])
        print("✅ Blocked reason too long test passed")
    
    def test_12_get_with_invalid_token(self):
        """Test GET endpoint with invalid token"""
        print("\n🔒 Testing GET with invalid token...")
        
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        
        response = requests.get(
            f"{self.base_url}/blacklists/test@example.com",
            headers=invalid_headers
        )
        
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        self.assertEqual(response_data["msg"], "Invalid token")
        print("✅ GET with invalid token test passed")


def run_performance_tests():
    """Run performance tests"""
    print("\n🚀 Running Performance Tests...")
    print("=" * 50)
    
    base_url = "http://localhost:3000"
    headers = {
        "Authorization": "Bearer test_secret_token_123",
        "Content-Type": "application/json"
    }
    
    # Test response times
    start_time = time.time()
    response = requests.get(f"{base_url}/blacklists/ping")
    health_check_time = time.time() - start_time
    
    print(f"Health Check Response Time: {health_check_time:.3f}s")
    
    # Test concurrent requests
    import concurrent.futures
    
    def make_request():
        return requests.get(f"{base_url}/blacklists/ping")
    
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in futures]
    
    concurrent_time = time.time() - start_time
    print(f"10 Concurrent Requests Time: {concurrent_time:.3f}s")
    print(f"Average Response Time: {concurrent_time/10:.3f}s")
    
    # Verify all requests succeeded
    success_count = sum(1 for r in results if r.status_code == 200)
    print(f"Successful Requests: {success_count}/10")


def main():
    """Main test runner"""
    print("🧪 Blacklist Microservice Test Suite")
    print("Universidad de los Andes - MISW4304")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:3000/blacklists/ping", timeout=5)
        if response.status_code != 200:
            print("❌ Server health check failed")
            return 1
    except requests.exceptions.RequestException:
        print("❌ Server is not running at http://localhost:3000")
        print("💡 Please start the server first with:")
        print("   cd api && source ../venv/bin/activate && python src/app.py")
        return 1
    
    print("✅ Server is running")
    print("")
    
    # Run unit tests
    print("🧪 Running Unit Tests...")
    print("-" * 30)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBlacklistMicroservice)
    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
    
    # Run tests and capture results
    result = runner.run(suite)
    
    # Print results
    if result.wasSuccessful():
        print(f"✅ All {result.testsRun} tests passed!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors out of {result.testsRun} tests")
        for failure in result.failures:
            print(f"   FAIL: {failure[0]}")
        for error in result.errors:
            print(f"   ERROR: {error[0]}")
    
    # Run performance tests
    run_performance_tests()
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests completed successfully!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
