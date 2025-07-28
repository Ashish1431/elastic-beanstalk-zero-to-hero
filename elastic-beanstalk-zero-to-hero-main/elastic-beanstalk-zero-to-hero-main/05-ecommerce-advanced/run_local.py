#!/usr/bin/env python3
"""
Local development server with mocked DynamoDB.
This allows you to test the application without AWS credentials.
"""

import os
import sys
from unittest.mock import patch, MagicMock

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

if __name__ == '__main__':
    print("🚀 Starting TechStore with Mocked DynamoDB")
    print("=" * 50)
    print("📝 This version uses a mock database for local testing")
    print("🌐 The application will be available at: http://localhost:8000")
    print("🔧 No AWS credentials required for local testing")
    print("=" * 50)
    
    # Mock boto3 before importing application
    with patch('boto3.resource', return_value=mock_dynamodb):
        from application import app
        
        # Set development environment
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = 'True'
        
        print("\n✅ Application started successfully!")
        print("📋 Available routes:")
        print("   - Home: http://localhost:8000/")
        print("   - Register: http://localhost:8000/register")
        print("   - Login: http://localhost:8000/login")
        print("   - Profile: http://localhost:8000/profile (requires login)")
        print("\n🛑 Press Ctrl+C to stop the server")
        
        # Run the application
        app.run(debug=True, host='0.0.0.0', port=8000) 