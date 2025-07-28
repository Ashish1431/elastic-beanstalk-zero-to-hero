// TechStore JavaScript

// Cart functionality
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(productId) {
    // Get product details (in a real app, this would come from the server)
    const products = [
        { id: 1, name: 'Wireless Headphones', price: 99.99 },
        { id: 2, name: 'Smart Watch', price: 199.99 },
        { id: 3, name: 'Laptop', price: 899.99 },
        { id: 4, name: 'Smartphone', price: 699.99 }
    ];
    
    const product = products.find(p => p.id === productId);
    
    if (product) {
        const existingItem = cart.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                id: product.id,
                name: product.name,
                price: product.price,
                quantity: 1
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        showNotification('Product added to cart!', 'success');
        updateCartBadge();
    }
}

function updateCartBadge() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    // You can add a cart badge to the navbar if needed
    console.log(`Cart has ${totalItems} items`);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// Newsletter subscription
function subscribeNewsletter() {
    const email = document.getElementById('newsletter-email').value;
    
    if (!email || !isValidEmail(email)) {
        showNotification('Please enter a valid email address.', 'danger');
        return;
    }
    
    // In a real app, this would send the email to the server
    showNotification('Thank you for subscribing to our newsletter!', 'success');
    document.getElementById('newsletter-email').value = '';
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// User list functionality
function showUserList() {
    const modal = new bootstrap.Modal(document.getElementById('userListModal'));
    modal.show();
    
    // Fetch users from the API
    fetch('/api/users')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch users');
            }
            return response.json();
        })
        .then(users => {
            displayUsers(users);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('userListContent').innerHTML = `
                <div class="alert alert-danger">
                    Failed to load users. Please try again.
                </div>
            `;
        });
}

function displayUsers(users) {
    const content = document.getElementById('userListContent');
    
    if (users.length === 0) {
        content.innerHTML = '<p class="text-muted text-center">No users found.</p>';
        return;
    }
    
    const userList = users.map(user => `
        <div class="user-item">
            <div class="row align-items-center">
                <div class="col-md-4">
                    <strong>${user.name}</strong>
                </div>
                <div class="col-md-4">
                    <span class="text-muted">${user.email}</span>
                </div>
                <div class="col-md-4 text-end">
                    <small class="text-muted">Joined: ${new Date(user.created_at).toLocaleDateString()}</small>
                </div>
            </div>
        </div>
    `).join('');
    
    content.innerHTML = userList;
}

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Initialize cart badge
    updateCartBadge();
    
    // Add loading animation to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('btn-close')) {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            }
        });
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields.', 'danger');
            }
        });
    });
});

// Product search functionality (placeholder)
function searchProducts(query) {
    // In a real app, this would search through products
    console.log('Searching for:', query);
    showNotification(`Searching for "${query}"...`, 'info');
}

// Add to wishlist functionality (placeholder)
function addToWishlist(productId) {
    showNotification('Product added to wishlist!', 'success');
}

// Share product functionality (placeholder)
function shareProduct(productId) {
    if (navigator.share) {
        navigator.share({
            title: 'Check out this product on TechStore',
            url: window.location.href
        });
    } else {
        // Fallback for browsers that don't support Web Share API
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            showNotification('Product link copied to clipboard!', 'success');
        });
    }
}

// Theme toggle functionality (placeholder)
function toggleTheme() {
    const body = document.body;
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
}); 