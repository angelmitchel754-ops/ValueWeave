from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Contribution, Confirmation
from .forms import ContributionForm

def home(request):
    contributions = Contribution.objects.filter(status='Confirmed').order_by('-created_at')[:6]
    return render(request, 'home.html', {'contributions': contributions})

def report(request):
    confirmed = Contribution.objects.filter(status='Confirmed')
    total_hours = sum(c.hours for c in confirmed)
    return render(request, 'report.html', {'total': confirmed.count(), 'total_hours': total_hours, 'total_count': confirmed.count()})

@login_required
def dashboard(request):
    my = Contribution.objects.filter(user=request.user).order_by('-created_at')
    total_hours = sum(c.hours for c in my.filter(status='Confirmed'))
    return render(request, 'dashboard.html', {'my': my, 'contributions': my, 'total_hours': total_hours})

@login_required
def add_contribution(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.status = 'Pending'
            c.save()
            return redirect('dashboard')
    else:
        form = ContributionForm()
    return render(request, 'add_contribution.html', {'form': form})

def feed(request):
    contributions = Contribution.objects.filter(status='Confirmed').order_by('-created_at')
    return render(request, 'feed.html', {'contributions': contributions})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def my_profile(request):
    return redirect('profile', username=request.user.username)

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    contributions = Contribution.objects.filter(user=profile_user, status='Confirmed').order_by('-created_at')
    return render(request, 'profile.html', {'profile_user': profile_user, 'contributions': contributions})

@login_required
def coordinator(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    pending = Contribution.objects.filter(status='Pending').order_by('-created_at')
    return render(request, 'coordinator.html', {'pending': pending})

@login_required
def approve(request, pk):
    if request.user.is_staff:
        c = get_object_or_404(Contribution, pk=pk)
        c.status = 'Confirmed'
        c.save()
        Confirmation.objects.create(contribution=c, confirmed_by=request.user, comment='Approved')
    return redirect('coordinator_panel')

@login_required
def reject(request, pk):
    if request.user.is_staff:
        c = get_object_or_404(Contribution, pk=pk)
        c.status = 'Rejected'
        c.save()
    return redirect('coordinator_panel')

def contribute(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        return render(request, 'myapp/thankyou.html', {'name': name})
    return render(request, 'myapp/contribute.html')