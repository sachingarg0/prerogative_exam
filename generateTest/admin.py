from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Test)

class stackedAnswer(admin.StackedInline):
    model= Answers

class stackedQuestion(admin.ModelAdmin):
    inlines=[stackedAnswer]

admin.site.register(Questions,stackedQuestion)
admin.site.register(Answers)
admin.site.register(Student)


