# Module 6: Deployment Strategies & Best Practices

**Duration:** 45 minutes  
**Difficulty:** Advanced

## 🎯 Learning Objectives

In this module, you will:
- Master different deployment strategies (rolling, blue-green, immutable)
- Implement CI/CD pipelines with Elastic Beanstalk
- Configure advanced monitoring and alerting
- Optimize application performance and costs
- Implement disaster recovery strategies
- Apply production security best practices

## 📖 Deployment Strategies Overview

Elastic Beanstalk supports multiple deployment strategies, each with different trade-offs:

| Strategy | Downtime | Risk | Speed | Cost |
|----------|----------|------|-------|------|
| **All at Once** | Yes | High | Fast | Low |
| **Rolling** | No | Medium | Medium | Low |
| **Rolling with Additional Batch** | No | Low | Medium | Medium |
| **Immutable** | No | Very Low | Slow | High |
| **Blue/Green** | No | Very Low | Fast | High |

## 🏗️ Architecture Patterns

### 1. Rolling Deployment
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Instance 1  │    │ Instance 2  │    │ Instance 3  │
│   v1.0      │───▶│   v2.0      │───▶│   v2.0      │
│             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
     Step 1             Step 2             Step 3
```

### 2. Blue-Green Deployment
```
┌─────────────────┐         ┌─────────────────┐
│  Blue Environment│         │ Green Environment│
│     (v1.0)      │◀───────▶│     (v2.0)      │
│                 │  Swap   │                 │
└─────────────────┘         └─────────────────┘
```

### 3. Immutable Deployment
```
┌─────────────────┐         ┌─────────────────┐
│ Current ASG     │         │   New ASG       │
│   (v1.0)        │         │   (v2.0)        │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
        │                           │
        └───────── Replace ─────────┘
```

## 📁 Module Structure

```
06-deployment-strategies/
├── README.md                    # This file
├── deployment-configs/          # Deployment configurations
│   ├── rolling-deployment.yaml
│   ├── blue-green-config.yaml
│   └── immutable-config.yaml
├── ci-cd/                      # CI/CD pipeline configs
│   ├── buildspec.yml           # CodeBuild specification
│   ├── pipeline.yaml           # CodePipeline template
│   └── deploy-script.sh        # Deployment script
├── monitoring/                 # Monitoring configurations
│   ├── cloudwatch-dashboard.json
│   ├── alarms.yaml
│   └── custom-metrics.py
├── security/                   # Security configurations
│   ├── security-groups.yaml
│   ├── iam-policies.json
│   └── ssl-config.yaml
└── examples/                   # Example applications
    ├── sample-app/
    └── load-test/
```

## 🚀 Deployment Strategy Deep Dive

### 1. Rolling Deployment

**Best for**: Most applications, balanced approach

**Configuration:**
```yaml
option_settings:
  aws:elasticbeanstalk:command:
    DeploymentPolicy: Rolling
    BatchSizeType: Percentage
    BatchSize: 30
    Timeout: 600
  aws:autoscaling:updatepolicy:rollingupdate:
    RollingUpdateEnabled: true
    MaxBatchSize: 1
    MinInstancesInService: 1
    RollingUpdateType: Health
    Timeout: PT30M
```

**Pros:**
- No additional cost
- Gradual deployment
- Easy rollback

**Cons:**
- Temporary capacity reduction
- Mixed versions during deployment

### 2. Rolling with Additional Batch

**Best for**: Applications that can't afford capacity reduction

**Configuration:**
```yaml
option_settings:
  aws:elasticbeanstalk:command:
    DeploymentPolicy: RollingWithAdditionalBatch
    BatchSizeType: Fixed
    BatchSize: 2
```

**Pros:**
- Maintains full capacity
- Gradual deployment
- Better for high-traffic apps

**Cons:**
- Temporary additional cost
- Slightly more complex

### 3. Immutable Deployment

**Best for**: Critical applications requiring maximum safety

**Configuration:**
```yaml
option_settings:
  aws:elasticbeanstalk:command:
    DeploymentPolicy: Immutable
    HealthCheckSuccessThreshold: Ok
    IgnoreHealthCheck: false
    Timeout: 900
```

**Pros:**
- Zero risk to existing environment
- Quick rollback
- Full validation before switch

**Cons:**
- Highest cost (double resources)
- Longer deployment time

### 4. Blue-Green Deployment

**Best for**: Applications requiring zero downtime and instant rollback

**Implementation:**
```bash
# Create green environment
eb create green-env --cname myapp-green

# Deploy to green environment
eb deploy green-env

# Test green environment
curl https://myapp-green.region.elasticbeanstalk.com

# Swap environments
eb swap blue-env green-env
```

**Pros:**
- Zero downtime
- Instant rollback
- Full testing before switch

**Cons:**
- Highest cost
- DNS propagation delay
- Complex database migrations

## 🔄 CI/CD Pipeline Implementation

### CodePipeline Configuration

```yaml
# pipeline.yaml
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      RoleArn: !GetAtt CodePipelineRole.Arn
      Stages:
        - Name: Source
          Actions:
            - Name: SourceAction
              ActionTypeId:
                Category: Source
                Owner: ThirdParty
                Provider: GitHub
                Version: '1'
              Configuration:
                Owner: !Ref GitHubOwner
                Repo: !Ref GitHubRepo
                Branch: !Ref GitHubBranch
                OAuthToken: !Ref GitHubToken
              OutputArtifacts:
                - Name: SourceOutput
        
        - Name: Build
          Actions:
            - Name: BuildAction
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: '1'
              Configuration:
                ProjectName: !Ref CodeBuildProject
              InputArtifacts:
                - Name: SourceOutput
              OutputArtifacts:
                - Name: BuildOutput
        
        - Name: Deploy
          Actions:
            - Name: DeployAction
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: ElasticBeanstalk
                Version: '1'
              Configuration:
                ApplicationName: !Ref EBApplication
                EnvironmentName: !Ref EBEnvironment
              InputArtifacts:
                - Name: BuildOutput
```

### CodeBuild Specification

```yaml
# buildspec.yml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.8
    commands:
      - echo Installing dependencies...
      - pip install -r requirements.txt
  
  pre_build:
    commands:
      - echo Running tests...
      - python -m pytest tests/
      - echo Running security scan...
      - bandit -r . -f json -o security-report.json
  
  build:
    commands:
      - echo Building application...
      - zip -r application.zip . -x "*.git*" "tests/*" "*.pyc"
  
  post_build:
    commands:
      - echo Build completed on `date`

artifacts:
  files:
    - application.zip
    - .ebextensions/**/*
  name: myapp-$(date +%Y-%m-%d)
```

## 📊 Advanced Monitoring

### CloudWatch Dashboard

```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ElasticBeanstalk", "ApplicationRequests2xx", "EnvironmentName", "production"],
          [".", "ApplicationRequests4xx", ".", "."],
          [".", "ApplicationRequests5xx", ".", "."]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "HTTP Response Codes"
      }
    },
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ElasticBeanstalk", "ApplicationLatencyP99", "EnvironmentName", "production"],
          [".", "ApplicationLatencyP95", ".", "."],
          [".", "ApplicationLatencyP90", ".", "."]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Application Latency"
      }
    }
  ]
}
```

### Custom Metrics

```python
# custom-metrics.py
import boto3
import psutil
import time

cloudwatch = boto3.client('cloudwatch')

def publish_custom_metrics():
    """Publish custom application metrics"""
    
    # CPU usage
    cpu_percent = psutil.cpu_percent()
    
    # Memory usage
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    
    # Disk usage
    disk = psutil.disk_usage('/')
    disk_percent = (disk.used / disk.total) * 100
    
    # Publish metrics
    cloudwatch.put_metric_data(
        Namespace='CustomApp/System',
        MetricData=[
            {
                'MetricName': 'CPUUtilization',
                'Value': cpu_percent,
                'Unit': 'Percent'
            },
            {
                'MetricName': 'MemoryUtilization',
                'Value': memory_percent,
                'Unit': 'Percent'
            },
            {
                'MetricName': 'DiskUtilization',
                'Value': disk_percent,
                'Unit': 'Percent'
            }
        ]
    )

if __name__ == '__main__':
    while True:
        publish_custom_metrics()
        time.sleep(60)  # Publish every minute
```

### Alerting Configuration

```yaml
# alarms.yaml
Resources:
  HighErrorRateAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: HighErrorRate
      AlarmDescription: High error rate detected
      MetricName: ApplicationRequests5xx
      Namespace: AWS/ElasticBeanstalk
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref SNSTopic
  
  HighLatencyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: HighLatency
      AlarmDescription: High application latency
      MetricName: ApplicationLatencyP95
      Namespace: AWS/ElasticBeanstalk
      Statistic: Average
      Period: 300
      EvaluationPeriods: 3
      Threshold: 2000
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref SNSTopic
```

## 🔒 Security Best Practices

### SSL/TLS Configuration

```yaml
# ssl-config.yaml
option_settings:
  aws:elb:listener:443:
    ListenerProtocol: HTTPS
    InstancePort: 80
    InstanceProtocol: HTTP
    SSLCertificateId: arn:aws:acm:region:account:certificate/certificate-id
  
  aws:elb:policies:
    SSLReferencePolicy: ELBSecurityPolicy-TLS-1-2-2017-01
  
  aws:elb:listener:80:
    ListenerEnabled: false  # Disable HTTP, force HTTPS
```

### Security Groups

```yaml
# security-groups.yaml
Resources:
  WebServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for web servers
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref LoadBalancerSecurityGroup
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          SourceSecurityGroupId: !Ref LoadBalancerSecurityGroup
  
  LoadBalancerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for load balancer
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
```

### IAM Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": [
        "arn:aws:dynamodb:*:*:table/MyAppTable",
        "arn:aws:dynamodb:*:*:table/MyAppTable/index/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-app-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🎯 Performance Optimization

### Auto Scaling Configuration

```yaml
option_settings:
  aws:autoscaling:asg:
    MinSize: 2
    MaxSize: 10
    Cooldown: 300
  
  aws:autoscaling:trigger:
    MeasureName: CPUUtilization
    Unit: Percent
    UpperThreshold: 70
    LowerThreshold: 20
    ScaleUpIncrement: 2
    ScaleDownIncrement: -1
    BreachDuration: 300
    Period: 60
```

### Load Balancer Optimization

```yaml
option_settings:
  aws:elb:loadbalancer:
    CrossZone: true
    ConnectionDrainingEnabled: true
    ConnectionDrainingTimeout: 20
  
  aws:elb:healthcheck:
    HealthyThreshold: 3
    Interval: 30
    Timeout: 5
    UnhealthyThreshold: 5
    Target: HTTP:80/health
```

## 🧪 Testing Strategies

### Load Testing

```python
# load-test.py
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def load_test(url, num_requests=1000, num_threads=10):
    """Perform load testing on the application"""
    
    def make_request():
        try:
            response = requests.get(url, timeout=10)
            return response.status_code
        except Exception as e:
            return str(e)
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        results = [future.result() for future in futures]
    
    end_time = time.time()
    
    # Analyze results
    success_count = sum(1 for r in results if r == 200)
    error_count = len(results) - success_count
    duration = end_time - start_time
    
    print(f"Load Test Results:")
    print(f"Total Requests: {num_requests}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Requests/second: {num_requests/duration:.2f}")

if __name__ == '__main__':
    load_test('https://your-app.elasticbeanstalk.com')
```

### Health Check Implementation

```python
# health.py
from flask import Flask, jsonify
import psutil
import boto3

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Comprehensive health check endpoint"""
    
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'checks': {}
    }
    
    # Check system resources
    health_status['checks']['cpu'] = psutil.cpu_percent() < 80
    health_status['checks']['memory'] = psutil.virtual_memory().percent < 80
    health_status['checks']['disk'] = psutil.disk_usage('/').percent < 80
    
    # Check database connectivity
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('your-table')
        table.load()
        health_status['checks']['database'] = True
    except:
        health_status['checks']['database'] = False
    
    # Overall health
    if all(health_status['checks'].values()):
        return jsonify(health_status), 200
    else:
        health_status['status'] = 'unhealthy'
        return jsonify(health_status), 503
```

## 🎯 Lab Exercises

### Exercise 1: Deployment Strategy Comparison
1. Deploy the same application using different strategies
2. Measure deployment time and downtime
3. Compare resource usage and costs
4. Document pros and cons of each approach

### Exercise 2: CI/CD Pipeline Setup
1. Set up CodePipeline with GitHub integration
2. Configure automated testing and deployment
3. Implement approval gates for production
4. Test the entire pipeline end-to-end

### Exercise 3: Advanced Monitoring
1. Create custom CloudWatch dashboard
2. Set up comprehensive alerting
3. Implement custom metrics collection
4. Test alert notifications

### Exercise 4: Security Hardening
1. Implement SSL/TLS termination
2. Configure security groups properly
3. Set up WAF rules
4. Audit IAM permissions

## 🔍 Troubleshooting Guide

### Common Deployment Issues

#### Issue 1: Deployment Timeout
**Symptoms**: Deployment fails with timeout error
**Solutions**:
- Increase deployment timeout
- Check application startup time
- Verify health check endpoint
- Review instance capacity

#### Issue 2: Health Check Failures
**Symptoms**: Instances marked as unhealthy
**Solutions**:
- Verify health check URL
- Check application logs
- Ensure proper response codes
- Adjust health check parameters

#### Issue 3: Auto Scaling Issues
**Symptoms**: Instances not scaling properly
**Solutions**:
- Review scaling triggers
- Check CloudWatch metrics
- Verify scaling policies
- Monitor cooldown periods

### Monitoring and Debugging

```bash
# Check environment health
eb health

# View detailed logs
eb logs --all

# Monitor real-time logs
eb logs --stream

# Check configuration
eb config

# View environment info
eb status --verbose
```

## 📚 Key Concepts Mastered

- **Deployment Strategies**: Rolling, blue-green, immutable deployments
- **CI/CD Pipelines**: Automated testing and deployment
- **Advanced Monitoring**: Custom metrics and alerting
- **Security Hardening**: SSL, security groups, IAM policies
- **Performance Optimization**: Auto scaling and load balancing
- **Troubleshooting**: Systematic problem resolution

## 🏆 Course Completion

Congratulations! You've completed the AWS Elastic Beanstalk Zero to Hero course. You now have:

- **Foundational Knowledge**: Understanding of EB concepts and architecture
- **Practical Skills**: Hands-on experience with multiple deployment scenarios
- **Advanced Techniques**: Production-ready deployment strategies
- **Best Practices**: Security, monitoring, and optimization knowledge
- **Troubleshooting Skills**: Ability to diagnose and resolve issues

## 🎓 Next Steps

### Certification Preparation
- AWS Certified Developer - Associate
- AWS Certified Solutions Architect - Associate
- AWS Certified DevOps Engineer - Professional

### Advanced Topics
- **Container Orchestration**: ECS, EKS integration
- **Serverless**: Lambda integration patterns
- **Multi-Region**: Global deployment strategies
- **Cost Optimization**: Advanced cost management

### Community Engagement
- Share your projects and learnings
- Contribute to open-source projects
- Join AWS community forums
- Attend AWS events and meetups

---

**🎉 Congratulations!** You've mastered AWS Elastic Beanstalk from zero to hero. You're now equipped to build, deploy, and manage production-ready applications with confidence!