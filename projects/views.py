from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .forms import WebsiteRequestForm
from .models import WebsiteRequest, Payment
from django.conf import settings


def landing(request):
    """Landing page for Arka"""
    return render(request, 'landing.html')


@require_http_methods(["GET", "POST"])
def request_website(request):
    """Handle website request submissions from public form"""
    
    if request.method == 'POST':
        form = WebsiteRequestForm(request.POST)
        if form.is_valid():
            # Check if user is logged in
            if request.user.is_authenticated:
                # Save with user
                website_request = form.save(commit=False)
                website_request.user = request.user
                website_request.save()
                messages.success(request, '✅ Your website request has been submitted! Check your dashboard to track progress.')
                return redirect('dashboard')
            else:
                # Store form data in session and redirect to login
                request.session['website_request_data'] = form.cleaned_data
                return redirect('login')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = WebsiteRequestForm()
    
    context = {
        'form': form,
        'total_requests': WebsiteRequest.objects.count(),
    }
    return render(request, 'request_website.html', context)


@login_required(login_url='login')
def dashboard(request):
    """Show user's submitted website requests"""
    requests = request.user.website_requests.all()
    
    context = {
        'requests': requests,
        'total_requests': requests.count(),
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def payment_page(request, request_id):
    """Handle payment processing page"""
    website_request = get_object_or_404(WebsiteRequest, id=request_id, user=request.user)
    
    # Check if payment already exists
    payment = Payment.objects.filter(request=website_request).first()
    
    if not payment:
        # Estimate payment based on budget or default
        amount = get_payment_amount(website_request)
        payment = Payment.objects.create(
            request=website_request,
            amount=amount,
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}"
        )
    
    context = {
        'payment': payment,
        'website_request': website_request,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'payment.html', context)


def get_payment_amount(website_request):
    """Determine payment amount based on budget or website type"""
    budget_map = {
        '0-5000': 5000,
        '5000-10000': 7500,
        '10000-25000': 15000,
        '25000-50000': 35000,
        '50000+': 50000,
    }
    
    if website_request.budget and website_request.budget in budget_map:
        return budget_map[website_request.budget]
    
    # Default pricing by type
    type_pricing = {
        'landing': 5000,
        'blog': 10000,
        'portfolio': 12000,
        'business': 20000,
        'ecommerce': 50000,
        'saas': 100000,
    }
    
    return type_pricing.get(website_request.website_type, 25000)


@csrf_exempt
def payment_callback(request):
    """Handle Razorpay payment callback"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_id = data.get('razorpay_payment_id')
            order_id = data.get('razorpay_order_id')
            signature = data.get('razorpay_signature')
            request_id = data.get('request_id')
            
            # Find payment
            payment = get_object_or_404(Payment, request_id=request_id)
            
            # In production: verify signature
            # For now: update payment status
            payment.razorpay_payment_id = payment_id
            payment.razorpay_order_id = order_id
            payment.razorpay_signature = signature
            payment.status = 'completed'
            payment.paid_at = __import__('django.utils.timezone', fromlist=['now']).now()
            payment.save()
            
            # Update request status
            payment.request.status = 'contacted'
            payment.request.admin_notes = f"Payment received: ₹{payment.amount}. Processing request..."
            payment.request.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=400)
    
    return JsonResponse({'status': 'invalid'}, status=405)


@login_required(login_url='login')
def payment_success(request, request_id):
    """Payment success page"""
    website_request = get_object_or_404(WebsiteRequest, id=request_id, user=request.user)
    payment = get_object_or_404(Payment, request=website_request)
    
    context = {
        'payment': payment,
        'website_request': website_request,
    }
    return render(request, 'payment_success.html', context)


def login_view(request):
    """Custom login view"""
    from django.contrib.auth import authenticate, login
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Check if there's pending form data
            if 'website_request_data' in request.session:
                data = request.session.pop('website_request_data')
                website_request = WebsiteRequest.objects.create(
                    user=user,
                    **data
                )
                messages.success(request, '✅ Welcome back! Your website request has been saved.')
                return redirect('dashboard')
            else:
                messages.success(request, f'✅ Welcome back, {user.first_name or user.username}!')
                return redirect('dashboard')
        else:
            messages.error(request, '❌ Invalid username or password.')
    
    context = {
        'has_pending_request': 'website_request_data' in request.session,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    """Custom signup view"""
    from django.contrib.auth import authenticate, login
    from accounts.models import User
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if password != password_confirm:
            messages.error(request, '❌ Passwords do not match.')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ Username already exists.')
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ Email already registered.')
            return render(request, 'signup.html')
        
        if len(password) < 6:
            messages.error(request, '❌ Password must be at least 6 characters.')
            return render(request, 'signup.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        
        # Log them in
        user = authenticate(request, username=username, password=password)
        login(request, user)
        
        # Check if there's pending form data
        if 'website_request_data' in request.session:
            data = request.session.pop('website_request_data')
            website_request = WebsiteRequest.objects.create(
                user=user,
                **data
            )
            messages.success(request, '✅ Account created! Your website request has been saved.')
            return redirect('dashboard')
        else:
            messages.success(request, '✅ Account created successfully!')
            return redirect('dashboard')
    
    context = {
        'has_pending_request': 'website_request_data' in request.session,
    }
    return render(request, 'signup.html', context)


def logout_view(request):
    """Logout user"""
    from django.contrib.auth import logout
    
    logout(request)
    messages.success(request, '✅ You have been logged out.')
    return redirect('request-website')
