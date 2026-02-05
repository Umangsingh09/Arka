# Email System - User Guide

## For Users

### Submitting a Contact Message

1. **Visit Contact Page:** `http://localhost:8000/contact/`
2. **Fill Form:**
   - Name: Your name
   - Email: Your email address
   - Message: Your message
3. **Click "Send Message"**
4. **Confirmation:** "Your message has been sent! We will get back to you soon."

**What Happens:**
- Admin receives email with your contact details
- Your message is formatted and delivered within seconds

---

## For Admin / Business Owner

### Receiving Notifications

You will receive emails when:
1. **Someone submits Contact Form**
   - Check the email (will be from `rajumang74@gmail.com` in development, real email in production)
   - Has the sender's name, email, and full message
   - Easy to reply directly to the sender

2. **Client requests a Website**
   - Detailed email with business name, website type, budget, description
   - Shows if client is logged in or anonymous
   - Includes action items checklist

3. **Client confirmation** 
   - Client also gets a thank you email
   - Sets expectation: "We'll contact you within 24 hours"

### Managing Requests

#### View all requests in admin panel:
- Go to `http://localhost:8000/admin/`
- Click "Website Requests" to see all submissions
- Update status, add notes, mark as completed

#### Check received emails:
- **Development:** Check console output where Django is running
- **Production:** Check `rajumang74@gmail.com` Gmail inbox

---

## Setup Instructions

### Minimal Setup (Development)

Just run Django - emails appear in console:

```bash
python manage.py runserver
```

No credentials needed! Emails print to console.

### Full Setup (Production)

1. **Get Gmail App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Google generates 16-character password
   - Copy it

2. **Update `.env` file:**
   ```
   DEBUG=False
   EMAIL_HOST_PASSWORD=your-16-character-app-password
   ```

3. **Restart Django:**
   ```
   python manage.py runserver
   ```

4. **Test it:**
   ```
   python test_email.py
   ```
   Check `rajumang74@gmail.com` inbox for 3 test emails

---

## Email Examples

### Email #1: Contact Message

```
FROM: rajumang74@gmail.com
TO: rajumang74@gmail.com
SUBJECT: New Contact Message – Arka

New Contact Message from Arka Website

---------- MESSAGE DETAILS ----------
Name:       John Smith
Email:      john@example.com
Date & Time: 2026-02-03 14:30:00
IP/Source:  Website Contact Form

---------- MESSAGE ----------
Hi, I'm interested in building an e-commerce website for my fashion 
business. Can you provide a quote?

---------- END MESSAGE ----------

To reply, use the sender's email: john@example.com
```

### Email #2: Website Request (Admin)

```
FROM: rajumang74@gmail.com
TO: rajumang74@gmail.com
SUBJECT: New Website Request Received – Arka

New Website Request Received – Arka

---------- REQUEST DETAILS ----------
Business Name:   Fashion Store Inc.
Client Email:    owner@fashionstore.com
Website Type:    E-Commerce Store
Budget:          $2000 - $5000
Logged In:       Yes (John Smith)
Submission Date: 2026-02-03 14:35:00

User Info:      John Smith

---------- PROJECT DESCRIPTION ----------
We're a growing fashion brand with 500+ SKUs. We need:
- Product catalog with filters
- Shopping cart
- Payment processing
- Inventory sync
- Mobile responsive

---------- END REQUEST ----------

Action Items:
1. Review the project requirements above
2. Contact the client at: owner@fashionstore.com
3. Follow up within 24 hours
4. Update request status in admin dashboard

Note: This request has been automatically logged in the Arka system.
Check the admin dashboard for more details and to track progress.
```

### Email #3: Confirmation (Client)

```
FROM: rajumang74@gmail.com
TO: owner@fashionstore.com
SUBJECT: Your Website Request Received – Arka

Thank you for requesting a website from Arka!

Hi Fashion Store Inc.,

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

---

## Website Integrations

### Navigation Bar
- Top right: "Contact" link → `/contact/`
- Top right: "Get Started" button → `/request-website/`

### Landing Page
- Hero section: "Request Your Website" button
- CTA section: "Request a Website" and "Contact Us" buttons

### Footer
- "Request Website" link
- "Contact Us" link
- "Login" and "Sign Up" links

---

## Testing

### Test All Emails

```bash
python test_email.py
```

Shows all 3 email types formatted and ready.

### Test in Django Shell

```bash
python manage.py shell
```

Then:
```python
from projects.services import send_contact_form_email

# Send test email
result = send_contact_form_email(
    "Test Name",
    "test@example.com",
    "This is a test message"
)
print(f"Sent: {result}")
```

### Manual Testing via Website

1. Go to `http://localhost:8000/contact/`
2. Fill form with test data
3. Submit
4. Check console output (if `DEBUG=True`)
5. Or check Gmail inbox (if `DEBUG=False`)

---

## Troubleshooting

### "Email didn't appear in my inbox"

**Development mode:**
- Check Django console where `runserver` is running
- Look for MIME email output with headers

**Production mode:**
- Check Gmail spam folder
- Wait 5-10 seconds (sometimes delayed)
- Verify `EMAIL_HOST_PASSWORD` is correct

### "Got authentication error"

- Email password wrong
- Using Gmail password instead of App Password
- Account doesn't have 2FA enabled

**Fix:**
1. Go to https://myaccount.google.com/apppasswords
2. Make sure 2FA is enabled first
3. Generate new 16-character password
4. Update `.env`

### "ModuleNotFoundError: No module named 'django'"

Make sure Python environment is activated:

```bash
# If using venv:
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Then run Django:
python manage.py runserver
```

---

## Files Reference

- **Contact Form:** [templates/contact.html](templates/contact.html)
- **Email Functions:** [projects/services.py](projects/services.py)
- **Contact View:** [projects/views.py](projects/views.py) - `contact()` function
- **Form Definition:** [projects/forms.py](projects/forms.py) - `ContactForm` class
- **Configuration:** [arka_backend/settings.py](arka_backend/settings.py) - EMAIL_* settings
- **Routes:** [arka_backend/urls.py](arka_backend/urls.py) - `path('contact/', ...)`

---

## Quick Reference

| Action | URL |
|--------|-----|
| Contact Us | `/contact/` |
| Request Website | `/request-website/` |
| Admin Panel | `/admin/` |
| Dashboard (logged in) | `/dashboard/` |
| Login | `/login/` |
| Signup | `/signup/` |

---

## Summary

✅ Email system fully operational
✅ Contact form working
✅ Website request emails working
✅ Admin notifications working
✅ Client confirmations working
✅ All integrated into website UI
✅ Production-ready

**Questions? See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed technical setup.**
