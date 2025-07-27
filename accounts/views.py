#views.py
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PlayerRecord, GameSession, UserProfile
from django.db.models import Max, Min, Sum
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request,'base.html')

def how_to_play_page(request):
    return render(request,'rules.html')

def news_page(request):
    return render(request,'news.html')

@login_required(login_url='/login/')
def download_page(request):
    return render(request,'download.html')

@login_required(login_url='/login/')
def contact_page(request):
    if request.method == 'POST':
        username = request.user.username
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f'New Contact Form Submission from {name}'
        message_body = f"""
Username: {username}
Full Name: {name}
Email: {email}
Message:
{message}
"""

        try:
            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Sending to registered email address
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f'Sorry, error sending your message: {e}')

        return redirect('contact-html')  # Redirect after POST to avoid resubmission

    return render(request, 'contact.html')

def forgotpass_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        subject = f'Reset Password Request {username}'
        message_body = f"""
Username: {username}
Email: {email}
"""

        try:
            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Sending to registered email address
                fail_silently=False,
            )
            messages.success(request, 'Success! Reset details will be sent to your signup email after verification.')
        except Exception as e:
            messages.error(request, f'Sorry, error sending your message: {e}')

        return redirect('forgotpass-html')  # Redirect after POST to avoid resubmission

    return render(request, 'forgotpass.html')

@login_required(login_url='/login/')
def changepassword_logic(request):
    if request.method == 'POST':
        prev_password = request.POST.get('prev_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_new_password')
        user = request.user

        if not user.check_password(prev_password):
            messages.error(request, "Previous password is incorrect.")
        elif not new_password or not confirm_password:
            messages.error(request, "Please fill in both fields.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('dashboard-html') 

    return render(request, 'changepassword.html')



@login_required(login_url='/login/')
def dashboard_page(request):
    user = request.user
    username = user.username

    # All Sessions played by the user
    sessions = GameSession.objects.filter(username=username)

    # Games played
    games_played = sessions.count()

    # Highest level reached
    highest_level = sessions.aggregate(Max('level_reached'))['level_reached__max'] or 0

    # Fastest Time
    fastest_time = sessions.aggregate(Min('time_taken'))['time_taken__min'] or 0

    # Calculate average time per level:
    # total_time / total_levels across all sessions
    sessions_with_levels = sessions.filter(level_reached__gt=0)

    total_time = sessions_with_levels.aggregate(Sum('time_taken'))['time_taken__sum'] or 0
    total_levels = sessions_with_levels.aggregate(Sum('level_reached'))['level_reached__sum'] or 1  # avoiding div by zero

    average_level_time = round(total_time / total_levels, 2) if total_levels else 0

    # Current rank
    leaderboard = PlayerRecord.objects.all().order_by('-level_reached', 'time_taken')
    current_rank = None
    for i, entry in enumerate(leaderboard, start=1):
        if entry.username == username:
            current_rank = i
            break

    highest_rank = current_rank or "—"

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'user_profile': profile,
        'games_played': games_played,
        'highest_level': highest_level,
        'fastest_time': round(fastest_time, 2),
        'average_time': average_level_time,
        'current_rank': current_rank or "—",
        'highest_rank': highest_rank,
        'user': user,
    }

    return render(request, 'dashboard.html', context)

@login_required
def set_description(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        description = request.POST.get('description', '')
        profile.description = description
        profile.save()
        messages.success(request, "Description updated!")
        return redirect('dashboard-html') 

    return render(request, 'description.html', {
        'user_profile': profile
    })

def leaderboard_page(request):
    records = PlayerRecord.objects.all().order_by('-level_reached', 'time_taken')

    leaderboard = []
    for record in records:
        user = User.objects.filter(username=record.username).first()
        profile = UserProfile.objects.filter(user=user).first() if user else None

        leaderboard.append({
            'username': record.username,
            'description': profile.description if profile else "",
            'time_taken': record.time_taken,
            'level_reached': record.level_reached,
            'input_used': record.input_used,
        })

    return render(request, 'leaderboard.html', {'leaderboard': leaderboard})

def about_page(request):
    return render(request,'about.html')

def privacy_page(request):
    return render(request,'privacy.html')

def terms_page(request):
    return render(request,'terms.html')

def login_page(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard-html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password', 'next': next_url})

    return render(request, 'login.html', {'next': next_url})


def signup_page(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'email already exists for a different account'})
        
        if confirm != password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        return redirect('/login')

    return render(request, 'signup.html')


def logout_page(request):
    logout(request)
    return redirect('/')


# REST API Views (for Python game and web)

@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({'status': 'success', 'message': 'Login successful'})
    else:
        return Response({'status': 'error', 'message': 'Invalid username or password'}, status=401)
    

@api_view(['POST'])
def submit_score(request):
    username = request.data.get('username')
    time_taken = float(request.data.get('time_taken'))
    level_reached = int(request.data.get('level_reached'))
    input_used = request.data.get('input_used')

    try:
        record = PlayerRecord.objects.get(username=username)

        if level_reached > record.level_reached:
            record.level_reached = level_reached
            record.time_taken = time_taken
            record.input_used = input_used
            record.save()
            message = 'Record updated (better level)!'
        
        elif level_reached == record.level_reached and time_taken < record.time_taken:
            record.time_taken = time_taken
            record.input_used = input_used
            record.save()
            message = 'Record updated (faster time)!'
        
        else:
            message = 'No update. Previous record is better.'

    except PlayerRecord.DoesNotExist:
        PlayerRecord.objects.create(
            username=username,
            time_taken=time_taken,
            level_reached=level_reached,
            input_used=input_used
        )
        message = 'New player record created!'

    print("Saving GameSession now...")
    GameSession.objects.create(
        username=username,
        time_taken=time_taken,
        level_reached=level_reached,
    )

    return Response({'message': message}, status=201)