# Module 4: Worker Environments & Background Processing

**Duration:** 40 minutes  
**Difficulty:** Intermediate

## 🎯 Learning Objectives

In this module, you will:
- Understand worker environments vs web server environments
- Configure SQS message processing
- Implement background job processing
- Set up automated cron jobs using .ebextensions
- Handle long-running tasks efficiently
- Monitor worker environment performance

## 📖 Worker Environment Overview

Worker environments are designed for applications that process background tasks, such as:
- **Message processing**: Handle SQS messages
- **Batch jobs**: Process large datasets
- **Scheduled tasks**: Run cron jobs
- **Long-running processes**: Handle time-intensive operations
- **Decoupled processing**: Separate from web tier

### Web Server vs Worker Environment

| Feature | Web Server Environment | Worker Environment |
|---------|----------------------|-------------------|
| **Purpose** | Handle HTTP requests | Process background tasks |
| **Load Balancer** | Application Load Balancer | None |
| **Scaling** | Based on HTTP traffic | Based on SQS queue depth |
| **Endpoints** | Public HTTP endpoints | SQS message processing |
| **Use Cases** | Web applications, APIs | Background jobs, batch processing |

## 🏗️ Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Tier      │    │      SQS         │    │   Worker Tier   │
│                 │───▶│     Queue        │───▶│                 │
│ (Sends Messages)│    │                  │    │ (Processes Jobs)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                         │
                       ┌──────────────────┐    ┌─────────────────┐
                       │   CloudWatch     │    │   Cron Jobs     │
                       │   Monitoring     │    │   Scheduled     │
                       └──────────────────┘    └─────────────────┘
```

## 📁 Application Structure

```
04-worker-environment/
├── README.md              # This file
├── application.py         # WSGI application
├── .ebextensions/        # EB configuration
│   └── cron.config       # Cron job setup
└── untitled folder/      # Additional resources
```

## 🐍 Application Code Analysis

### Main Application (`application.py`)

```python
import json
import logging
from flask import Flask, request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

application = Flask(__name__)

@application.route('/', methods=['GET'])
def welcome():
    """Welcome endpoint for health checks"""
    return "Worker Environment is running!"

@application.route('/', methods=['POST'])
def process_message():
    """Process SQS messages"""
    try:
        # Parse SQS message
        message = request.get_json()
        logger.info(f"Received message: {message}")
        
        # Process the message
        # Add your business logic here
        
        return "Message processed successfully", 200
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return "Error processing message", 500

@application.route('/scheduled', methods=['POST'])
def scheduled_task():
    """Handle scheduled tasks from cron"""
    try:
        logger.info("Executing scheduled task")
        
        # Add your scheduled task logic here
        # Example: cleanup, data processing, reports
        
        return "Scheduled task completed", 200
    except Exception as e:
        logger.error(f"Error in scheduled task: {e}")
        return "Error in scheduled task", 500

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=False)
```

## ⚙️ Cron Configuration

### .ebextensions/cron.config

```yaml
files:
  "/etc/cron.d/mycron":
    mode: "000644"
    owner: root
    group: root
    content: |
      # Run every 5 minutes
      */5 * * * * root curl -X POST http://localhost/scheduled >> /tmp/cronlog.txt 2>&1
      
      # Run daily at 2 AM
      0 2 * * * root curl -X POST http://localhost/scheduled >> /tmp/cronlog.txt 2>&1

commands:
  01_create_log_file:
    command: "touch /tmp/cronlog.txt && chmod 666 /tmp/cronlog.txt"
  02_restart_cron:
    command: "service crond restart"
```

## 🚀 Deployment Instructions

### Step 1: Prepare Application

1. **Review application structure:**
   ```bash
   ls -la
   # application.py - Main WSGI app
   # .ebextensions/ - Configuration
   ```

2. **Create deployment package:**
   ```bash
   zip -r worker-app.zip application.py .ebextensions/
   ```

### Step 2: Deploy Worker Environment

#### Option A: Using EB CLI
```bash
# Initialize EB application
eb init -p python-3.8

# Create worker environment (important!)
eb create production --tier worker

# Deploy application
eb deploy

# Check status
eb status
```

#### Option B: Using AWS Console
1. Go to Elastic Beanstalk Console
2. Create new application
3. **Important**: Select **Worker** environment tier
4. Choose Python platform
5. Upload application ZIP
6. Configure environment settings

### Step 3: Configure SQS Queue

The worker environment automatically creates an SQS queue, but you can customize it:

1. **Queue Settings:**
   - **Visibility timeout**: 300 seconds (default)
   - **Message retention**: 14 days
   - **Dead letter queue**: Configure for failed messages

2. **Worker Settings:**
   - **HTTP path**: `/` (where messages are sent)
   - **MIME type**: `application/json`
   - **HTTP connections**: Number of concurrent connections

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_SQS_QUEUE_URL` | SQS queue URL | Auto-generated |
| `AWS_SQS_REGION` | AWS region | Environment region |
| `WORKER_CONNECTIONS` | Concurrent connections | 50 |
| `VISIBILITY_TIMEOUT` | Message visibility timeout | 300 |

### Worker Configuration

#### Via EB Console:
1. Go to Configuration → Worker
2. Set HTTP path: `/`
3. Configure MIME type: `application/json`
4. Set connection count: `50`

#### Via .ebextensions:
```yaml
option_settings:
  aws:elasticbeanstalk:sqsd:
    HttpPath: /
    MimeType: application/json
    HttpConnections: 50
    ConnectTimeout: 5
    InactivityTimeout: 299
    VisibilityTimeout: 300
    ErrorVisibilityTimeout: 2
    RetentionPeriod: 345600
```

## 📨 Message Processing

### SQS Message Format

When SQS sends messages to your worker, they arrive as HTTP POST requests:

```json
{
  "Type": "Notification",
  "MessageId": "12345678-1234-1234-1234-123456789012",
  "TopicArn": "arn:aws:sns:us-east-1:123456789012:my-topic",
  "Message": "{\"key\": \"value\", \"data\": \"payload\"}",
  "Timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Processing Logic

```python
def process_message():
    try:
        # Get message from request
        message = request.get_json()
        
        # Extract actual message content
        if 'Message' in message:
            actual_message = json.loads(message['Message'])
        else:
            actual_message = message
        
        # Process based on message type
        if actual_message.get('type') == 'user_signup':
            process_user_signup(actual_message)
        elif actual_message.get('type') == 'order_processing':
            process_order(actual_message)
        else:
            logger.warning(f"Unknown message type: {actual_message}")
        
        return "OK", 200
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        return "Error", 500
```

## 🕐 Scheduled Tasks

### Cron Job Examples

```bash
# Every minute
* * * * * root curl -X POST http://localhost/scheduled

# Every 5 minutes
*/5 * * * * root curl -X POST http://localhost/scheduled

# Daily at 2 AM
0 2 * * * root curl -X POST http://localhost/scheduled

# Weekly on Sunday at 3 AM
0 3 * * 0 root curl -X POST http://localhost/scheduled

# Monthly on 1st at 4 AM
0 4 1 * * root curl -X POST http://localhost/scheduled
```

### Advanced Cron Configuration

```yaml
files:
  "/etc/cron.d/advanced-tasks":
    mode: "000644"
    owner: root
    group: root
    content: |
      # Data cleanup every hour
      0 * * * * root curl -X POST http://localhost/cleanup >> /var/log/cleanup.log 2>&1
      
      # Generate reports daily
      0 6 * * * root curl -X POST http://localhost/reports >> /var/log/reports.log 2>&1
      
      # Database backup weekly
      0 1 * * 0 root curl -X POST http://localhost/backup >> /var/log/backup.log 2>&1

commands:
  01_create_log_files:
    command: |
      touch /var/log/cleanup.log /var/log/reports.log /var/log/backup.log
      chmod 666 /var/log/cleanup.log /var/log/reports.log /var/log/backup.log
```

## 🧪 Testing the Worker Environment

### Local Testing

```python
# test_worker.py
import requests
import json

def test_message_processing():
    """Test message processing endpoint"""
    test_message = {
        "type": "test",
        "data": "Hello Worker!"
    }
    
    response = requests.post('http://localhost:5000/', 
                           json=test_message)
    print(f"Response: {response.status_code} - {response.text}")

def test_scheduled_task():
    """Test scheduled task endpoint"""
    response = requests.post('http://localhost:5000/scheduled')
    print(f"Scheduled task: {response.status_code} - {response.text}")

if __name__ == '__main__':
    test_message_processing()
    test_scheduled_task()
```

### Production Testing

1. **Send test message to SQS:**
   ```bash
   aws sqs send-message \
     --queue-url YOUR_QUEUE_URL \
     --message-body '{"type": "test", "data": "Hello from SQS!"}'
   ```

2. **Check cron job execution:**
   ```bash
   eb ssh
   tail -f /tmp/cronlog.txt
   ```

3. **Monitor worker metrics:**
   - Check CloudWatch metrics
   - Monitor SQS queue depth
   - Review application logs

## 📊 Monitoring & Scaling

### Key Metrics

- **Queue Depth**: Number of messages in SQS queue
- **Processing Rate**: Messages processed per minute
- **Error Rate**: Failed message processing percentage
- **Response Time**: Average processing time per message

### Auto Scaling Configuration

```yaml
option_settings:
  aws:autoscaling:asg:
    MinSize: 1
    MaxSize: 10
  aws:autoscaling:trigger:
    MeasureName: QueueDepth
    Unit: Count
    UpperThreshold: 100
    LowerThreshold: 10
    ScaleUpIncrement: 2
    ScaleDownIncrement: -1
```

### CloudWatch Alarms

```bash
# High queue depth alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "High-SQS-Queue-Depth" \
  --alarm-description "SQS queue depth is high" \
  --metric-name ApproximateNumberOfVisibleMessages \
  --namespace AWS/SQS \
  --statistic Average \
  --period 300 \
  --threshold 1000 \
  --comparison-operator GreaterThanThreshold
```

## 🎯 Lab Exercises

### Exercise 1: Basic Worker Deployment
1. Deploy the worker environment
2. Send test messages to SQS queue
3. Verify message processing in logs
4. Check cron job execution

### Exercise 2: Custom Message Processing
1. Modify the message processing logic
2. Add different message types
3. Implement error handling
4. Test with various message formats

### Exercise 3: Scheduled Task Implementation
1. Create custom scheduled tasks
2. Configure different cron schedules
3. Implement task logging
4. Monitor task execution

### Exercise 4: Scaling Configuration
1. Configure auto-scaling based on queue depth
2. Load test with multiple messages
3. Monitor scaling behavior
4. Optimize scaling parameters

## 🔍 Troubleshooting

### Common Issues

#### Issue 1: Messages Not Processing
**Symptoms**: Messages remain in SQS queue
**Solutions**:
- Check worker application logs
- Verify HTTP endpoint configuration
- Ensure application returns 200 status

#### Issue 2: Cron Jobs Not Running
**Symptoms**: Scheduled tasks don't execute
**Solutions**:
- Check cron service status
- Verify cron file permissions
- Review cron syntax

#### Issue 3: High Error Rate
**Symptoms**: Many failed message processing attempts
**Solutions**:
- Implement proper error handling
- Configure dead letter queue
- Add retry logic

### Debugging Commands

```bash
# Check worker status
eb status

# View application logs
eb logs

# SSH and check cron
eb ssh
sudo service crond status
sudo crontab -l
```

## 📚 Key Concepts Learned

- **Worker Environments**: Background processing architecture
- **SQS Integration**: Message queue processing
- **Cron Jobs**: Scheduled task automation
- **Auto Scaling**: Queue-based scaling strategies
- **Error Handling**: Robust message processing
- **Monitoring**: Worker environment observability

## 🔐 Security Best Practices

- **IAM Roles**: Use instance profiles for SQS access
- **Message Encryption**: Enable SQS encryption
- **Network Security**: Restrict worker environment access
- **Logging**: Secure log handling
- **Error Messages**: Don't expose sensitive information

## ➡️ Next Steps

Ready for advanced applications? Continue to [Module 5: Advanced E-commerce Application](../05-ecommerce-advanced/README.md) to learn about:
- Full-stack application architecture
- User authentication and authorization
- Database design and optimization
- Production deployment strategies

---

**Outstanding!** You've mastered worker environments and background processing. You now understand how to build scalable, decoupled architectures that can handle both real-time and batch processing workloads.