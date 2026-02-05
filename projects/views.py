from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import WebsiteRequestForm, ContactForm
from .models import WebsiteRequest
from .services import send_website_request_email, send_website_request_confirmation, send_contact_form_email


def landing(request):
    """Landing page for Arka"""
    # Dynamic stats
    total_projects = WebsiteRequest.objects.count()
    active_projects = WebsiteRequest.objects.exclude(status='completed').count()
    happy_clients = WebsiteRequest.objects.filter(status='completed').count()

    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'happy_clients': happy_clients,
    }
    return render(request, 'landing.html', context)


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
                
                # Send email to admin (non-blocking)
                try:
                    user_info = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
                    send_website_request_email(
                        business_name=website_request.business_name,
                        email=website_request.email,
                        website_type=website_request.get_website_type_display(),
                        description=website_request.description,
                        budget=website_request.budget,
                        is_logged_in=True,
                        user_info=user_info
                    )
                except Exception as e:
                    print(f"Email sending error (non-blocking): {str(e)}")
                
                # Send confirmation email to client
                try:
                    send_website_request_confirmation(website_request.email, website_request.business_name)
                except Exception as e:
                    print(f"Confirmation email error (non-blocking): {str(e)}")
                
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


@require_http_methods(["GET", "POST"])
def contact(request):
    """Handle contact form submissions"""
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send email to admin (non-blocking)
            email_sent = send_contact_form_email(name, email, message)
            
            if email_sent:
                messages.success(request, '✅ Your message has been sent! We will get back to you soon.')
            else:
                # Still show success to user, but log the error server-side
                messages.success(request, '✅ Your message has been received! We will get back to you soon.')
            
            return redirect('contact')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)



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
                
                # Send email to admin (non-blocking)
                try:
                    user_info = f"{user.first_name} {user.last_name}".strip() or user.username
                    send_website_request_email(
                        business_name=website_request.business_name,
                        email=website_request.email,
                        website_type=website_request.get_website_type_display(),
                        description=website_request.description,
                        budget=website_request.budget,
                        is_logged_in=True,
                        user_info=user_info
                    )
                except Exception as e:
                    print(f"Email sending error (non-blocking): {str(e)}")
                
                # Send confirmation email to client
                try:
                    send_website_request_confirmation(website_request.email, website_request.business_name)
                except Exception as e:
                    print(f"Confirmation email error (non-blocking): {str(e)}")
                
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
            
            # Send email to admin (non-blocking)
            try:
                user_info = f"{user.first_name} {user.last_name}".strip() or user.username
                send_website_request_email(
                    business_name=website_request.business_name,
                    email=website_request.email,
                    website_type=website_request.get_website_type_display(),
                    description=website_request.description,
                    budget=website_request.budget,
                    is_logged_in=True,
                    user_info=user_info
                )
            except Exception as e:
                print(f"Email sending error (non-blocking): {str(e)}")
            
            # Send confirmation email to client
            try:
                send_website_request_confirmation(website_request.email, website_request.business_name)
            except Exception as e:
                print(f"Confirmation email error (non-blocking): {str(e)}")
            
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
