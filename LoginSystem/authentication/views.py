from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from LoginSystem import settings
from django.core.mail import send_mail  

# Create your views here.
def home(request):
    return render(request,'authenticate/index.html')
def signup(request):

    if(request.method=="POST"):
        username=request.POST['username']
        name=request.POST['name']
        mail=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirm']
        
        if(User.objects.filter(username=username)):
            messages.error(request,"Username Already exist! try with another username.")
            return redirect('home')
        # if(User.objects.filter(email=mail)):
        #     messages.error(request,"Email Already Registered !")
        #     return redirect('home')
        if(len(username)>10):
            messages.error(request,"length of username should be less than 10 !")
            return redirect('home')
        if(password!=confirmpassword):
            messages.error(request,"Password did't match !")
            return redirect('home')
        if not username.isalnum():
            messages.error(request,"Username should be alpha numeric !")
            return redirect('home')

        myuser=User.objects.create_user(username,mail,password)
        myuser.first_name=name
        myuser.save()
        messages.success(request,"Your Account has been successfully created! Confirmation mail sent to your registerd mail!")

        # Working on Email
        subject= "Welcome to Interview Experience portal!"
        message="Hello"+ myuser.first_name + "! \n" + "Welcome to Interview Experience portal \n here your can write your own interview experiences. \n You can also view top interview experiences from employees of google, amazon, meta etc. \n we have sent a confirmation mail to activate your account. \n\n Thank You! \n Daravath Naresh"
        from_email = settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        return redirect("signin")

    return render(request,"authenticate/signup.html")
def signin(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            name=user.first_name
            return render(request,"authenticate/index.html",{'name':name})
        else:
            messages.error(request,"Bad Credintials")   
            return redirect('home')
            
    return render(request,"authenticate/signin.html")
def signout(request):
    logout(request)
    messages.success(request,"You have Successfully logged out!")
    return redirect('home')