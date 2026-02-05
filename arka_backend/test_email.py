#!/usr/bin/env python
"""
Test script for email functionality
Run with: python test_email.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arka_backend.settings')
django.setup()

from projects.services import send_contact_form_email, send_website_request_email, send_website_request_confirmation

print("=" * 60)
print("TESTING ARKA EMAIL FUNCTIONALITY")
print("=" * 60)

# Test 1: Contact form email
print("\n[TEST 1] Contact Form Email")
print("-" * 60)
try:
    result = send_contact_form_email(
        name="Test User",
        email="test@example.com",
        message="This is a test message from the contact form. Please verify it was received correctly."
    )
    print(f"✓ Contact email sent: {result}")
except Exception as e:
    print(f"✗ Error sending contact email: {str(e)}")

# Test 2: Website request email
print("\n[TEST 2] Website Request Email (Admin Notification)")
print("-" * 60)
try:
    result = send_website_request_email(
        business_name="Test Business",
        email="client@example.com",
        website_type="E-Commerce Store",
        description="We need a beautiful e-commerce website to sell our products online. The website should have product catalog, shopping cart, and payment integration.",
        budget="$1000 - $2000",
        is_logged_in=True,
        user_info="John Doe"
    )
    print(f"✓ Website request email sent to admin: {result}")
except Exception as e:
    print(f"✗ Error sending website request email: {str(e)}")

# Test 3: Confirmation email
print("\n[TEST 3] Website Request Confirmation Email (Client)")
print("-" * 60)
try:
    result = send_website_request_confirmation(
        email="client@example.com",
        business_name="Test Business"
    )
    print(f"✓ Confirmation email sent to client: {result}")
except Exception as e:
    print(f"✗ Error sending confirmation email: {str(e)}")

print("\n" + "=" * 60)
print("EMAIL TESTING COMPLETED")
print("=" * 60)
print("\nNote: Check your console output above for emails if DEBUG=True")
print("For production, check your Gmail inbox at rajumang74@gmail.com")
