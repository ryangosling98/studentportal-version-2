# studentportal-version-2

added a user page  login logout functionalitry   improved asthetics    
also added a notification model 

Login Functionality (10-15 minutes):

Enhanced User Profile (10-15 minutes):

Notification System (15-20 minutes):

Home Page and Navigation (5-10 minutes):

# Step 1: Add login functionality

1. Update portal/urls.py:
```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
]
```

2. Create a new template portal/templates/portal/login.html:
```html
{% extends 'portal/base.html' %}

{% block content %}
<h2>Login</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>
<p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
{% endblock %}
```

3. Create a base template portal/templates/portal/base.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudentPortal</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        nav { background: #333; padding: 10px; }
        nav a { color: #fff; text-decoration: none; padding: 10px; }
        .container { max-width: 800px; margin: auto; padding: 20px; }
        .notification { background: #f4f4f4; padding: 10px; margin-bottom: 10px; border-left: 4px solid #333; }
    </style>
</head>
<body>
    <nav>
        <a href="{% url 'home' %}">Home</a>
        {% if user.is_authenticated %}
            <a href="{% url 'profile' %}">Profile</a>
            <a href="{% url 'logout' %}">Logout</a>
        {% else %}
            <a href="{% url 'login' %}">Login</a>
            <a href="{% url 'register' %}">Register</a>
        {% endif %}
    </nav>
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```

# Step 2: Enhance user profile and add notifications

4. Update portal/models.py to include a Notification model:
```python
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)
    major = models.CharField(max_length=100)
    gpa = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}..."
```

5. Update portal/views.py:
```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import StudentProfile, Notification

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            Notification.objects.create(user=user, message="Welcome to StudentPortal! Please complete your profile.")
            return redirect('create_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'portal/register.html', {'form': form})

@login_required
def create_profile(request):
    if hasattr(request.user, 'studentprofile'):
        return redirect('profile')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        major = request.POST.get('major')
        gpa = request.POST.get('gpa')
        
        StudentProfile.objects.create(
            user=request.user,
            student_id=student_id,
            major=major,
            gpa=gpa
        )
        Notification.objects.create(user=request.user, message="Your profile has been created successfully!")
        return redirect('profile')
    return render(request, 'portal/create_profile.html')

@login_required
def profile(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'portal/profile.html', {'profile': student_profile, 'notifications': notifications})

def home(request):
    return render(request, 'portal/home.html')
```

6. Update portal/templates/portal/profile.html:
```html
{% extends 'portal/base.html' %}

{% block content %}
<h2>Student Profile</h2>
<p>Username: {{ profile.user.username }}</p>
<p>Student ID: {{ profile.student_id }}</p>
<p>Major: {{ profile.major }}</p>
<p>GPA: {{ profile.gpa }}</p>

<h3>Recent Notifications</h3>
{% for notification in notifications %}
    <div class="notification">
        {{ notification.message }}
        <small>({{ notification.created_at|date:"F d, Y H:i" }})</small>
    </div>
{% empty %}
    <p>No notifications.</p>
{% endfor %}
{% endblock %}
```

7. Create portal/templates/portal/home.html:
```html
{% extends 'portal/base.html' %}

{% block content %}
<h1>Welcome to StudentPortal</h1>
{% if user.is_authenticated %}
    <p>Hello, {{ user.username }}!</p>
    <p><a href="{% url 'profile' %}">View your profile</a></p>
{% else %}
    <p>Please <a href="{% url 'login' %}">login</a> or <a href="{% url 'register' %}">register</a> to access your profile.</p>
{% endif %}
{% endblock %}
```

8. Update other templates to extend from base.html:
   - Update register.html, create_profile.html to extend from 'portal/base.html' like the login.html example.

9. Run migrations for the new Notification model:
```
python manage.py makemigrations
python manage.py migrate
```

10. Update StudentPortal/settings.py to include login redirect:
```python
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
