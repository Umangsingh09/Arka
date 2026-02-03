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
├── requirements.txt   # Python dependencies
├── Procfile          # Deployment config
└── render.yaml       # Render.com config
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

## Deployment on Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select this repo
   - Use the default settings
   - Click "Create Web Service"

3. **Set Environment Variables on Render**
    - Go to Dashboard → Your Service → Environment
    - Add the following variables:
       - `SECRET_KEY`: Generate one using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
       - `DEBUG`: `false`
       - `ALLOWED_HOSTS`: `your-app-name.onrender.com`

4. **Create Superuser on Render**
   ```bash
   render exec django python manage.py createsuperuser
   ```

## Payments

Automated payment gateway integration is currently disabled. The admin can record payment status and notes on each request; the team will provide invoice and manual payment instructions to clients.

## Environment Variables

Create a `.env` file locally:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## URLs

- `/` - Landing page
- `/request-website/` - Public form
- `/login/` - User login
- `/signup/` - User signup
- `/dashboard/` - User dashboard
- `/admin/` - Admin panel
-- (Automated payment URLs removed) Use the dashboard and admin comments for manual payment instructions.

## Support

📧 Email: contact@arka.com

## License

MIT License - feel free to use for personal/commercial projects!

---

Built with ❤️ by Arka Team ✨
