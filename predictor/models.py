from django.db import models
# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)


from django.contrib.auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    study_hours = models.FloatField()
    attendance = models.FloatField()
    past_performance = models.CharField(max_length=50)
    extracurricular = models.CharField(max_length=50)

    
    result = models.FloatField() 

    
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.user.username
    
    from django.db import models



    

    