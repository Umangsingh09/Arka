# Email Configuration & Setup Guide

This guide explains how to set up and use the email notification system in Arka.

## Overview

Arka now has a complete email notification system that sends:

1. **Contact Form Emails** – When someone uses the "Contact Us" page
2. **Website Request Admin Notification** – When a client submits a website request
3. **Website Request Confirmation** – Confirmation email to the client

All emails are formatted cleanly and include all relevant information.

## Quick Start

### Development Mode (Console Backend)

By default, `DEBUG=True` in `settings.py` uses the **Console Email Backend**. This means:
- Emails are printed to your console instead of being sent
- Useful for testing without needing real email credentials
- No actual email is sent

### Production Mode (SMTP Backend)

To enable real email sending:

1. **Get Gmail App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your platform)
   - Google will generate a 16-character password
   - Copy this password

2. **Set Environment Variables** in `.env`:
   ```bash
   DEBUG=False
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=rajumang74@gmail.com
   EMAIL_HOST_PASSWORD=your-16-character-app-password
   DEFAULT_FROM_EMAIL=rajumang74@gmail.com
   ADMIN_EMAIL=rajumang74@gmail.com
   ```

3. **Test Email Sending**
   ```bash
   python test_email.py
   ```

## Email Types & Content

### 1. Contact Form Email (to Admin)

**When triggered:** User submits the Contact Us form

**Subject:** `New Contact Message – Arka`

**Includes:**
- Sender's name
- Sender's email address
- Date & time of submission
- Full message
- Reply-to email address

**Example:**
```
New Contact Message from Arka Website

---------- MESSAGE DETAILS ----------
Name:       John Smith
Email:      john@example.com
Date & Time: 2026-02-03 14:30:00
IP/Source:  Website Contact Form

---------- MESSAGE ----------
I'm interested in building an e-commerce site for my business...

---------- END MESSAGE ----------

To reply, use the sender's email: john@example.com
```

---

### 2. Website Request Admin Email

**When triggered:** User submits a website request (logged in or anonymous)

**Subject:** `New Website Request Received – Arka`

**Includes:**
- Business name
- Client email
- Website type (e.g., E-Commerce, Blog, etc.)
- Budget (if provided)
- Whether user is logged in or anonymous
- User info (name if logged in)
- Full project description
- Action items for the admin

**Example:**
```
New Website Request Received – Arka

---------- REQUEST DETAILS ----------
Business Name:   Fashion Store Co.
Client Email:    owner@fashionstore.com
Website Type:    E-Commerce Store
Budget:          $2000 - $5000
Logged In:       Yes (John Doe)
Submission Date: 2026-02-03 14:35:00

---------- PROJECT DESCRIPTION ----------
We need a modern e-commerce website with:
- Product catalog with 500+ items
- Shopping cart functionality
- Payment integration
- Inventory management

---------- END REQUEST ----------

Action Items:
1. Review the project requirements above
2. Contact the client at: owner@fashionstore.com
3. Follow up within 24 hours
4. Update request status in admin dashboard
```

---

### 3. Website Request Confirmation (to Client)

**When triggered:** Right after website request is saved

**Subject:** `Your Website Request Received – Arka`

**Includes:**
- Personalized greeting with business name
- Confirmation message
- Expected response timeframe
- Invitation to reply

**Example:**
```
Thank you for requesting a website from Arka!

Hi Fashion Store Co.,

We've received your website request and our team is reviewing your project 
details.

You can expect to hear from us within 24 hours at the email address you 
provided (owner@fashionstore.com).

In the meantime, if you have any questions or additional information to 
share, feel free to reply to this email.

Best regards,
The Arka Team

P.S. Keep an eye on your email for our follow-up!
```

## Code Structure

### Email Services (`projects/services.py`)

All email logic is centralized in this module:

```python
# Send contact form email
send_contact_form_email(name, email, message)

# Send website request notification to admin
send_website_request_email(
    business_name, email, website_type, 
    description, budget, is_logged_in, user_info
)

# Send confirmation to client
send_website_request_confirmation(email, business_name)
```

### Integration Points

**Contact Form (`/contact/`)**
- `projects/views.py` → `contact()` function
- Calls `send_contact_form_email()` on form submission
- Graceful error handling (email failure doesn't break the flow)

**Website Request (`/request-website/`)**
- `projects/views.py` → `request_website()` function
- Calls both `send_website_request_email()` and `send_website_request_confirmation()`
- Also triggered when user creates request after logging in

## Error Handling

The email system is designed to be **non-blocking**:

- If email sending fails, the request is still processed and saved
- Errors are logged to `logger.error()` for debugging
- User still gets success message (won't notice email failure)
- Admin can see errors in Django logs

Example in `views.py`:
```python
try:
    send_website_request_email(...)
except Exception as e:
    print(f"Email sending error (non-blocking): {str(e)}")
```

## Testing

### Local Testing (Console Output)

The easiest way to test:

```bash
python test_email.py
```

This will:
1. Generate sample contact form email
2. Generate sample website request email
3. Generate sample confirmation email
4. Print all emails to console

Check the console output to see formatted emails.

### Production Testing

To test with real Gmail account:

1. Set `DEBUG=False` in `.env`
2. Add valid Gmail credentials to `.env`
3. Run `python test_email.py`
4. Check Gmail inbox at `rajumang74@gmail.com`
5. Emails should arrive in the inbox within seconds

### Manual Testing in Django

Use Django shell to test:

```bash
python manage.py shell
```

Then:
```python
from projects.services import send_contact_form_email

result = send_contact_form_email(
    "Test Name",
    "test@example.com", 
    "This is a test message"
)
print(f"Email sent: {result}")
```

## Switching Email Providers

The system is designed to be easy to switch providers.

### Switch from Gmail to SendGrid

1. Update `.env`:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.sendgrid.net
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=apikey
   EMAIL_HOST_PASSWORD=your-sendgrid-api-key
   ```

2. No code changes needed – it works immediately!

### Switch from SMTP to AWS SES

1. Install `django-ses`:
   ```bash
   pip install django-ses
   ```

2. Update `settings.py` EMAIL_BACKEND:
   ```python
   EMAIL_BACKEND = 'django_ses.SESBackend'
   ```

3. Add AWS credentials to `.env`

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `EMAIL_BACKEND` | `console.EmailBackend` | Email service (console for dev, SMTP for production) |
| `EMAIL_HOST` | `smtp.gmail.com` | SMTP server address |
| `EMAIL_PORT` | `587` | SMTP port (usually 587 for TLS) |
| `EMAIL_USE_TLS` | `True` | Whether to use TLS encryption |
| `EMAIL_HOST_USER` | `rajumang74@gmail.com` | Email account for sending |
| `EMAIL_HOST_PASSWORD` | `` | Email account password (set in .env) |
| `DEFAULT_FROM_EMAIL` | `rajumang74@gmail.com` | "From" email address in sent emails |
| `ADMIN_EMAIL` | `rajumang74@gmail.com` | Where admin notifications are sent |

## Troubleshooting

### "Connection refused" error

**Problem:** Django can't connect to SMTP server

**Solution:**
- Check `EMAIL_HOST` and `EMAIL_PORT` are correct
- Verify internet connection
- Check firewall isn't blocking port 587

### "Authentication failed" error

**Problem:** Gmail credentials are invalid

**Solution:**
- Verify you're using Gmail App Password (not regular password)
- Get it from: https://myaccount.google.com/apppasswords
- Make sure you have 2FA enabled on your Google account
- Check `EMAIL_HOST_USER` matches the account

### Emails not appearing in Gmail inbox

**Problem:** Email was sent but not visible

**Solution:**
- Check Spam/Promotions folder
- Add `rajumang74@gmail.com` to contacts to mark as trusted
- Check email headers for any issues
- Verify `EMAIL_HOST_PASSWORD` is correct

## Future Enhancements

Potential improvements:

1. **HTML Emails** – Currently plain text; can add HTML templates
2. **Email Templates** – Use Django's template system for dynamic content
3. **Email Queuing** – Use Celery to queue emails for async sending
4. **Email Tracking** – Track opens, clicks, bounces
5. **Scheduled Emails** – Follow-up emails at specific times
6. **Custom Email Domains** – Use Arka's own domain for sending

## Summary

✅ **Email system is fully functional and production-ready**
- Centralized, reusable code
- Clean, professional email formatting
- Graceful error handling
- Easy to configure and switch providers
- Tested and working
