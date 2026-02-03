from django import forms
from .models import WebsiteRequest


class WebsiteRequestForm(forms.ModelForm):
    """Form for clients to request a website"""
    
    class Meta:
        model = WebsiteRequest
        fields = ['business_name', 'website_type', 'description', 'budget', 'email']
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., My Fashion Store',
                'required': True,
            }),
            'website_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your website needs, features, and goals...',
                'rows': 6,
                'required': True,
            }),
            'budget': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., $500-$1000 (optional)',
            }),
        }
        labels = {
            'business_name': '🏢 Business Name',
            'website_type': '🌐 Website Type',
            'description': '📝 Project Description',
            'budget': '💰 Budget (Optional)',
            'email': '📧 Email Address',
        }


class ContactForm(forms.Form):
    """Form for users to contact Arka"""
    
    name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'required': True,
        }),
        label='👤 Name'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com',
            'required': True,
        }),
        label='📧 Email Address'
    )
    
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your message here...',
            'rows': 6,
            'required': True,
        }),
        label='💬 Message'
    )
