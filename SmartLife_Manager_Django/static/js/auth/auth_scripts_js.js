// ===== NAVIGATION FUNCTIONS =====
function goToRegister() {
    // Dalam implementasi nyata, ini akan redirect ke halaman register
    window.location.href = 'register_page.html';
    // Untuk demo: alert('Redirect to register page');
}

function goToLogin() {
    // Dalam implementasi nyata, ini akan redirect ke halaman login
    window.location.href = 'login_page.html';
    // Untuk demo: alert('Redirect to login page');
}

// ===== PASSWORD STRENGTH CHECKER =====
function checkPasswordStrength(password) {
    let strength = 0;
    let text = '';
    let className = '';

    // Check password criteria
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/)) strength++;
    if (password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;

    // Determine strength level
    switch (strength) {
        case 0:
        case 1:
            text = 'Very Weak';
            className = 'strength-weak';
            break;
        case 2:
            text = 'Weak';
            className = 'strength-weak';
            break;
        case 3:
            text = 'Fair';
            className = 'strength-fair';
            break;
        case 4:
            text = 'Good';
            className = 'strength-good';
            break;
        case 5:
            text = 'Strong';
            className = 'strength-strong';
            break;
    }

    return { text, className };
}

// ===== FORM VALIDATION FUNCTIONS =====
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateUsername(username) {
    // Username should be 3-20 characters, alphanumeric and underscore only
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    return usernameRegex.test(username);
}

function validatePassword(password) {
    // Password should be at least 8 characters
    return password.length >= 8;
}

// ===== FORM INPUT HANDLERS =====
function setupFormInputHandlers() {
    // Add floating animation to form inputs
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
}

// ===== RIPPLE EFFECT =====
function setupRippleEffect() {
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            let ripple = document.createElement('span');
            let rect = this.getBoundingClientRect();
            let size = Math.max(rect.width, rect.height);
            let x = e.clientX - rect.left - size / 2;
            let y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// ===== LOGIN PAGE FUNCTIONS =====
function setupLoginPage() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.querySelector('#loginForm input[type="text"]').value;
            const password = document.querySelector('#loginForm input[type="password"]').value;
            
            // Basic validation
            if (!username || !password) {
                showAlert('Please fill in all fields', 'error');
                return;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading-spinner"></span> Logging in...';
            submitBtn.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Show success message
                showAlert('Login successful!', 'success');
                
                // In real implementation, redirect to dashboard
                // window.location.href = 'dashboard.html';
            }, 2000);
        });
    }
}

// ===== REGISTER PAGE FUNCTIONS =====
function setupRegisterPage() {
    const registerForm = document.getElementById('registerForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    
    if (registerForm) {
        // Password strength checker
        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                const password = this.value;
                const strengthResult = checkPasswordStrength(password);
                
                const strengthText = document.getElementById('strength-text');
                const strengthFill = document.getElementById('strength-fill');
                
                if (strengthText && strengthFill) {
                    strengthText.textContent = strengthResult.text;
                    strengthFill.className = 'strength-fill ' + strengthResult.className;
                }
            });
        }
        
        // Confirm password checker
        if (confirmPasswordInput) {
            confirmPasswordInput.addEventListener('input', function() {
                const password = passwordInput.value;
                const confirmPassword = this.value;
                const matchDiv = document.getElementById('password-match');
                
                if (matchDiv) {
                    if (confirmPassword === '') {
                        matchDiv.textContent = '';
                        this.classList.remove('is-valid', 'is-invalid');
                    } else if (password === confirmPassword) {
                        matchDiv.textContent = '✓ Passwords match';
                        matchDiv.style.color = '#198754';
                        this.classList.remove('is-invalid');
                        this.classList.add('is-valid');
                    } else {
                        matchDiv.textContent = '✗ Passwords do not match';
                        matchDiv.style.color = '#dc3545';
                        this.classList.remove('is-valid');
                        this.classList.add('is-invalid');
                    }
                }
            });
        }
        
        // Form submission
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;
            const termsAccepted = document.getElementById('termsCheck').checked;
            
            // Validation
            let isValid = true;
            
            if (!validateUsername(username)) {
                showFieldError('username', 'Username must be 3-20 characters, alphanumeric and underscore only');
                isValid = false;
            } else {
                clearFieldError('username');
            }
            
            if (!validateEmail(email)) {
                showFieldError('email', 'Please enter a valid email address');
                isValid = false;
            } else {
                clearFieldError('email');
            }
            
            if (!validatePassword(password)) {
                showFieldError('password', 'Password must be at least 8 characters long');
                isValid = false;
            } else {
                clearFieldError('password');
            }
            
            if (password !== confirmPassword) {
                showFieldError('confirmPassword', 'Passwords do not match');
                isValid = false;
            } else {
                clearFieldError('confirmPassword');
            }
            
            if (!termsAccepted) {
                showAlert('Please accept the terms and conditions', 'error');
                isValid = false;
            }
            
            if (!isValid) {
                return;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading-spinner"></span> Creating Account...';
            submitBtn.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Show success message
                showAlert('Registration successful! Please check your email to verify your account.', 'success');
                
                // In real implementation, redirect to login or verification page
                // window.location.href = 'login.html';
            }, 2000);
        });
    }
}

// ===== FIELD VALIDATION HELPERS =====
function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        
        // Remove existing error message
        const existingError = field.parentElement.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        field.parentElement.appendChild(errorDiv);
    }
}

function clearFieldError(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        
        // Remove error message
        const existingError = field.parentElement.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
    }
}

// ===== ALERT SYSTEM =====
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlert = document.querySelector('.custom-alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `custom-alert alert-${type}`;
    alert.innerHTML = `
        <div class="alert-content">
            <span class="alert-icon">${getAlertIcon(type)}</span>
            <span class="alert-message">${message}</span>
            <button class="alert-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    // Add styles
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        padding: 15px 20px;
        z-index: 9999;
        animation: slideInRight 0.3s ease-out;
        max-width: 400px;
        border-left: 4px solid ${getAlertColor(type)};
    `;
    
    // Add to page
    document.body.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentElement) {
            alert.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (alert.parentElement) {
                    alert.remove();
                }
            }, 300);
        }
    }, 5000);
}

function getAlertIcon(type) {
    switch (type) {
        case 'success': return '✓';
        case 'error': return '✗';
        case 'warning': return '⚠';
        default: return 'ℹ';
    }
}

function getAlertColor(type) {
    switch (type) {
        case 'success': return '#198754';
        case 'error': return '#dc3545';
        case 'warning': return '#ffc107';
        default: return '#0dcaf0';
    }
}

// ===== SOCIAL LOGIN HANDLERS =====
function setupSocialLogin() {
    document.querySelectorAll('.social-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const platform = this.classList[1]; // google, facebook, etc.
            showAlert(`${platform.charAt(0).toUpperCase() + platform.slice(1)} login clicked!`, 'info');
            
            // In real implementation, redirect to OAuth provider
            // window.location.href = `auth/${platform}`;
        });
    });
}

// =====