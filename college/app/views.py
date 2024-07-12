from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login
from .models import Course,Student,Teacher
import os
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def landingpage(request):
    return render(request,'landingpage.html')
def teachercard(request):
    tchr=Teacher.objects.get(user=request.user)
    cr=Course.objects.all()
    return render(request,'teachercard.html',{'tcr':tchr,'csr':cr})
def signupteachers(request):
    course=Course.objects.all()
    return render(request,'signupteachers.html',{'crse':course})
    
def teacherhome(request):
       if 'user' in request.session:
        return render(request, 'teacherhome.html')
       else:
        query_params = {'error': 'access_denied'}
        url = '{}?{}'.format(reverse('landingpage'), urlencode(query_params))
        return redirect(url)
    
def user_sign(request): 
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        username=request.POST['uname']
        addr=request.POST['add']
        ag=request.POST['age']
        email=request.POST['email']
        ph=request.POST['pn']
        password=request.POST['pass']
        cpassword=request.POST['cnpass']
        im=request.FILES.get('img')
        cou=request.POST['c']
        
        
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'This username already exists')
                return redirect('signupteachers')
            else:
                user=User.objects.create_user(first_name=first_name,
                                              last_name=last_name,
                                              username=username,
                                              password=password,
                                              email=email)
                user.save()
                use=Course.objects.get(id=cou)
                u=User.objects.get(id=user.id)
                reg=Teacher(address=addr,age=ag,phone=ph,image=im,user=u,course=use)
                reg.save()
                return redirect('teacherlogin')

        else:
            messages.info(request,'Password doesnot match')
            return redirect('signupteachers')       
    else:
        return render(request,'homepage.html')




@login_required(login_url='landingpage')
def adminhome(request):
    if request.user.is_staff:
        return render(request,'adminhome.html')
    else:
        query_params = {'adminhome': 'access_denied'}
        url = '{}?{}'.format(reverse('landingpage'), urlencode(query_params))
        return redirect(url)
def adminaddcrs(request):
    if request.user.is_staff:
    
        return render(request,'adminaddcrs.html')
    else:
        query_params = {'adminhome': 'access_denied'}
        url = '{}?{}'.format(reverse('landingpage'), urlencode(query_params))
        return redirect(url)
    
def loginfnc(request):
        if request.method == 'POST':
            username = request.POST['usname']
            password = request.POST['passd']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_authenticated:  # Check if the user is authenticated
                    if user.is_staff:
                        login(request, user)
                        request.session['user'] = user.username  # Set user session variable
                        return redirect('adminhome')
                    else:
                        login(request, user)
                        request.session['user'] = user.username  # Set user session variable
                        messages.info(request, f'Welcome {user}')
                        return redirect('teacherhome')  # Redirect to techhome after login
                else:
                    messages.info(request, 'Invalid Username or Password')
                    return redirect('landingpage')
            else:
                messages.info(request, 'Invalid Username or Password')
                return redirect('landingpage')
        return render(request, 'landingpage.html')


def add_course(request):
    if request.method=='POST':
        cname=request.POST['course']
        fe=request.POST['fees']
        sp=Course(coursename=cname,fees=fe)
        sp.save()
        return redirect('adminaddstd')
def adminaddstd(request):
    st=Course.objects.all()
    
    return render(request,'adminaddstd.html',{'crs':st})

@login_required(login_url='homepage')
def addstd_details(request):
    if request.method=='POST':
        nam=request.POST['name']
        add=request.POST['address']
        ag=request.POST['age']
        dt=request.POST['date']
        dp=request.POST['c']
        cc=Course.objects.get(id=dp)
        std=Student(studentname=nam,address=add,age=ag,joiningdate=dt,course=cc)
        std.save()
        return redirect('stddetails')
def stddetails(request):
    student=Student.objects.all()
    
    return render(request,'stddetails.html',{'stu':student})

def stdedit(request,pk):
    std=Student.objects.get(id=pk)
    c=Course.objects.all()
    

    return render(request,'stdedit.html',{'stu':std,'crs':c})

def editdetails(request,pk):
    if request.method=='POST':
        ss=Student.objects.get(id=pk)
        ss.studentname=request.POST['name']
        ss.address=request.POST['add']
        ss.age=request.POST['age']
        ss.joiningdate=request.POST['doj']
        co=request.POST['coursename']
        
        course1=Course.objects.get(id=co)
        
        course1.save()
        ss.course=course1
        ss.save()
        return redirect('stddetails')
    return render(request,'stdedit.html')

def delete(request,pk):
    student=Student.objects.get(id=pk)
    student.delete()
    return redirect('stddetails')
    

def teacherlogin(request):
    return render(request,'teacherlogin.html')


    
def teacheredit(request):
    tchr=Teacher.objects.get(user=request.user)
    cr=Course.objects.all()
    return render(request,'teacheredit.html',{'tea':tchr,'csr':cr})

def tchr_edit(request,id):
    if request.method=='POST':
        t=Teacher.objects.get(user=id)
        user=User.objects.get(id=id)
        user.first_name=request.POST['fname']
        user.last_name=request.POST['lname']
        user.username=request.POST['uname']
        t.address=request.POST['add']
        t.age=request.POST['age']
        user.email=request.POST['mail']
        t.phone=request.POST['phone']
        courseid=request.POST['c']
        course=Course.objects.get(id=courseid)
        t.course=course

        new_image=request.FILES.get('img')
        if new_image:
            if t.image:
                os.remove(t.image.path)
            t.image = new_image
        t.save()
        user.save()
        return redirect('teachercard')
def teacherdetails(request):
    teacher=Teacher.objects.all()
    return render(request,'teacherdetails.html',{'tc':teacher})

def tdelete(request,pk):
    teacher=Teacher.objects.get(id=pk)
    teacher.delete()
    return redirect('teacherdetails')
def logout(request):
    auth.logout(request)
    return redirect('landingpage')







