from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, Feedback
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def FileUploading(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "fileupload.html", {"error": "Invalid credentials"})

    return render(request, 'fileupload.html')

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        company = request.POST.get("company")
        
        if User.objects.filter(email=email).exists():
            return render(request, "login.html", {"error": "Email already exists"})
    
        user = User.objects.create_user(email=email, password=password, name=first_name, company=company)
        user.save()

        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'login.html')

@login_required
def Home(request):
    return render(request, 'navbar.html')

@login_required
def how(request):
    return render(request, 'how.html')

def getFeedbackMessage(value):
    if value <= 30:
        return "Strongly Dislike"
    elif value <= 50:
        return "Dislike"
    elif value <= 70:
        return "Neutral"
    elif value <= 90:
        return "Like"
    else:
        return "Love"

@login_required
def feedback(request):
    feed = Feedback.objects.all()
    if request.method == 'POST':
        demo_rating_value = int(request.POST.get('demo_rating', 4))
        subject = request.POST.get('subject', '')
        feedback_text = request.POST.get('feedback', '')
        email = request.POST.get('email', '')
        future_projects_rating = int(request.POST.get('future_projects_rating', 1))

        feedback_message = getFeedbackMessage(demo_rating_value)
        feedback = Feedback(
            demo_rating=feedback_message, 
            subject=subject,
            feedback_text=feedback_text,
            email=email,
            future_projects_rating=future_projects_rating
        )
        feedback.save()

    return render(request, "feedback.html")

@login_required
def excercise(request):
    return render(request, 'excercise.html')
