# Module 3: Containerized Applications with Docker

**Duration:** 30 minutes  
**Difficulty:** Intermediate

## 🎯 Learning Objectives

In this module, you will:
- Understand containerization concepts and benefits
- Create and configure Dockerfiles for Elastic Beanstalk
- Deploy containerized Python Flask applications
- Configure container-specific settings
- Implement blue-green deployments with containers
- Monitor containerized applications

## 📖 Containerization Overview

Containerization packages your application with all its dependencies into a lightweight, portable container. Benefits include:

- **Consistency**: Same environment across development, testing, and production
- **Portability**: Run anywhere Docker is supported
- **Isolation**: Applications don't interfere with each other
- **Scalability**: Easy to scale individual components
- **Efficiency**: Better resource utilization than VMs

## 🏗️ Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Developer     │    │  Elastic         │    │   Docker        │
│                 │───▶│  Beanstalk       │───▶│   Container     │
│ (Dockerfile +   │    │  Environment     │    │   (Your App)    │
│  Application)   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                         │
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Application    │    │   Container     │
                       │  Load Balancer   │    │   Registry      │
                       └──────────────────┘    └─────────────────┘
```

## 📁 Application Structure

```
03-containerized-app/
├── README.md           # This file
├── application.py      # Flask application
├── Dockerfile         # Container configuration
├── app.zip           # Deployment package
└── Archive.zip       # Backup deployment package
```

## 🐳 Dockerfile Explained

```dockerfile
# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=application.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "application.py"]
```

## 🚀 Application Code

The Flask application (`application.py`) demonstrates:
- **Dynamic content**: Personalized greetings
- **Background styling**: CSS with background images
- **Routing**: Multiple URL patterns
- **Error handling**: Graceful error responses

### Key Features:
- **Welcome page**: Customizable greeting
- **Dynamic routing**: URL parameters
- **Visual design**: Background images and styling
- **Production ready**: WSGI application object

## 🔧 Deployment Instructions

### Step 1: Prepare Application

1. **Review application files:**
   ```bash
   ls -la
   # application.py - Flask app
   # Dockerfile - Container config
   ```

2. **Test locally (optional):**
   ```bash
   # Build Docker image
   docker build -t my-flask-app .
   
   # Run container
   docker run -p 5000:5000 my-flask-app
   
   # Test in browser
   curl http://localhost:5000
   ```

### Step 2: Deploy to Elastic Beanstalk

#### Option A: Using EB CLI
```bash
# Initialize EB application
eb init -p docker

# Create environment
eb create production

# Deploy application
eb deploy

# Open in browser
eb open
```

#### Option B: Using AWS Console
1. Go to Elastic Beanstalk Console
2. Create new application
3. Choose **Docker** platform
4. Upload ZIP file containing:
   - `application.py`
   - `Dockerfile`
5. Deploy and test

### Step 3: Verify Deployment

1. **Access application**: Use provided EB URL
2. **Test routes**:
   - `/` - Welcome page
   - `/yourname` - Personalized greeting
3. **Check logs**: Monitor container startup

## 🎨 Application Features

### Dynamic Greetings
- **Default route** (`/`): Shows welcome message
- **Named route** (`/<username>`): Personalized greeting
- **Styling**: Background images and custom CSS

### Container Benefits
- **Fast startup**: Optimized container layers
- **Consistent environment**: Same runtime everywhere
- **Easy scaling**: Container orchestration ready
- **Resource efficiency**: Minimal overhead

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_APP` | Flask application file | `application.py` |
| `FLASK_ENV` | Flask environment | `production` |
| `PORT` | Application port | `5000` |

### Container Configuration

#### Dockerfile Best Practices:
- **Multi-stage builds**: Reduce image size
- **Layer caching**: Order commands for optimal caching
- **Security**: Use non-root user
- **Health checks**: Add container health checks

#### Example Enhanced Dockerfile:
```dockerfile
FROM python:3.9-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "application.py"]
```

## 🧪 Testing Strategies

### Local Testing
```bash
# Build and test locally
docker build -t flask-app .
docker run -p 5000:5000 flask-app

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/student
```

### Production Testing
1. **Functionality**: Test all routes
2. **Performance**: Load testing
3. **Monitoring**: Check container metrics
4. **Logs**: Verify logging works

## 📊 Monitoring Containerized Applications

### Container Metrics
- **CPU usage**: Monitor container CPU
- **Memory usage**: Track memory consumption
- **Network I/O**: Monitor network traffic
- **Disk I/O**: Track storage usage

### Application Logs
```bash
# View logs
eb logs

# Stream logs
eb logs --all
```

### Health Monitoring
- **Container health**: Docker health checks
- **Application health**: EB health monitoring
- **Custom metrics**: CloudWatch custom metrics

## 🔄 Blue-Green Deployments

### Benefits:
- **Zero downtime**: Seamless deployments
- **Easy rollback**: Quick revert capability
- **Testing**: Validate before switching traffic

### Implementation:
```bash
# Deploy to staging environment
eb create staging

# Test staging environment
# ... run tests ...

# Swap environments (blue-green)
eb swap staging production
```

## 🎯 Lab Exercises

### Exercise 1: Basic Container Deployment
1. Deploy the provided Flask application
2. Test both routes (`/` and `/yourname`)
3. Verify container is running correctly
4. Check application logs

### Exercise 2: Container Customization
1. Modify the Flask application
2. Update the Dockerfile
3. Rebuild and redeploy
4. Test the changes

### Exercise 3: Blue-Green Deployment
1. Create a staging environment
2. Deploy updated application to staging
3. Test staging environment
4. Perform blue-green swap

## 🔍 Troubleshooting

### Common Issues

#### Issue 1: Container Won't Start
**Symptoms**: Application fails to deploy
**Solutions**:
- Check Dockerfile syntax
- Verify base image availability
- Review application logs

#### Issue 2: Port Configuration
**Symptoms**: Application not accessible
**Solutions**:
- Ensure EXPOSE directive in Dockerfile
- Check application binds to 0.0.0.0
- Verify port environment variable

#### Issue 3: Build Failures
**Symptoms**: Docker build fails
**Solutions**:
- Check dependency versions
- Verify file paths in Dockerfile
- Review build context

### Debugging Commands
```bash
# Check container status
eb status

# View detailed logs
eb logs --all

# SSH into instance (if enabled)
eb ssh
```

## 📚 Key Concepts Learned

- **Containerization**: Packaging applications with dependencies
- **Docker**: Container platform and tooling
- **Dockerfile**: Container build instructions
- **Container orchestration**: Managing containerized applications
- **Blue-green deployments**: Zero-downtime deployment strategy
- **Container monitoring**: Tracking container performance

## 🔐 Security Considerations

### Container Security:
- **Base images**: Use official, minimal images
- **User privileges**: Run as non-root user
- **Secrets management**: Use environment variables
- **Image scanning**: Scan for vulnerabilities
- **Network security**: Limit container network access

### Best Practices:
- Regular image updates
- Minimal attack surface
- Secure secrets handling
- Network segmentation
- Access controls

## ➡️ Next Steps

Ready for background processing? Continue to [Module 4: Worker Environments](../04-worker-environment/README.md) to learn about:
- SQS message processing
- Background job handling
- Cron job scheduling
- Worker environment configuration

---

**Excellent work!** You've successfully containerized and deployed a Python application. You now understand how containers provide consistency, portability, and scalability for your applications.