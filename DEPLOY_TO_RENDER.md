# 🚀 Deploy Arka to Render (Free)

## Step 1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `arka`
3. Description: "Custom website builder with Razorpay payments"
4. Click "Create repository"

## Step 2: Push Your Code to GitHub

```bash
# In c:\Users\rajum\arka\arka_backend

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/arka.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free account)
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub → Select your `arka` repository
4. Configure:
   - **Name**: `arka` (or any name)
   - **Runtime**: Python 3.13
   - **Build Command**: Leave as default (Render detects from Procfile)
   - **Start Command**: Leave as default
5. Scroll down to **"Environment"**
6. Add these environment variables:

```
DEBUG=false
ALLOWED_HOSTS=arka.onrender.com
SECRET_KEY=<generate-a-new-one>
RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_ID
RAZORPAY_KEY_SECRET=rzp_test_YOUR_KEY_SECRET
```

To generate `SECRET_KEY`, run in terminal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

7. Click **"Create Web Service"**
8. Wait for deployment (2-3 minutes)
9. Your live URL: `https://arka.onrender.com/`

## Step 4: Create Superuser on Render

After deployment completes, go to your service dashboard:

1. Click **"Shell"** tab
2. Run:
```bash
python manage.py createsuperuser
```

3. Enter username, email, password
4. Admin panel: `https://your-app-name.onrender.com/admin/`

## Step 5: Get Razorpay Test Keys

1. Go to [https://dashboard.razorpay.com/#/app/keys](https://dashboard.razorpay.com/#/app/keys)
2. Copy your **Test Key ID** and **Test Key Secret**
3. Update Render environment variables:
   - `RAZORPAY_KEY_ID` = Your test key ID
   - `RAZORPAY_KEY_SECRET` = Your test key secret
4. Redeploy (Render auto-deploys on env changes)

## Step 6: Test Your Live App

- Landing: `https://your-app-name.onrender.com/`
- Admin: `https://your-app-name.onrender.com/admin/`
- Request form: `https://your-app-name.onrender.com/request-website/`

## Troubleshooting

**App won't deploy?**
- Check Render logs in the dashboard
- Ensure all environment variables are set
- Verify `SECRET_KEY` is set (not the default insecure one)

**Database issues?**
- Render provides free SQLite for small apps
- For production, upgrade to PostgreSQL

**"Static files not found"?**
- Render collects static files automatically
- Wait 2-3 minutes after deploy

## Next Steps (Production Ready)

1. Add your real domain
2. Switch to Razorpay live keys
3. Set up email backend (Gmail SMTP, SendGrid, etc.)
4. Upgrade to PostgreSQL for reliability
5. Add SSL certificate (Render includes free Let's Encrypt)

---

Your live link will be: **https://arka.onrender.com** (replace `arka` with your app name)

🎉 That's it! Your Arka website is now live!
