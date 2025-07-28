// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

// Initialize page functionality
function initializePage() {
    updateTimestamp();
    detectRegion();
    addEventListeners();
}

// Update timestamp
function updateTimestamp() {
    const timestampElement = document.getElementById('timestamp');
    const now = new Date();
    timestampElement.textContent = now.toLocaleString();
}

// Detect AWS region (simplified for demo)
function detectRegion() {
    const regionElement = document.getElementById('region');
    // In a real application, you might get this from environment variables
    // For demo purposes, we'll use a placeholder
    regionElement.textContent = 'us-east-1 (Demo)';
}

// Add event listeners
function addEventListeners() {
    // Update timestamp every minute
    setInterval(updateTimestamp, 60000);
}

// Show alert function
function showAlert() {
    alert('🎉 Congratulations! JavaScript is working perfectly in your Elastic Beanstalk application!');
}

// Toggle theme function
function changeTheme() {
    const body = document.body;
    body.classList.toggle('dark-theme');
    
    const isDark = body.classList.contains('dark-theme');
    localStorage.setItem('darkTheme', isDark);
    
    // Show notification
    showNotification(isDark ? 'Dark theme enabled' : 'Light theme enabled');
}

// Show more info function
function showInfo() {
    const info = `
🚀 AWS Elastic Beanstalk Application Info:

📊 Current Status: Running
🌐 Platform: Node.js
⚡ Load Balancer: Active
📈 Auto Scaling: Enabled
🔍 Health Monitoring: Active
📝 Logging: CloudWatch Integration

🎯 This is Module 1 of the Elastic Beanstalk Zero to Hero course.

Next: Try Module 2 for database integration!
    `;
    
    alert(info);
}

// Show notification function
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Add animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Load saved theme preference
function loadThemePreference() {
    const savedTheme = localStorage.getItem('darkTheme');
    if (savedTheme === 'true') {
        document.body.classList.add('dark-theme');
    }
}

// Load theme preference on page load
loadThemePreference();

// Add some interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add click effects to info items
    const infoItems = document.querySelectorAll('.info-item');
    infoItems.forEach(item => {
        item.addEventListener('click', function() {
            this.style.background = '#e3f2fd';
            setTimeout(() => {
                this.style.background = '#f8f9fa';
            }, 200);
        });
    });
});

// Console welcome message
console.log(`
🚀 Welcome to AWS Elastic Beanstalk!
📚 Module 1: Introduction
🎯 Learning Objective: First deployment success!

Check out the other modules to learn more advanced features:
- Module 2: Node.js with DynamoDB
- Module 3: Containerized Applications  
- Module 4: Worker Environments
- Module 5: Advanced E-commerce App
`);

// Performance monitoring (basic)
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`⚡ Page loaded in ${Math.round(loadTime)}ms`);
});