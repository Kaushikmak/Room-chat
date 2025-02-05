// Add this to a separate JS file
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss messages after 5 seconds
    const messages = document.querySelectorAll('.messages li');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
});


// feed
// Optional: Add fade-in animation when new items are loaded
document.addEventListener('DOMContentLoaded', function() {
    const feedItems = document.querySelectorAll('.feed-container > div');
    feedItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });
});
// activity
// Add staggered animation delay to activity items
document.addEventListener('DOMContentLoaded', function() {
    const activities = document.querySelectorAll('.activity-item');
    activities.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
    });

    // Optional: Add time ago updates
    function updateTimestamps() {
        const timestamps = document.querySelectorAll('.activity-header small:first-child');
        timestamps.forEach(timestamp => {
            // Update relative time logic here
        });
    }
    
    setInterval(updateTimestamps, 60000); // Update every minute
});
// topic
document.addEventListener('DOMContentLoaded', function() {
    // Add animation delay to topics
    const topics = document.querySelectorAll('.topic-widget-container > div');
    topics.forEach((topic, index) => {
        topic.style.animationDelay = `${index * 0.05}s`;
    });

    // Optional: Add topic count badges
    topics.forEach(topic => {
        const link = topic.querySelector('a');
        const count = topic.dataset.count;
        if (count) {
            link.setAttribute('data-count', count);
        }
    });
});
// room
document.addEventListener('DOMContentLoaded', function() {
    // Add animation delay to comments
    const comments = document.querySelectorAll('.commnet-wrapper > div');
    comments.forEach((comment, index) => {
        comment.style.animationDelay = `${index * 0.1}s`;
    });

    // Auto-submit form on enter
    const commentForm = document.querySelector('.commnet-form form');
    const commentInput = commentForm.querySelector('input[type="text"]');

    commentInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (this.value.trim()) {
                commentForm.submit();
            }
        }
    });
});
// topic form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.create-topic-container form');
    const submitButton = form.querySelector('input[type="submit"]');

    form.addEventListener('submit', function(e) {
        // Add loading state
        submitButton.classList.add('loading');
        submitButton.value = 'Creating...';
        
        // Optional: Basic form validation
        const inputs = form.querySelectorAll('input[type="text"], textarea');
        inputs.forEach(input => {
            if (!input.value.trim()) {
                e.preventDefault();
                input.style.borderColor = '#e74c3c';
                submitButton.classList.remove('loading');
                submitButton.value = 'Submit';
            }
        });
    });

    // Remove error styling on input
    form.querySelectorAll('input, textarea').forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '';
        });
    });
});
// delete obj
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.delete-object-container form');
    const deleteButton = form.querySelector('input[type="submit"]');
    const goBackButton = form.querySelector('a');

    // Add confirmation on delete
    form.addEventListener('submit', function(e) {
        deleteButton.value = 'Deleting...';
        deleteButton.style.opacity = '0.7';
        deleteButton.style.cursor = 'not-allowed';
    });

    // Optional: Close on overlay click
    document.querySelector('.delete-overlay').addEventListener('click', function(e) {
        if (e.target === this) {
            window.history.back();
        }
    });

    // Optional: Close on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            window.history.back();
        }
    });
});
// room form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.create-room-container form');
    const submitButton = form.querySelector('input[type="submit"]');

    // Form submission handling
    form.addEventListener('submit', function(e) {
        submitButton.value = 'Creating Room...';
        submitButton.style.opacity = '0.7';
        submitButton.disabled = true;
    });

    // Character counter for textarea
    const textarea = form.querySelector('textarea');
    if (textarea) {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('small');
            counter.classList.add('char-counter');
            textarea.parentNode.appendChild(counter);

            textarea.addEventListener('input', function() {
                const remaining = maxLength - this.value.length;
                counter.textContent = `${remaining} characters remaining`;
            });
        }
    }

    // Form field validation
    form.querySelectorAll('input[type="text"], textarea').forEach(field => {
        field.addEventListener('blur', function() {
            if (!this.value.trim() && this.hasAttribute('required')) {
                this.style.borderColor = '#e74c3c';
            }
        });

        field.addEventListener('focus', function() {
            this.style.borderColor = '';
        });
    });
});
// user registration
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.user-registration-container form');
    const passwordInput = form.querySelector('input[type="password"]');
    
    // Password strength indicator
    if (passwordInput) {
        const strengthIndicator = document.createElement('div');
        strengthIndicator.className = 'password-strength';
        passwordInput.parentNode.appendChild(strengthIndicator);

        passwordInput.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            strengthIndicator.className = `password-strength ${strength}`;
        });
    }

    // Form submission handling
    form.addEventListener('submit', function(e) {
        const submitButton = this.querySelector('input[type="submit"]');
        submitButton.value = 'Creating Account...';
        submitButton.style.opacity = '0.7';
        submitButton.disabled = true;
    });

    // Password strength checker
    function checkPasswordStrength(password) {
        if (password.length < 8) return 'weak';
        if (password.match(/(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])/)) return 'strong';
        return 'medium';
    }
});
// login
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.login-container form');
    const submitButton = form.querySelector('input[type="submit"]');

    // Form submission handling
    form.addEventListener('submit', function(e) {
        const username = form.querySelector('input[name="username"]').value;
        const password = form.querySelector('input[name="password"]').value;

        if (!username || !password) {
            e.preventDefault();
            showError('Please fill in all fields');
            return;
        }

        submitButton.value = 'Logging in...';
        submitButton.disabled = true;
    });

    // Error message display
    function showError(message) {
        const error = document.createElement('div');
        error.className = 'error-message';
        error.textContent = message;
        
        const existingError = form.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        submitButton.parentNode.insertBefore(error, submitButton);
    }

    // Optional: Password visibility toggle
    const passwordField = form.querySelector('input[name="password"]');
    const toggleButton = document.createElement('span');
    toggleButton.className = 'password-toggle';
    toggleButton.innerHTML = '👁️';
    passwordField.parentNode.appendChild(toggleButton);

    toggleButton.addEventListener('click', function() {
        const type = passwordField.getAttribute('type');
        passwordField.setAttribute('type', type === 'password' ? 'text' : 'password');
    });
});
// profile page
document.addEventListener('DOMContentLoaded', function() {
    // Add intersection observer for smooth scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all main sections
    document.querySelectorAll('.profile-page > div').forEach(section => {
        observer.observe(section);
    });

    // Optional: Add scroll to top button
    const scrollButton = document.createElement('button');
    scrollButton.className = 'scroll-top';
    scrollButton.innerHTML = '↑';
    document.body.appendChild(scrollButton);

    scrollButton.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    window.addEventListener('scroll', () => {
        scrollButton.style.display = window.scrollY > 500 ? 'block' : 'none';
    });
});
