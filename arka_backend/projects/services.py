"""
Email services for Arka
Handles all email notifications in a reusable, maintainable way
"""

import logging
import smtplib
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

# Configure logging for email errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def send_admin_email(subject, message, recipient=None):
    """
    Send an email to admin with specified content
    
    Args:
        subject (str): Email subject
        message (str): Email body (plain text)
        recipient (str): Optional recipient email (defaults to ADMIN_EMAIL from settings)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    if not recipient:
        recipient = settings.ADMIN_EMAIL
    
    try:
        # Log the attempt
        logger.info(f"Attempting to send email to {recipient}")
        logger.info(f"Email Backend: {settings.EMAIL_BACKEND}")
        logger.info(f"DEBUG Mode: {settings.DEBUG}")
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        logger.info(f"✓ Email sent successfully to {recipient} | Subject: {subject}")
        print(f"✓ Email sent successfully to {recipient}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"✗ SMTP Authentication Error: Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env")
        logger.error(f"  Details: {str(e)}")
        return False
        
    except smtplib.SMTPException as e:
        logger.error(f"✗ SMTP Error while sending to {recipient}: {str(e)}")
        logger.error(f"  Check EMAIL_HOST ({settings.EMAIL_HOST}) and EMAIL_PORT ({settings.EMAIL_PORT})")
        return False
        
    except Exception as e:
        logger.error(f"✗ Unexpected error sending email to {recipient}: {type(e).__name__}: {str(e)}")
        return False


def send_contact_form_email(name, email, message):
    """
    Send contact form submission to admin
    
    Args:
        name (str): Sender's name
        email (str): Sender's email address
        message (str): Message content
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    formatted_message = f"""
New Contact Message from Arka Website

---------- MESSAGE DETAILS ----------
Name:       {name}
Email:      {email}
Date & Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
IP/Source:  Website Contact Form

---------- MESSAGE ----------
{message}

---------- END MESSAGE ----------

To reply, use the sender's email: {email}
    """.strip()
    
    subject = "New Contact Message – Arka"
    return send_admin_email(subject, formatted_message)


def send_website_request_email(business_name, email, website_type, description, budget=None, is_logged_in=False, user_info=None):
    """
    Send website request submission to admin
    
    Args:
        business_name (str): Business name
        email (str): Client's email address
        website_type (str): Type of website needed
        description (str): Project description
        budget (str): Budget (optional)
        is_logged_in (bool): Whether user is logged in
        user_info (str): Additional user info if logged in
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # Format the message clearly
    formatted_message = f"""
New Website Request Received – Arka

---------- REQUEST DETAILS ----------
Business Name:   {business_name}
Client Email:    {email}
Website Type:    {website_type}
Budget:          {budget if budget else 'Not specified'}
Logged In:       {'Yes' if is_logged_in else 'No (Anonymous)'}
Submission Date: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

{f'User Info:      {user_info}' if user_info else ''}

---------- PROJECT DESCRIPTION ----------
{description}

---------- END REQUEST ----------

Action Items:
1. Review the project requirements above
2. Contact the client at: {email}
3. Follow up within 24 hours
4. Update request status in admin dashboard

Note: This request has been automatically logged in the Arka system.
Check the admin dashboard for more details and to track progress.
    """.strip()
    
    subject = "New Website Request Received – Arka"
    return send_admin_email(subject, formatted_message)


def send_website_request_confirmation(email, business_name):
    """
    Send confirmation email to client after submitting website request
    
    Args:
        email (str): Client's email address
        business_name (str): Business name for personalization
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    message = f"""
Thank you for requesting a website from Arka!

Hi {business_name},

We've received your website request and our team is reviewing your project details.

You can expect to hear from us within 24 hours at the email address you provided ({email}).

In the meantime, if you have any questions or additional information to share, feel free to reply to this email.

Best regards,
The Arka Team

P.S. Keep an eye on your email for our follow-up!
    """.strip()
    
    subject = "Your Website Request Received – Arka"
    
    try:
        logger.info(f"Attempting to send confirmation email to client: {email}")
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"✓ Confirmation email sent successfully to {email}")
        print(f"✓ Confirmation email sent successfully to {email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"✗ SMTP Authentication Error when sending confirmation to {email}: Check credentials")
        logger.error(f"  Details: {str(e)}")
        return False
        
    except smtplib.SMTPException as e:
        logger.error(f"✗ SMTP Error sending confirmation to {email}: {str(e)}")
        return False
        
    except Exception as e:
        logger.error(f"✗ Unexpected error sending confirmation email to {email}: {type(e).__name__}: {str(e)}")
        return False
