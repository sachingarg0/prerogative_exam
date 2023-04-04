from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class BaseModel(models.Model):
    id=models.AutoField(primary_key=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)

    class Meta:
        abstract=True

class Test(BaseModel):
    name=models.CharField(max_length=255,unique=True)
    summary=models.TextField()
    duration=models.DurationField()
    accepting_response= models.BooleanField(default=True)
    mutli_response= models.BooleanField(default=False)
    # responses

    def __str__(self):
        return self.name
# class Images(BaseModel):    
#     image=models.ImageField(upload_to="questionImages")
    
class Questions(BaseModel):
    test_id=models.ForeignKey(Test,related_name="test", on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    marks=models.IntegerField()
    # image_url= models.ForeignKey(Images, on_delete=models.SET_NULL, null=True)

    # image_url = models.URLField()
    def __str__(self):
        return self.name
    


class Answers(BaseModel):
    question_id=models.ForeignKey(Questions,related_name='question',on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    is_correct=models.BooleanField(max_length=100)
    def __str__(self):
        return self.name


class Student(BaseModel):    
    test_id=models.ForeignKey(Test,related_name="Student_test" ,on_delete=models.CASCADE)   
    name=models.CharField(max_length=100)
    father_name=models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # gender
    dob = models.DateField()
    phone_number = models.CharField(max_length=20)    
    marks=models.IntegerField(default=0)
    email_token=models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    test_complete = models.BooleanField(default=False)
    def __str__(self):
        return self.name




# class Responses(BaseModel):
#     test_id=
#     student_details=
#     marks=
    








