from django.contrib import admin
from django.utils.html import format_html
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import WebsiteRequest, StatusUpdate


@admin.register(StatusUpdate)
class StatusUpdateAdmin(admin.ModelAdmin):
    list_display = ['request', 'old_status', 'new_status', 'created_at', 'notified_status']
    list_filter = ['created_at', 'notified']
    search_fields = ['request__business_name', 'admin_message']
    readonly_fields = ['request', 'old_status', 'new_status', 'created_at']
    
    def notified_status(self, obj):
        if obj.notified:
            return format_html('✅ <span style="color: green;">Notified</span>')
        return format_html('❌ <span style="color: red;">Not Notified</span>')
    notified_status.short_description = 'User Notified'


@admin.register(WebsiteRequest)
class WebsiteRequestAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'email', 'website_type', 'status_badge', 'payment_status_display', 'created_at', 'user_info']
    list_filter = ['status', 'website_type', 'created_at']
    search_fields = ['business_name', 'email', 'description']
    readonly_fields = ['email', 'created_at', 'updated_at', 'status_updated_at']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('user', 'business_name', 'email')
        }),
        ('Project Details', {
            'fields': ('website_type', 'description', 'budget')
        }),
        ('Status & Communication', {
            'fields': ('status', 'admin_notes', 'status_updated_at', 'notified_user', 'payment_status', 'payment_note'),
            'description': 'Update status, add notes, and manage manual payment info'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Display status with color coding"""
        colors = {
            'new': '#FFC107',
            'contacted': '#17A2B8',
            'in_progress': '#0D6EFD',
            'completed': '#28A745',
        }
        emoji = {
            'new': '🆕',
            'contacted': '📞',
            'in_progress': '⚙️',
            'completed': '✅',
        }
        color = colors.get(obj.status, '#6C757D')
        icon = emoji.get(obj.status, '•')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def user_info(self, obj):
        if obj.user:
            return format_html('<a href="/admin/accounts/user/{}/change/">{}</a>', obj.user.id, obj.user.username)
        return '—'
    user_info.short_description = 'User'

    def payment_status_display(self, obj):
        colors = {
            'not_discussed': '#6C757D',
            'pending': '#FFC107',
            'paid': '#28A745',
        }
        labels = {
            'not_discussed': 'Not Discussed',
            'pending': 'Pending',
            'paid': 'Paid',
        }
        color = colors.get(obj.payment_status, '#6C757D')
        label = labels.get(obj.payment_status, obj.payment_status)
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>', color, label)
    payment_status_display.short_description = 'Payment'
    
    def save_model(self, request, obj, form, change):
        """Save model and track status changes"""
        if change:  # If editing existing object
            old_obj = WebsiteRequest.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                # Status changed - create update record
                StatusUpdate.objects.create(
                    request=obj,
                    old_status=old_obj.status,
                    new_status=obj.status,
                    admin_message=obj.admin_notes
                )
                obj.status_updated_at = __import__('django.utils.timezone', fromlist=['now']).now()
                obj.notified_user = False  # Reset notification flag
                
                # Send email notification
                self.send_status_email(obj, old_obj.status)
        
        super().save_model(request, obj, form, change)
    
    def send_status_email(self, obj, old_status):
        """Send email to client when status changes"""
        try:
            subject = f"Update: Your {obj.business_name} Website Request - {obj.get_status_display()}"
            
            context = {
                'business_name': obj.business_name,
                'old_status': dict(WebsiteRequest._meta.get_field('status').choices).get(old_status, old_status),
                'new_status': obj.get_status_display(),
                'status_emoji': obj.get_status_emoji(),
                'admin_notes': obj.admin_notes or 'Your request is being processed.',
                'dashboard_url': 'http://127.0.0.1:8000/dashboard/',
            }
            
            message = f"""
Hi {obj.business_name},

Your website request status has been updated!

OLD STATUS: {context['old_status']}
NEW STATUS: {context['status_emoji']} {context['new_status']}

NOTES FROM OUR TEAM:
{context['admin_notes']}

View your full request details here:
{context['dashboard_url']}

Best regards,
Arka Team ✨
            """
            
            send_mail(
                subject,
                message,
                'noreply@arka.com',
                [obj.email],
                fail_silently=True,
            )
            
            # Mark as notified
            obj.notified_user = True
            WebsiteRequest.objects.filter(pk=obj.pk).update(notified_user=True)
            
        except Exception as e:
            print(f"Email notification error: {e}")



