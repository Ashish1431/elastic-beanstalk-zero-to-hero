#!/bin/bash

# TechStore Deployment Script for AWS Elastic Beanstalk

echo "🚀 Starting TechStore deployment to AWS Elastic Beanstalk..."

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "❌ EB CLI is not installed. Please install it first:"
    echo "   pip install awsebcli"
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

# Create deployment package
echo "📦 Creating deployment package..."

# Remove existing deployment files
rm -rf .ebignore
rm -rf .elasticbeanstalk

# Create .ebignore file
cat > .ebignore << EOF
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/
.DS_Store
*.swp
*.swo
*~
EOF

# Initialize EB application (if not already done)
if [ ! -d ".elasticbeanstalk" ]; then
    echo "🔧 Initializing Elastic Beanstalk application..."
    eb init --platform python-3.8 --region us-east-1
fi

# Create environment (if not exists)
echo "🌍 Creating/updating Elastic Beanstalk environment..."
eb create production --instance-type t2.micro --single-instance

# Deploy the application
echo "📤 Deploying application..."
eb deploy

# Get the application URL
echo "🔗 Getting application URL..."
APP_URL=$(eb status | grep CNAME | awk '{print $2}')

echo "✅ Deployment completed successfully!"
echo "🌐 Your application is available at: http://$APP_URL"
echo ""
echo "📋 Next steps:"
echo "   1. Configure your AWS credentials for DynamoDB access"
echo "   2. Set up environment variables in the Elastic Beanstalk console"
echo "   3. Test the application functionality"
echo ""
echo "🔧 To view logs: eb logs"
echo "🔧 To open the application: eb open" 