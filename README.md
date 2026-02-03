# 🚀 Arka - Custom Website Builder

A Django-based web application that helps clients request and track custom websites with built-in admin communication, status tracking, and payment integration.

## Features

✨ **Core Features:**
- 📋 Public website request form (no login required)
- 🔐 User authentication & dashboard
- 📞 Admin-to-client communication with status updates
- 📧 Email notifications
- 💳 Payment integration (Razorpay ready)
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
- Connected to Payment model

### Payment
- OneToOne relationship with WebsiteRequest
- Razorpay integration fields
- Status tracking (pending, processing, completed, failed, refunded)
- Invoice & receipt management

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
     - `RAZORPAY_KEY_ID`: Your Razorpay test key
     - `RAZORPAY_KEY_SECRET`: Your Razorpay test secret

4. **Create Superuser on Render**
   ```bash
   render exec django python manage.py createsuperuser
   ```

## Payment Integration

### Test Mode (Development)
- Get keys from [Razorpay Dashboard](https://dashboard.razorpay.com/#/app/keys)
- Use test keys starting with `rzp_test_`
- Test card: `4111 1111 1111 1111`

### Live Mode (Production)
- Switch to live keys starting with `rzp_live_`
- Razorpay will verify your website details

## Environment Variables

Create a `.env` file locally:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=rzp_test_xxx
```

## URLs

- `/` - Landing page
- `/request-website/` - Public form
- `/login/` - User login
- `/signup/` - User signup
- `/dashboard/` - User dashboard
- `/admin/` - Admin panel
- `/payment/<id>/` - Payment page
- `/payment/callback/` - Razorpay webhook

## Support

📧 Email: contact@arka.com

## License

MIT License - feel free to use for personal/commercial projects!

---

Built with ❤️ by Arka Team ✨
