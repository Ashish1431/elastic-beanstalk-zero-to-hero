# 🚀 TechStore Deployment Instructions

## **Overview**
This guide will help you deploy the TechStore e-commerce application to AWS Elastic Beanstalk with DynamoDB integration.

## **Prerequisites**
- AWS Account with appropriate permissions
- Python 3.8+ installed
- AWS CLI configured
- Git (optional)

---

## **Step 1: Environment Setup**

### **1.1 Navigate to Project Directory**
```bash
cd /Users/pravinmenghani/Documents/elastic-beanstalk
```

### **1.2 Create and Activate Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### **1.3 Install Dependencies**
```bash
# Install Python packages
pip install -r requirements.txt

# Install AWS CLI and EB CLI
pip install awsebcli
```

---

## **Step 2: AWS Configuration**

### **2.1 Configure AWS Credentials**
```bash
aws configure
```
Enter the following information when prompted:
- **AWS Access Key ID**: Your AWS access key
- **AWS Secret Access Key**: Your AWS secret key
- **Default region name**: `us-east-1`
- **Default output format**: `json`

### **2.2 Verify AWS Configuration**
```bash
aws sts get-caller-identity
```
This should return your AWS account information.

---

## **Step 3: Elastic Beanstalk Setup**

### **3.1 Initialize EB Project (First Time Only)**
```bash
eb init
```

**Follow the prompts:**
- Select your region (e.g., `us-east-1`)
- Choose application name (e.g., `techstore`)
- Select Python platform
- Choose Python version (3.8 or higher)
- Set up SSH (optional)

### **3.2 Create Environment**
```bash
eb create production --instance-type t2.micro --single
```

**Or use the deployment script:**
```bash
./deploy.sh
```

---

## **Step 4: Deploy Application**

### **4.1 Deploy to AWS**
```bash
eb deploy
```

**Expected Output:**
```
Creating application version archive "app-XXXXXXXXXX".
Uploading techstore/app-XXXXXXXXXX.zip to S3. This may take a while.
Upload Complete.
Environment update is starting.
Deploying new version to instance(s).
Instance deployment completed successfully.
New application version was deployed to running EC2 instances.
Environment update completed successfully.
```

### **4.2 Open Application**
```bash
eb open
```

---

## **Step 5: Verify Deployment**

### **5.1 Check Application Status**
```bash
eb status
```

### **5.2 Test Application Features**
1. **Home Page**: Visit the application URL
2. **User Registration**: Try registering a new user
3. **User Login**: Test login functionality
4. **DynamoDB**: Check if `ecommerce-users` table was created

### **5.3 Check DynamoDB Table**
- Go to [AWS DynamoDB Console](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:)
- Look for table named `ecommerce-users`
- Verify it has the correct schema:
  - Primary Key: `email` (String)

---

## **Step 6: Troubleshooting**

### **6.1 View Application Logs**
```bash
eb logs
```

### **6.2 Check Environment Variables**
```bash
eb printenv
```

**Expected Environment Variables:**
- `AWS_DEFAULT_REGION = us-east-1`
- `DYNAMODB_TABLE = ecommerce-users`
- `FLASK_DEBUG = False`
- `FLASK_ENV = production`
- `SECRET_KEY = your-super-secret-key-change-in-production`

### **6.3 Redeploy if Needed**
```bash
eb deploy
```

---

## **Step 7: Common Commands Reference**

| Command | Description |
|---------|-------------|
| `eb status` | Check deployment status |
| `eb logs` | View application logs |
| `eb deploy` | Deploy new version |
| `eb open` | Open app in browser |
| `eb printenv` | Show environment variables |
| `eb config` | Edit environment configuration |
| `eb terminate` | Delete environment |

---

## **Step 8: Application Features**

### **8.1 What's Included**
- ✅ User registration and authentication
- ✅ DynamoDB integration for user storage
- ✅ Modern responsive e-commerce UI
- ✅ Shopping cart functionality
- ✅ User profile management
- ✅ RESTful API endpoints

### **8.2 Database Schema**
**Table: `ecommerce-users`**
- `email` (String, Primary Key)
- `name` (String)
- `password` (String, hashed)
- `created_at` (String, ISO timestamp)

---

## **Step 9: Security Considerations**

### **9.1 Update Secret Key**
In production, update the `SECRET_KEY` environment variable:
```bash
eb config
```
Navigate to Software → Environment properties and update:
- `SECRET_KEY`: Generate a strong secret key

### **9.2 IAM Permissions**
The application requires DynamoDB permissions:
- `dynamodb:CreateTable`
- `dynamodb:DescribeTable`
- `dynamodb:GetItem`
- `dynamodb:PutItem`
- `dynamodb:Scan`
- `dynamodb:UpdateItem`
- `dynamodb:DeleteItem`

---

## **Step 10: Scaling and Maintenance**

### **10.1 Monitor Application**
- Use AWS CloudWatch for monitoring
- Check application logs regularly
- Monitor DynamoDB usage and costs

### **10.2 Update Application**
```bash
# Make code changes
# Deploy updates
eb deploy
```

### **10.3 Scale Environment**
```bash
eb config
```
Navigate to Capacity and adjust:
- Instance type
- Number of instances
- Auto-scaling settings

---

## **🎉 Success Indicators**

Your deployment is successful when:
- ✅ Application loads without errors
- ✅ User registration works
- ✅ DynamoDB table `ecommerce-users` exists
- ✅ Login/logout functionality works
- ✅ All pages load correctly

---

## **📞 Support**

If you encounter issues:
1. Check the logs: `eb logs`
2. Verify AWS credentials: `aws sts get-caller-identity`
3. Ensure all dependencies are installed
4. Check IAM permissions for DynamoDB access

---

## **🔗 Useful Links**

- [AWS Elastic Beanstalk Console](https://console.aws.amazon.com/elasticbeanstalk/)
- [AWS DynamoDB Console](https://console.aws.amazon.com/dynamodb/)
- [AWS IAM Console](https://console.aws.amazon.com/iam/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

**Happy Deploying! 🚀** 