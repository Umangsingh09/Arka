# 🚀 Arka - Custom Website Builder

A Django-based web application that helps clients request and track custom websites with built-in admin communication, status tracking, and payment integration.

## Features

✨ **Core Features:**
- 📋 Public website request form (no login required)
- 🔐 User authentication & dashboard
- 📞 Admin-to-client communication with status updates
- 📧 Email notifications
- 💳 Manual payment workflow (admin-managed)
- 🎨 Beautiful, responsive UI with Bootstrap

## Quick Start

### Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd arka_backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the landing page.

### Admin Panel

- URL: `http://127.0.0.1:8000/admin/`
- Manage website requests and track payments

## Project Structure

```
arka_backend/
├── accounts/          # User authentication
├── projects/          # Website requests & payments
├── templates/         # HTML templates
├── arka_backend/      # Django settings & URLs
├── manage.py          # Django management
└── requirements.txt   # Python dependencies
```

## Key Models


### WebsiteRequest
- business_name, email, description
- website_type, budget
- Status tracking with admin notes
- Admin-managed payment fields (`payment_status`, `payment_note`) for manual invoicing

### StatusUpdate
- Tracks all status changes
- Admin messages & timestamps
- Email notification tracking

## Local Development Setup

1. **Clone and Setup**
   ```bash
   git clone <your-repo-url>
   cd arka_backend
   python -m venv venv
   source venv/Scripts/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**
   ```bash
   python manage.py runserver
   ```
   
   Visit: `http://127.0.0.1:8000/`

## Payments

Automated payment gateway integration is currently disabled. The admin can record payment status and notes on each request; the team will provide invoice and manual payment instructions to clients.

## Environment Variables

Create a `.env` file locally:
```
SECRET_KEY=django-insecure-c7=f@6ix@37_bosvln-8j@ijsk+f)45-ejl129%2py=6r-f!m+
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## URLs

- `/` - Landing page
- `/request-website/` - Public form
- `/login/` - User login
- `/signup/` - User signup
- `/dashboard/` - User dashboard
- `/admin/` - Admin panel
- `/contact/` - Contact form

## Support

📧 Email: contact@arka.com

## License

MIT License - feel free to use for personal/commercial projects!

---

Built with ❤️ by Arka Team ✨
