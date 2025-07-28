# Module 2: Node.js Application with DynamoDB Integration

**Duration:** 45 minutes  
**Difficulty:** Beginner-Intermediate

## 🎯 Learning Objectives

In this module, you will:
- Deploy a Node.js Express application to Elastic Beanstalk
- Integrate with Amazon DynamoDB for data storage
- Configure Amazon SNS for notifications
- Use environment variables for configuration
- Implement IAM roles and policies
- Handle form submissions and data processing

## 📖 Application Overview

This module features a customer signup application that demonstrates:
- **Express.js Framework**: Modern Node.js web framework
- **Bootstrap Themes**: Dynamic theme switching
- **DynamoDB Integration**: NoSQL database for user data
- **SNS Notifications**: Email notifications for new signups
- **Cluster Mode**: Multi-process Node.js application

## 🏗️ Architecture Diagram

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   User      │───▶│  Application │───▶│  DynamoDB   │
│  Browser    │    │  Load        │    │   Table     │
└─────────────┘    │  Balancer    │    └─────────────┘
                   └──────────────┘           │
                          │                   │
                   ┌──────────────┐          │
                   │   EC2        │          │
                   │ Instances    │          │
                   └──────────────┘          │
                          │                   │
                   ┌──────────────┐          │
                   │     SNS      │◀─────────┘
                   │    Topic     │
                   └──────────────┘
```

## 📁 Application Structure

```
02-nodejs-dynamodb/
├── README.md                    # This file
├── app.js                      # Main application file
├── package.json                # Node.js dependencies
├── npm-shrinkwrap.json         # Locked dependency versions
├── views/
│   └── index.ejs              # EJS template
├── static/                    # Static assets
│   ├── bootstrap/             # Bootstrap framework
│   └── jquery/               # jQuery library
├── .ebextensions/            # EB configuration
│   ├── create-dynamodb-table.config
│   ├── create-sns-topic.config
│   ├── nginx.config
│   └── options.config
├── iam_policy.json           # Required IAM permissions
└── .gitignore               # Git ignore rules
```

## 🚀 Prerequisites

### AWS Resources Required
- DynamoDB table for storing signup data
- SNS topic for notifications
- IAM instance profile with appropriate permissions

### Local Development
- Node.js 14+ installed
- AWS CLI configured
- EB CLI installed (optional)

## 🔧 Setup Instructions

### Step 1: Review IAM Policy

The application requires specific IAM permissions. Review `iam_policy.json`:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:CreateTable",
                "dynamodb:DescribeTable",
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sns:CreateTopic",
                "sns:Publish",
                "sns:Subscribe"
            ],
            "Resource": "*"
        }
    ]
}
```

### Step 2: Create IAM Instance Profile

1. **Create IAM Role:**
   ```bash
   aws iam create-role --role-name aws-elasticbeanstalk-sample-role \
     --assume-role-policy-document file://trust-policy.json
   ```

2. **Attach Policy:**
   ```bash
   aws iam put-role-policy --role-name aws-elasticbeanstalk-sample-role \
     --policy-name EBSampleAppPolicy \
     --policy-document file://iam_policy.json
   ```

3. **Create Instance Profile:**
   ```bash
   aws iam create-instance-profile --instance-profile-name aws-elasticbeanstalk-sample-role
   aws iam add-role-to-instance-profile --instance-profile-name aws-elasticbeanstalk-sample-role \
     --role-name aws-elasticbeanstalk-sample-role
   ```

### Step 3: Deploy Application

#### Option A: Using EB CLI
```bash
# Initialize EB application
eb init -r us-east-1 -p "Node.js"

# Create environment with instance profile
eb create --instance_profile aws-elasticbeanstalk-sample-role

# Open application
eb open
```

#### Option B: Using AWS Console
1. Go to Elastic Beanstalk Console
2. Create new application
3. Choose Node.js platform
4. Upload application ZIP
5. Configure instance profile in advanced settings

## 🎨 Application Features

### Dynamic Themes
The application supports multiple Bootstrap themes:
- **Amelia**: Dark theme with purple accents
- **Default**: Standard Bootstrap styling
- **Flatly**: Modern flat design
- **Slate**: Dark professional theme
- **United**: Orange and blue theme

Switch themes by setting the `THEME` environment variable.

### Form Processing
- **Client-side validation**: JavaScript form validation
- **Server-side processing**: Express.js route handlers
- **Data persistence**: DynamoDB storage
- **Notifications**: SNS email alerts

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REGION` | AWS region | `us-east-1` |
| `STARTUP_SIGNUP_TABLE` | DynamoDB table name | Auto-created |
| `NEW_SIGNUP_TOPIC` | SNS topic ARN | Auto-created |
| `THEME` | Bootstrap theme | `flatly` |
| `PORT` | Application port | `3000` |

### .ebextensions Configuration

The `.ebextensions` directory contains:

1. **create-dynamodb-table.config**: Creates DynamoDB table
2. **create-sns-topic.config**: Creates SNS topic
3. **nginx.config**: Nginx proxy configuration
4. **options.config**: Environment variables

## 🧪 Testing the Application

### Local Testing
```bash
# Install dependencies
npm install

# Set environment variables
export REGION=us-east-1
export STARTUP_SIGNUP_TABLE=signup-table
export NEW_SIGNUP_TOPIC=arn:aws:sns:us-east-1:123456789012:new-signup

# Run application
node app.js
```

### Production Testing
1. **Access Application**: Use EB environment URL
2. **Submit Form**: Fill out signup form
3. **Verify Storage**: Check DynamoDB table
4. **Check Notifications**: Verify SNS message delivery

## 🔍 Monitoring & Troubleshooting

### Application Logs
```bash
# View logs using EB CLI
eb logs

# Or download logs
eb logs --all
```

### Common Issues

#### Issue 1: DynamoDB Access Denied
**Solution**: Verify IAM instance profile has DynamoDB permissions

#### Issue 2: SNS Publishing Fails
**Solution**: Check SNS topic exists and permissions are correct

#### Issue 3: Application Won't Start
**Solution**: Check Node.js version compatibility and dependencies

### Health Monitoring
- Monitor application health in EB console
- Set up CloudWatch alarms for key metrics
- Configure SNS notifications for health events

## 📊 Performance Optimization

### Cluster Mode
The application uses Node.js cluster module for:
- **Multi-process**: Utilizes all CPU cores
- **Load distribution**: Spreads requests across workers
- **Fault tolerance**: Automatic worker restart

### Caching Strategies
- **Static assets**: Served by nginx
- **Database queries**: Consider implementing caching
- **Session management**: Use external session store for scaling

## 🎯 Lab Exercises

### Exercise 1: Basic Deployment
1. Deploy the application using provided instructions
2. Test the signup form functionality
3. Verify data appears in DynamoDB
4. Confirm SNS notifications are sent

### Exercise 2: Theme Customization
1. Change the THEME environment variable
2. Deploy the update
3. Verify the new theme is applied
4. Try different theme combinations

### Exercise 3: Monitoring Setup
1. Enable detailed monitoring
2. Create CloudWatch dashboard
3. Set up alarms for key metrics
4. Test alarm notifications

## 📚 Key Concepts Learned

- **Express.js Application Structure**: MVC pattern implementation
- **DynamoDB Integration**: NoSQL database operations
- **SNS Notifications**: Pub/sub messaging pattern
- **Environment Configuration**: Managing app settings
- **IAM Security**: Role-based access control
- **Application Monitoring**: Health checks and logging

## 🔐 Security Best Practices

- **IAM Roles**: Use instance profiles, not access keys
- **Environment Variables**: Store sensitive data securely
- **Input Validation**: Sanitize all user inputs
- **HTTPS**: Enable SSL/TLS in production
- **Security Groups**: Restrict network access

## ➡️ Next Steps

Ready for containerization? Continue to [Module 3: Containerized Applications](../03-containerized-app/README.md) to learn about:
- Docker containerization
- Container deployment strategies
- Multi-stage builds
- Container orchestration

---

**Great job!** You've successfully deployed a full-stack Node.js application with database integration. You now understand how to build scalable web applications on Elastic Beanstalk.