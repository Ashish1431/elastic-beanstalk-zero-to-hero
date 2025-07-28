#!/usr/bin/env python3
"""
Simple test script to verify the Flask application can start locally.
This script will test basic functionality without requiring AWS credentials.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock boto3 to avoid AWS credentials requirement
class MockDynamoDB:
    def __init__(self):
        self.users = {}
    
    def Table(self, table_name):
        return MockTable(self.users)

class MockTable:
    def __init__(self, users):
        self.users = users
    
    def load(self):
        pass
    
    def get_item(self, Key):
        email = Key['email']
        if email in self.users:
            return {'Item': self.users[email]}
        return {}
    
    def put_item(self, Item):
        self.users[Item['email']] = Item
    
    def scan(self):
        return {'Items': list(self.users.values())}

# Mock the DynamoDB resource
mock_dynamodb = MockDynamoDB()

def test_flask_app():
    """Test that the Flask app can be imported and basic routes work."""
    
    # Mock boto3 before importing application
    with patch('boto3.resource', return_value=mock_dynamodb):
        try:
            from application import app
            
            # Test app creation
            assert app is not None, "Flask app should be created"
            print("✅ Flask app created successfully")
            
            # Test basic routes
            with app.test_client() as client:
                # Test home page
                response = client.get('/')
                assert response.status_code == 200, f"Home page should return 200, got {response.status_code}"
                print("✅ Home page loads successfully")
                
                # Test register page
                response = client.get('/register')
                assert response.status_code == 200, f"Register page should return 200, got {response.status_code}"
                print("✅ Register page loads successfully")
                
                # Test login page
                response = client.get('/login')
                assert response.status_code == 200, f"Login page should return 200, got {response.status_code}"
                print("✅ Login page loads successfully")
                
                # Test profile page (should redirect to login)
                response = client.get('/profile')
                assert response.status_code == 302, f"Profile page should redirect, got {response.status_code}"
                print("✅ Profile page redirects when not logged in")
                
            print("\n🎉 All basic tests passed!")
            return True
            
        except ImportError as e:
            print(f"❌ Failed to import application: {e}")
            return False
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False

def test_user_registration():
    """Test user registration functionality."""
    
    with patch('boto3.resource', return_value=mock_dynamodb):
        try:
            from application import app
            
            with app.test_client() as client:
                # Test user registration
                response = client.post('/register', data={
                    'name': 'Test User',
                    'email': 'test@example.com',
                    'password': 'testpassword123',
                    'confirm_password': 'testpassword123'
                }, follow_redirects=True)
                
                assert response.status_code == 200, f"Registration should succeed, got {response.status_code}"
                print("✅ User registration works")
                
                # Test duplicate registration
                response = client.post('/register', data={
                    'name': 'Test User 2',
                    'email': 'test@example.com',
                    'password': 'testpassword123',
                    'confirm_password': 'testpassword123'
                }, follow_redirects=True)
                
                # Should show error for duplicate email
                assert b'Email already registered' in response.data, "Should show duplicate email error"
                print("✅ Duplicate email detection works")
                
            print("🎉 User registration tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Registration test failed: {e}")
            return False

if __name__ == '__main__':
    print("🧪 Testing TechStore Flask Application")
    print("=" * 50)
    
    # Test basic app functionality
    basic_test_passed = test_flask_app()
    
    if basic_test_passed:
        # Test user registration
        registration_test_passed = test_user_registration()
        
        if registration_test_passed:
            print("\n🎉 All tests passed! The application is ready for deployment.")
            print("\n📋 Next steps:")
            print("   1. Configure AWS credentials: aws configure")
            print("   2. Install EB CLI: pip install awsebcli")
            print("   3. Deploy to Elastic Beanstalk: ./deploy.sh")
        else:
            print("\n❌ Registration tests failed. Please check the application code.")
            sys.exit(1)
    else:
        print("\n❌ Basic tests failed. Please check the application code.")
        sys.exit(1) 