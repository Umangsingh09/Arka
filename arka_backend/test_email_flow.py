#!/usr/bin/env python
"""
Comprehensive email flow test script for Arka
Tests the complete website request submission flow with specific test emails
Run with: python test_email_flow.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arka_backend.settings')
django.setup()

from projects.services import send_contact_form_email, send_website_request_email, send_website_request_confirmation
from django.conf import settings
import logging

# Configure logging to see all messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("=" * 80)
print("ARKA - COMPREHENSIVE EMAIL FLOW TEST")
print("=" * 80)
print(f"\nEmail Configuration:")
print(f"  DEBUG Mode: {settings.DEBUG}")
print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print(f"  ADMIN_EMAIL: {settings.ADMIN_EMAIL}")

print("\n" + "=" * 80)
print("TEST 1: CONTACT FORM EMAIL (Admin Notification)")
print("=" * 80)
try:
    result = send_contact_form_email(
        name="Test User",
        email="umangraj032@gmail.com",
        message="This is a test contact message from the website contact form."
    )
    status = "✓ SUCCESS" if result else "✗ FAILED"
    print(f"{status} - Contact form email sent to admin (rajumang74@gmail.com)")
except Exception as e:
    print(f"✗ FAILED - Error: {type(e).__name__}: {str(e)}")

print("\n" + "=" * 80)
print("TEST 2: WEBSITE REQUEST - ADMIN NOTIFICATION")
print("=" * 80)
try:
    result = send_website_request_email(
        business_name="Test Business LLC",
        email="umangraj032@gmail.com",
        website_type="E-Commerce Store",
        description="We need a custom e-commerce website to sell our products online. The site should have product catalog, shopping cart, payment integration, and inventory management.",
        budget="$2000 - $3000",
        is_logged_in=True,
        user_info="Umanraj Singh"
    )
    status = "✓ SUCCESS" if result else "✗ FAILED"
    print(f"{status} - Website request email sent to admin (rajumang74@gmail.com)")
except Exception as e:
    print(f"✗ FAILED - Error: {type(e).__name__}: {str(e)}")

print("\n" + "=" * 80)
print("TEST 3: WEBSITE REQUEST - CLIENT CONFIRMATION")
print("=" * 80)
try:
    result = send_website_request_confirmation(
        email="umangraj032@gmail.com",
        business_name="Test Business LLC"
    )
    status = "✓ SUCCESS" if result else "✗ FAILED"
    print(f"{status} - Confirmation email sent to client (umangraj032@gmail.com)")
except Exception as e:
    print(f"✗ FAILED - Error: {type(e).__name__}: {str(e)}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("""
The email system has been tested with the following test emails:
  - Client Email: umangraj032@gmail.com
  - Admin Email: rajumang74@gmail.com

Expected Results:
  1. Admin (rajumang74@gmail.com) should receive:
     - Contact form submission from umangraj032@gmail.com
     - Website request notification with project details
     
  2. Client (umangraj032@gmail.com) should receive:
     - Confirmation email for their website request

Check your Gmail inbox for incoming emails.
If DEBUG=True, emails appear in the console output above.
If DEBUG=False, emails are sent via SMTP to rajumang74@gmail.com.

Configuration Details:
""")
print(f"  Email Backend: {settings.EMAIL_BACKEND}")
print(f"  SMTP Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
print(f"  TLS Enabled: {settings.EMAIL_USE_TLS}")
print(f"  From Email: {settings.DEFAULT_FROM_EMAIL}")
print("\n" + "=" * 80)
