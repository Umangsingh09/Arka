from django.db import models
from django.utils import timezone
from django.conf import settings


WEBSITE_TYPES = [
    ('ecommerce', 'E-Commerce Store'),
    ('blog', 'Blog/Content Site'),
    ('portfolio', 'Portfolio/Resume'),
    ('business', 'Business Website'),
    ('landing', 'Landing Page'),
    ('saas', 'SaaS Application'),
    ('social', 'Social Network'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
    ('new', '🆕 New'),
    ('contacted', '📞 Contacted'),
    ('in_progress', '⚙️ In Progress'),
    ('completed', '✅ Completed'),
]

PAYMENT_STATUS_CHOICES = [
    ('pending', '⏳ Pending'),
    ('processing', '🔄 Processing'),
    ('completed', '✅ Completed'),
    ('failed', '❌ Failed'),
    ('refunded', '↩️ Refunded'),
]


class WebsiteRequest(models.Model):
    """Model to track website requests from clients"""
    
    # User (optional - for logged-in users)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='website_requests')
    
    # Required fields
    business_name = models.CharField(max_length=200, help_text="Name of the business or project", default="Not provided")
    website_type = models.CharField(max_length=50, choices=WEBSITE_TYPES, help_text="Type of website needed", default='other')
    email = models.EmailField(help_text="Contact email address", default="unknown@example.com")
    description = models.TextField(help_text="Describe what you need for your website", default="No description provided")
    
    # Optional fields
    budget = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Your budget range (optional)"
    )
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    
    # Admin Communication
    admin_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Internal notes from admin team"
    )
    status_updated_at = models.DateTimeField(null=True, blank=True)
    notified_user = models.BooleanField(default=False, help_text="Whether user was notified about status change")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Website Request'
        verbose_name_plural = 'Website Requests'
    
    def __str__(self):
        return f"{self.business_name} - {self.get_status_display()}"
    
    def get_status_emoji(self):
        """Return emoji for current status"""
        emojis = {
            'new': '🆕',
            'contacted': '📞',
            'in_progress': '⚙️',
            'completed': '✅',
        }
        return emojis.get(self.status, '•')


class Payment(models.Model):
    """Model to track payments for website requests"""
    
    request = models.OneToOneField(WebsiteRequest, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Payment amount in INR")
    currency = models.CharField(max_length=3, default='INR')
    
    # Payment tracking
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    # Razorpay integration
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Receipt
    receipt_url = models.URLField(blank=True, null=True)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"Payment for {self.request.business_name} - ₹{self.amount}"
    
    def get_payment_status_display(self):
        """Return emoji for payment status"""
        statuses = {
            'pending': '⏳ Pending',
            'processing': '🔄 Processing',
            'completed': '✅ Completed',
            'failed': '❌ Failed',
            'refunded': '↩️ Refunded',
        }
        return statuses.get(self.status, self.get_status_display())


class StatusUpdate(models.Model):
    """Track status update history for client notifications"""
    
    request = models.ForeignKey(WebsiteRequest, on_delete=models.CASCADE, related_name='status_updates')
    old_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    admin_message = models.TextField(blank=True, null=True, help_text="Message to send to client")
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Status Update'
        verbose_name_plural = 'Status Updates'
    
    def __str__(self):
        return f"{self.request.business_name}: {self.old_status} → {self.new_status}"
