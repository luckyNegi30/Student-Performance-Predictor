import joblib
import os
model= joblib.load(os.path.join(os.path.dirname(__file__),'model.pkl'))
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student
from django.contrib.auth.decorators import login_required
from .models import Prediction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json


#-------home page-----------
def home(request):
    return render(request, 'user/home.html')


# ------------REGISTER (data save karega)--------
def register(request):
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        course = request.POST.get('course')
    
        contact = request.POST.get('contact')
        
        if password != confirm_password:
            return render(request, 'user/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'user/register.html', {
                'error': 'Username already exists!'
            })

        
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        Student.objects.create(
            username=username,
            email=email,
            course=course,

            contact=contact
        )

        messages.success(request, "Registered successfully!")
        return redirect('login')

    return render(request, 'user/register.html')

# --------LOGIN (data check karega)--------

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # terminal me----
        print("USERNAME;",username)
        print("PASSWORD;",password)

        user = authenticate(request, username=username, password=password)
        

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid Credentials'})

    return render(request, 'user/login.html')

#---------profile page-------

from django.contrib.auth.decorators import login_required
@login_required
def profile(request):
    student = Student.objects.filter(username=str(request.user)).first()

    return render(request, 'user/profile.html', {
        'user': request.user,
        'student': student
    })

#---------edit profile--------

from django.contrib.auth.decorators import login_required
@login_required
def edit_profile(request):
    user = request.user  
   
    if request.method == "POST":
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        if new_username and new_email:
            user.username = new_username
            user.email = new_email
            user.save()

            messages.success(request, "Profile updated successfully")

        return redirect('profile')

    return render(request, 'user/edit_profile.html', {'user': user})
# ---------------- PREDICT VIEW ----------------

@login_required
def predict(request):
    

    # 👉 GET request → sirf form dikhega
    if request.method == "GET":
        return render(request, 'user/predict.html')

    # 👉 POST request → calculation + save
    elif request.method == "POST":

        # 🔹 Basic Inputs
        study_hours = float(request.POST.get('study_hours', 0))
        attendance = float(request.POST.get('attendance', 0))
        sleep = float(request.POST.get('sleep', 0))

        # 🔹 Academic
        past_performance = int(request.POST.get('past_performance', 1))
        activities = int(request.POST.get('activities', 1))

        # 🔹 Study Habits
        environment = int(request.POST.get('environment', 1))
        method = int(request.POST.get('method', 1))
        participation = int(request.POST.get('participation', 1))
        group_study = int(request.POST.get('group_study', 1))
        tech_use = int(request.POST.get('tech_use', 1))

        # 🔹 Lifestyle
        social = int(request.POST.get('social', 1))
        stress = int(request.POST.get('stress', 1))
        activity = int(request.POST.get('activity', 1))
        nutrition = int(request.POST.get('nutrition', 1))

        #  ML INPUT
        data = [[
            study_hours,
            attendance,
            sleep,
            
        ]]

        #  Prediction
        prediction = model.predict(data)
        score = round(float(prediction[0]), 2)

        # 🎯 Message
        if score > 80:
            message = "Excellent Performance 🎉 Keep it up!"
        elif score > 60:
            message = "Good Performance 👍 You can improve more!"
        else:
            message = "Needs Improvement ⚠ Focus more on studies!"

        #  SAVE DATA (FIXED)
        Prediction.objects.create(
            user=request.user,
            study_hours=study_hours,
            attendance=attendance,
            past_performance=str(past_performance),
            extracurricular=str(activities),
            result=str(score)
        )
        print("DATA SAVED")

        # Result page pe bhejna
        
    return render(request,'user/result.html', {
    'score': score,
    'message': message,

    # ALL INPUTS
    'study_hours': study_hours,
    'attendance': attendance,
    'sleep': sleep,
    'past_performance': past_performance,
    'activities': activities,
    'environment': environment,
    'method': method,
    'participation': participation,
    'group_study': group_study,
    'tech_use': tech_use,
    'social': social,
    'stress': stress,
    'activity': activity,
    'nutrition': nutrition
})
            
        

# ---------------- RESULT VIEW ----------------

def result(request):
    if request.method == "POST":

        # 🔹 Basic
        study_hours = float(request.POST.get('study_hours', 0))
        attendance = float(request.POST.get('attendance', 0))
        sleep = float(request.POST.get('sleep', 0))

        # 🔹 Academic
        past_performance = int(request.POST.get('past_performance', 1))
        activities = int(request.POST.get('activities', 1))

        # 🔹 Study
        environment = int(request.POST.get('environment', 1))
        method = int(request.POST.get('method', 1))
        participation = int(request.POST.get('participation', 1))
        group_study = int(request.POST.get('group_study', 1))
        tech_use = int(request.POST.get('tech_use', 1))

        # 🔹 Lifestyle
        social = int(request.POST.get('social', 1))
        stress = int(request.POST.get('stress', 1))
        activity = int(request.POST.get('activity', 1))
        nutrition = int(request.POST.get('nutrition', 1))

        # 🔥 ML input (IMPORTANT)
        data = [[study_hours, attendance, sleep]]

        prediction = model.predict(data)
        score = round(float(prediction[0]), 2)
        score= max(0,min(100,round(score)))

        # 🎯 message
        if score > 80:
            message = "Excellent Performance 🎉 Keep it up!"
            
        elif score > 60:
            message = "Good Performance 👍 You can improve more!"
            
        else:
            message = "Needs Improvement"
           

        

        return render(request,'user/result.html', {
            "score": score,
            "message": message,
            
            # display data
            "study_hours": study_hours,
            "attendance": attendance,
            "sleep": sleep,
            "past_performance": past_performance,
            "activities": activities,
            "environment": environment,
            "method": method,
            "participation": participation,
            "group_study": group_study,
            "tech_use": tech_use,
            "social": social,
            "stress": stress,
            "activity": activity,
            "nutrition": nutrition,
        })
    request.session['dashboard_data'] = {
    "score": score,
    "study_hours": study_hours,
    "attendance": attendance,
    "sleep": sleep
}

    return redirect('dashboard')


#--------dashboard--------  
from django.shortcuts import render
from .models import Prediction 
import json


import json

def dashboard(request):

    predictions = Prediction.objects.filter(user=request.user)
    total_predictions = predictions.count()

    if total_predictions > 0:
        last_prediction = predictions.last()

        last_score = last_prediction.result
        last_date = last_prediction.timestamp

        total_score = sum(float(p.result) for p in predictions)
        avg_score = round(total_score / total_predictions, 2)

    
        labels = ["Attendance", "Past Performance", "Study Hours",]
        
        scores = [
            float(last_prediction.attendance) if last_prediction.attendance else 0,
            float(last_prediction.study_hours) if last_prediction.study_hours else 0,
            float(last_prediction.past_performance) if last_prediction.past_performance else 0
        ]
        

    else:
        last_score = None
        avg_score = None
        last_date = None
        labels = []
        scores = []

    context = {
        'last_score': last_score,
        'total_predictions': total_predictions,
        'avg_score': avg_score,
        'last_date': last_date,
        'labels': json.dumps(labels),
        'scores': json.dumps(scores)
    }

    return render(request, 'user/dashboard.html', context)
#------- history------
@login_required
def history(request):
    data = Prediction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'user/history.html', {'data': data})

#--------logout-------
from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    return redirect('login')



#------admin panel-----
#admin login------
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(request, username=username, password=password)
        

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_panel/admin_login.html', {'error': 'Invalid Credentials'})

    return render(request, 'admin_panel/admin_login.html')

#------admin dashboard-----
from django.utils import timezone
from datetime import timedelta

from .models import Prediction
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def admin_dashboard(request):

    # 👉 Latest predictions (top 10)
    predictions = Prediction.objects.select_related('user').order_by('-id')[:10]

    # 👉 Add Good / Bad status dynamically
    for p in predictions:
        if p.result >= 50:
            p.status = "Good"
        else:
            p.status = "Bad"

    # 👉 Total counts
    total_students = User.objects.count()
    total_predictions = Prediction.objects.count()

    # 👉 Today / Yesterday counts
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    today_count = Prediction.objects.filter(timestamp__date=today).count()
    yesterday_count = Prediction.objects.filter(timestamp__date=yesterday).count()

    # 👉 Good / Bad count for chart
    pass_count = Prediction.objects.filter(result__gte=50).count()
    fail_count = Prediction.objects.filter(result__lt=50).count()

    # 👉 Send all data to template
    context = {
        'predictions': predictions,
        'total_students': total_students,
        'total_predictions': total_predictions,
        'today_count': today_count,
        'yesterday_count': yesterday_count,
        'pass_count': pass_count,
        'fail_count': fail_count
    }

    return render(request, 'admin_panel/admin_dashboard.html', context)
# 👉 VIEW SINGLE RECORD
def view_prediction(request, id):
    data = get_object_or_404(Prediction, id=id)


    return render(request, 'user/result.html', {
        
        'p':data
    })
from django.http import JsonResponse
from .models import Prediction

def view_result_ajax(request, id):
    student = student.objects.get(id=id)

    data = {
        "prediction": student.prediction  
    }

    return JsonResponse(data)

# 👉 DELETE RECORD
def delete_prediction(request, id):
    data = get_object_or_404(Prediction, id=id)
    data.delete()
    return redirect('admin_dashboard')



def delete_history(request):
    if request.method == "POST":
        Prediction.objects.all().delete()
    return redirect('history')