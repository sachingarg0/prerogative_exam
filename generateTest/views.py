from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate ,logout ,login,get_user_model
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random,csv,uuid
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from datetime import timedelta
from .models import*

def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user != None:
            login(request, user)
            return redirect('dashboard')

    context={'form':form}
    return render (request ,'generateTest/login.html' ,context )

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='/login')
def Dashboard(request):
    search_query = request.GET.get('search_query')
    if search_query:
        quizzes = Test.objects.filter(name__icontains=search_query)
    else:
        quizzes = Test.objects.all()
    return render(request, 'generateTest/dashboard.html',{"quizzes":quizzes,"link":"http://127.0.0.1:8000/studentDetails/"})

def storeQA(request,quiz,no_of_prevques):
        questions= request.POST.getlist('question[]')
        number=request.POST.getlist('question_number[]')
        print(questions)
        print("no",number)
        mark=request.POST.getlist('marks[]')
        l=len(questions)

        for q in range(0,l):
         question=Questions.objects.create(test_id=quiz,name=questions[q],marks=mark[q])
         print("q",questions[q])

         
         options=request.POST.getlist(f'question_{number[q]}_option_[]')
         print(options)
         correct=request.POST.getlist(f'question_{number[q]}_correct_[]')
         o_l=len(options)

         for a in range(0,o_l):
            correct_opt = str(a) in correct
            Answers.objects.create(question_id=question,name=options[a],is_correct=correct_opt) 
       

@login_required(login_url='/login')
def Createtest(request):

    if request.method=="POST":
            test_name=request.POST.get('title')
            test_summary=request.POST.get('summary')
            # test_duration=request.POST.get('duration')
            h = int(request.POST.get("Hrs"))
            m = int(request.POST.get("Mins"))
            s = int(request.POST.get("Secs"))
            test_duration=timedelta(hours=h, minutes=m, seconds=s)      
            quiz=Test.objects.create(name=test_name,summary=test_summary,duration=test_duration)
           
            storeQA(request,quiz,0)
            return redirect(reverse('edit', args=[quiz.id])) 
             

    return render(request, 'generateTest/createTest.html',{'no_of_ques':0,})

@login_required(login_url='/login')
def DelQuiz(request,quiz_id):
    q_del=Test.objects.get(id=quiz_id)
    q_del.delete()
    return redirect('dashboard') 

@login_required(login_url='/login')
def Edit(request,quiz_id):
    quiz=Test.objects.get(id=quiz_id)
    duration=quiz.duration.total_seconds()   
    link=f'https://preogative.in/exam/studentDetails/{quiz_id}'
    h=int(duration // 3600)
    m=int((duration % 3600) // 60)
    s=int(duration % 60)
    
    questions = Questions.objects.filter(test_id=quiz)
    no_of_q=len(questions)
    question_answers=[]
    for q in questions:
        options=Answers.objects.filter(question_id=q)       
        question_answers.append({'question': q, 'answers': options}) 

    if request.method=='POST':
        change=0
        # questions = Questions.objects.filter(test_id=quiz)        
        title=request.POST.get('title')
        summary=request.POST.get('summary')
        hr = int(request.POST.get("Hrs"))
        mi = int(request.POST.get("Mins"))
        se = int(request.POST.get("Secs"))
        if(title!=quiz.name):
            change=1
            quiz.name=title
        if (summary != quiz.summary):
            change=1
            quiz.summary=summary
        if (hr!=h or mi!=m or se!=s): 
            change=1
            quiz.duration=timedelta(hours=hr, minutes=mi, seconds=se)  
        if(change==1):
            quiz.save()


        edit_questions= request.POST.getlist('edit_question[]')
        edit_qid=request.POST.getlist('edit_qid[]')       
        edit_mark=request.POST.getlist('edit_marks[]')
        number=request.POST.getlist('edit_question_number[]')
        print("num",number)
        print("ed",edit_questions)
        
       
        for x in range(len(questions)):
                if( not str(questions[x].id) in edit_qid):
                    q_del=questions.filter(id=questions[x].id)
                    q_del.delete()
            
        
            
        for x in range(len(edit_questions)):
                questions.filter(id=edit_qid[x]).update(name=edit_questions[x], marks=edit_mark[x])
                    

        for i in range(len(edit_questions)):            
            edit_options=request.POST.getlist(f'edit_question_{number[i]}_option_[]')
            edit_correct=request.POST.getlist(f'edit_question_{number[i]}_correct_[]')           
            option_id=request.POST.getlist(f'edit_question_{number[i]}_optionid_[]')
            print(edit_options)
            print("oid",option_id)
            
            
            questions = Questions.objects.filter(test_id=quiz)   
            # for q in questions:
            options=Answers.objects.filter(question_id=questions[i])
            print(options)
            for x in range(len(options)):
                    if( not str(options[x].id) in option_id):
                        print(options[x].id,"=")
                        o_del=options.filter(id=options[x].id)
                        # print(o_del)
                        o_del.delete()

            original_opt_l=len(option_id)
            new_opt_l=len(edit_options)           
            for o in range(len(option_id)):     
                correct_opt = str(option_id[o]) in edit_correct   
                Answers.objects.filter(id=option_id[o]).update(name=edit_options[o],is_correct=correct_opt)
            for o in range(original_opt_l,new_opt_l):
                correct_opt = str(o) in edit_correct
                Answers.objects.create(question_id=questions[i],name=edit_options[o],is_correct=correct_opt)
       
        storeQA(request,quiz,len(questions))
        return redirect(reverse('edit', args=[quiz.id]))


    context={'quiz':quiz,'QA':question_answers,'no_of_ques':no_of_q,
             "hrs":h,"min":m,"sec":s,'link':link}
    return render(request, 'generateTest/createTest.html',context)



def Details(request,quiz_id):
    quiz=Test.objects.get(id=quiz_id)
    if(not quiz.accepting_response):
        return redirect('viewMessage',message="Sorry! We are no longer accepting any response")
    form = StudentForm(request.POST or None)
    if form.is_valid():
        # if not quiz.mutli_response and Student.objects.get(email=form.email):
        #     return redirect('view-result')
        obj=form.save(commit=False) 
        obj.email_token=str(uuid.uuid4())
        obj.test_id=quiz
        obj.save()
        print(obj.email_token,"++++",obj.id)
        sendMail(obj.email, obj.email_token,quiz_id,obj.id) 
        return redirect('viewMessage',message="Please verify yourself, Check your Email!")

    context={'form':form}
    return render(request , 'generateTest/studentDetail.html',context)

# def imageupload

def Verify(request,student_id,quiz_id,token):
    try:
        obj=Student.objects.get(email_token=token)
        obj.is_verified=True
        obj.save()
        return redirect(f'/activeTest/{quiz_id}/{student_id}')  
    
    except Exception as e:
        return HttpResponse('You are not Verified') 



def Activetest(request,student_id,quiz_id):
    
    student=Student.objects.get(id=student_id)
    if(student.test_complete):
        return redirect('viewMessage',message="You already completed your test!")
    if(not student.is_verified):
        return redirect('viewMessage',message="You are not Verified!")


    quiz=Test.objects.get(id=quiz_id)
    time= quiz.duration.total_seconds()
    questions = list(Questions.objects.filter(test_id=quiz))
    random.shuffle(questions)
    question_answers=[]
    correct = 0
    unanswered=0
    incorrect=0
    score=0
    total_score=0
    for i in questions:
      answers = list(Answers.objects.filter(question_id=i))
      random.shuffle(answers)
      question_answers.append({'question': i, 'answers': answers})    

    if request.method == 'POST':
        # test = request.POST.get('test_id')
        # print(test_id)
        total=len(questions)
        for question in questions:           
            selected_answer_id = request.POST.get(str(question.id))
            total_score+=question.marks
            if selected_answer_id:
                selected_answer = Answers.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    correct += 1
                    score += question.marks
            else:
                unanswered +=1            
                messages.error(request, f'Question "{question.name}" was not answered')
        student.test_complete=True
        student.marks=score
        student.save()        
        incorrect+=(total-unanswered)-correct
        return redirect('view-result')
    context = {'test': quiz,
                'question_answers': question_answers,
                "correct":correct,"unanswered":unanswered,
                "incorrect":incorrect,
                "score":score,'time':time}
    return render(request, 'generateTest/activeTest.html', context)

def viewResult(request):
    return render(request, 'generateTest/result.html')

def viewMessage(request,message):
    return render(request, 'generateTest/messages.html', {'message':message})




def sendMail(email, token, quiz_id, student_id):
    try:
        subject = 'Verify Your Email'
        
        
        html_content = render_to_string('generateTest/email.html', {'token': token, 'quiz_id': quiz_id, 'student_id': student_id})
        
        text_content = strip_tags(html_content)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        email = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        
        email.attach_alternative(html_content, "text/html")
        
        email.send()
    
        return True
    
    except Exception as e:
        print(e)
        return False

@login_required(login_url='/login')
def viewResponses(request,quiz_id):
    student_list = Student.objects.filter(test_id=quiz_id)
    quiz=Test.objects.get(id=quiz_id)
    link=f'https://preogative.in/exam/studentDetails/{quiz_id}' 
    print(student_list)
    paginator = Paginator(student_list, 1) # Show 10 students per page
    page = request.GET.get('page')
    students = paginator.get_page(page)
    if request.method=='POST':
        form=request.POST.get('form')
        if form=='accept':
            acceptResponse=request.POST.get('acceptResponse')
            if acceptResponse=='on':
                acceptResponse=True
            else:
                acceptResponse=False
            quiz.accepting_response=acceptResponse
        else:
            multiResponse=request.POST.get('multiResponse')
            if multiResponse=='on':
                multiResponse=True
            else:
                multiResponse=False
            quiz.mutli_response=multiResponse
        quiz.save()
        


    context = {
        'students': students,'total_responses':len(student_list),
        'quiz':quiz,'link':link
    }
    return render(request, 'generateTest/responses.html', context)

@login_required(login_url='/login')
def down_csv(request,quiz_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Father Name', 'Email', 'Date of Birth', 'Phone Number', 'Marks'])

    students = Student.objects.filter(test_id=quiz_id)
   
    for student in students:
        writer.writerow([student.name,student.father_name,student.email,student.dob,student.phone_number,student.marks])

    return response