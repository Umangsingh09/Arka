#!/usr/bin/env python
"""
Send real test email for gym website request
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arka_backend.settings')
django.setup()

from projects.services import send_website_request_email, send_website_request_confirmation

print("=" * 70)
print("SENDING TEST EMAIL TO: rajumang74@gmail.com")
print("=" * 70)

try:
    # Send email to admin
    result = send_website_request_email(
        business_name="FitZone Gym",
        email="umangraj032@gmail.com",
        website_type="Business Website",
        description="""
We are a premium fitness gym in the city center with state-of-the-art equipment. 

We need a professional website that:
- Showcases our gym facilities with photos
- Lists our membership packages and pricing
- Shows class schedules (yoga, CrossFit, spinning, etc.)
- Allows members to book personal training sessions
- Online payment for memberships
- Contact form for inquiries
- Integration with our gym management software

We have 200+ members and want to attract more through the website.
        """.strip(),
        budget="$1500 - $3000",
        is_logged_in=False,
        user_info=None
    )
    
    print(f"\n✓ Admin email sent successfully: {result}")
    
    # Send confirmation to customer
    result = send_website_request_confirmation("umangraj032@gmail.com", "FitZone Gym")
    print(f"✓ Confirmation email sent to customer: {result}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE!")
    print("=" * 70)
    print("\nCheck rajumang74@gmail.com inbox for the gym website request")
    print("Check umangraj032@gmail.com inbox for the confirmation email")
    
except Exception as e:
    print(f"\n✗ Error: {str(e)}")
    print(f"\nNote: If you see 'Connection refused', SMTP is not configured.")
    print(f"To send real emails, add Gmail credentials to .env:")
    print(f"  EMAIL_HOST_PASSWORD=your-app-password")
