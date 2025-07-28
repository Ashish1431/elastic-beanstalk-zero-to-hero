# Module 1: Introduction to AWS Elastic Beanstalk

**Duration:** 30 minutes  
**Difficulty:** Beginner

## 🎯 Learning Objectives

In this module, you will:
- Understand what AWS Elastic Beanstalk is and its benefits
- Learn about Elastic Beanstalk architecture and components
- Deploy your first application to Elastic Beanstalk
- Navigate the Elastic Beanstalk console
- Understand basic configuration options

## 📖 What is AWS Elastic Beanstalk?

AWS Elastic Beanstalk is a Platform-as-a-Service (PaaS) offering that makes it easy to deploy and manage applications in the AWS cloud. You simply upload your code, and Elastic Beanstalk automatically handles:

- **Capacity provisioning** - Auto-scaling groups, load balancers
- **Load balancing** - Application Load Balancer configuration
- **Auto-scaling** - Automatic scaling based on demand
- **Application health monitoring** - Health checks and monitoring
- **Version management** - Application version control

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Developer     │    │  Elastic         │    │   AWS           │
│                 │───▶│  Beanstalk       │───▶│   Resources     │
│   (Your Code)   │    │  Platform        │    │   (EC2, ALB,    │
│                 │    │                  │    │    ASG, etc.)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Key Components:
- **Application**: A logical collection of components (versions, environments)
- **Application Version**: A specific iteration of deployable code
- **Environment**: A version deployed on AWS resources
- **Platform**: The runtime environment (Node.js, Python, Java, etc.)

## 🚀 Hands-On Lab: Deploy Your First Application

### Step 1: Prepare the Application

We'll deploy a simple HTML website to get started.

1. **Review the application files:**
   - `index.html` - Main webpage
   - `styles.css` - Styling
   - `script.js` - Basic JavaScript functionality

### Step 2: Deploy Using AWS Console

1. **Access Elastic Beanstalk Console:**
   - Go to AWS Console → Elastic Beanstalk
   - Click "Create Application"

2. **Configure Application:**
   - **Application name**: `my-first-eb-app`
   - **Platform**: Choose "Node.js" (we'll use this for static files)
   - **Application code**: Upload the provided ZIP file

3. **Create Environment:**
   - **Environment name**: `production`
   - **Domain**: Choose available domain
   - Click "Create environment"

### Step 3: Deploy Using EB CLI (Alternative)

```bash
# Initialize EB application
eb init

# Create and deploy environment
eb create production

# Open application in browser
eb open
```

## 📁 Application Structure

```
01-introduction/
├── README.md           # This file
├── index.html         # Main HTML file
├── styles.css         # CSS styling
├── script.js          # JavaScript functionality
├── app.zip           # Deployment package
└── deployment-guide.md # Detailed deployment steps
```

## 🔧 Configuration Options

### Environment Variables
- Set via Console: Configuration → Software → Environment properties
- Common variables: `NODE_ENV`, `PORT`, custom app settings

### Instance Configuration
- **Instance type**: t3.micro (free tier eligible)
- **Auto Scaling**: Min 1, Max 4 instances
- **Load balancer**: Application Load Balancer

### Monitoring
- **Health monitoring**: Application health dashboard
- **Logs**: Access via Console or EB CLI
- **Metrics**: CloudWatch integration

## 🎯 Lab Tasks

### Task 1: Basic Deployment
1. Deploy the provided HTML application
2. Access the application URL
3. Verify the application is running correctly

### Task 2: Environment Exploration
1. Navigate through the EB console
2. Check the health status
3. View application logs
4. Explore configuration options

### Task 3: Make Changes
1. Modify the `index.html` file
2. Create a new application version
3. Deploy the updated version
4. Verify changes are live

## 🔍 Key Concepts Learned

- **Platform as a Service (PaaS)**: Abstraction layer over infrastructure
- **Application Versions**: Code deployment and rollback capabilities
- **Environments**: Isolated deployment targets
- **Health Monitoring**: Automatic health checks and recovery
- **Configuration Management**: Environment-specific settings

## 🚨 Common Issues & Solutions

### Issue 1: Deployment Fails
**Solution**: Check application logs in EB console → Logs → Request Logs

### Issue 2: Application Not Accessible
**Solution**: Verify security group settings and health checks

### Issue 3: Wrong Platform
**Solution**: Ensure you select the correct platform for your application type

## 📚 Additional Resources

- [AWS Elastic Beanstalk Developer Guide](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Supported Platforms](https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/)
- [EB CLI Documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html)

## ✅ Module Completion Checklist

- [ ] Successfully deployed first application
- [ ] Accessed application via provided URL
- [ ] Explored EB console interface
- [ ] Viewed application logs
- [ ] Made and deployed a code change
- [ ] Understood basic EB concepts

## ➡️ Next Steps

Ready for more advanced features? Continue to [Module 2: Node.js Application with DynamoDB](../02-nodejs-dynamodb/README.md) to learn about:
- Database integration
- Environment variables
- SNS notifications
- Advanced configuration

---

**Congratulations!** You've completed your first Elastic Beanstalk deployment. You now understand the basics of how EB simplifies application deployment and management.