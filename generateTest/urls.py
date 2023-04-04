
from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path('login',views.login_user,name='login_user'),
    path('logout',views.logout_user,name='logout_user'),
    path('activeTest/<int:quiz_id>/<int:student_id>',views.Activetest,name='activeTest'),
    path('result/', views.viewResult, name='view-result'),
    path('dashboard',views.Dashboard,name='dashboard'),
    path('del/<int:quiz_id>',views.DelQuiz,name='del_quiz'),
    path('edit/<int:quiz_id>',views.Edit,name='edit'),
    path('createTest',views.Createtest,name='createTest'),
    path('studentDetails/<int:quiz_id>',views.Details,name='studentDetails'),
    path('verify/<int:quiz_id>/<int:student_id>/<str:token>',views.Verify,name='verify'),
    path('viewResponses/<int:quiz_id>',views.viewResponses,name='viewResponses'),
    path('downloadCSV/<int:quiz_id>',views.down_csv,name='downloadCSV'),
    path('viewMessage/<str:message>',views.viewMessage,name='viewMessage')
    
]