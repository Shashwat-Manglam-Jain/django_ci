from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.crypto import get_random_string
import string
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from smtplib import SMTPException
from . import signals
from django.core.signals import request_finished


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        role = request.POST.get('role', 'buyer')
        
        if confirm_password != password:
            messages.error(request, 'Password and confirm password do not match')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            roles=role
        )
        
      
        messages.success(request, 'Your account has been created! You can now log in')
        return redirect('login')
    
    return render(request, 'Register.html', { 'title':'register here'})


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {email}!')
            return redirect('home')
        else:
            messages.info(request, 'Email or password is incorrect')

    return render(request, 'Login.html', {'title':'Log In'})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('login')


def forget_Password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, 'Email is required for password reset')
            return redirect('forget_Password')
        
        try:
            user = User.objects.get(email=email)
            code = get_random_string(32, allowed_chars=string.ascii_lowercase + string.digits)

            request.session[f'reset_code_{email}'] = code
            
            # mail system
            try:
                htmly = get_template('Email.html')
                reset_link = f'http://127.0.0.1:8000/accounts/reset_password/{code}/'
                d = { 'email': email, 'email_type': 'password_reset','reset_link':reset_link }
                subject = 'Password Reset Request'
                from_email = 'shashwat100k@gmail.com'
                to = email
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except:
                pass
            
            messages.success(request, 'Email sent successfully. Please check your email')
        except User.DoesNotExist:
            messages.info(request, 'If email exists, password reset instructions have been sent')
    
    return render(request, 'forget_password.html')


def reset_password(request, code):
    if request.method == 'GET':
        return render(request, 'reset_password.html', {'code': code})
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'reset_password.html', {'code': code})
        
        try:
            email = None
            for key in request.session.keys():
                if key.startswith('reset_code_') and request.session[key] == code:
                    email = key.replace('reset_code_', '')
                    break
            
            if not email:
                messages.error(request, 'Invalid or expired reset code')
                return redirect('forget_Password')
            
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            # Clear the reset code
            try:
                del request.session[f'reset_code_{email}']
            except KeyError:
                pass
            
            messages.success(request, 'Password reset successfully! Please log in')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Error resetting password')
            return redirect('forget_Password')
        



@login_required
def home_view(request):
    return render(request,'index.html')