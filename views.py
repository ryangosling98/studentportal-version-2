from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from .forms import UserRegistrationForm
# from .models import StudentProfile

from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import StudentProfile, Notification

#
# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             login(request, user)
#             return redirect('create_profile')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'portal/register.html', {'form': form})
#
#
# def create_profile(request):
#     if request.method == 'POST':
#         student_id = request.POST.get('student_id')
#         major = request.POST.get('major')
#         gpa = request.POST.get('gpa')
#
#         StudentProfile.objects.create(
#             user=request.user,
#             student_id=student_id,
#             major=major,
#             gpa=gpa
#         )
#         return redirect('profile')
#     return render(request, 'portal/create_profile.html')
#
#
# def profile(request):
#     student_profile = StudentProfile.objects.get(user=request.user)
#     return render(request, 'portal/profile.html', {'profile': student_profile})

def logout_view(request):
    logout(request)
    # messages.success(request, "You have been successfully logged out.")
    return redirect('home')



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