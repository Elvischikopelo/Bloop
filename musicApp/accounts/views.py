from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib import auth
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
# Create your views here.

#  VERIFICATION 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage 
from .models import Account

def login(request):
    if request.method =='POST':
        try:
            email = request.POST['email']
            password = request.POST['password'] 

            user = auth.authenticate(request,email=email,password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request,"You have logged in")
                return redirect('home')

            else:
                messages.error(request, "Inavlid login creadential")
                return redirect('dashboard')
        except MultiValueDictKeyError:
            messages.error(request,"email and password are required to login")


    return render(request,'accounts/login.html')


def register(request):
  
    if request.method == "POST":
   
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            username = email.split('@')[0]

            user =  Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
            user.phone_number = phone_number 
            user.save() 




        # USER activation 
            current_site = get_current_site(request)
            mail_subject ='Please activate your account '
            message = render_to_string('accounts/account_verify_email.html',{
                'user':user ,
                'domain':current_site ,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email 
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Thank you for registering ,Verify your email')
            return redirect('acconts/login/?command=verification&email-'+email)
           
    else:
        form = RegistrationForm()
  
    context ={
        'form':form
    }
    return render(request,'accounts/register.html',context)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You have logged out")
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64,decode())
        user = Account._default_manager.get(pk=uid)


    except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.chec_token(user,token):
        user.is_active = True 
        user.save()
        messages.success(request,"Your account has been activated ")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('register') 

@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')



def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.fiter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #send password via email
            current_site = get_current_site(request)
            mail_subject ='Reset tour password '
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user ,
                'domain':current_site ,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email 
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,"Password reset email has been sent to your email")
            return redirect('login')
        else:
            messages.error(request,"Account does not exists")
            return redirect('forgotpassword')
    return render(request,'accounts/forgotpassword.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64,decode())
        user = Account._default_manager.get(pk=uid)


    except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None 

    if user is not None and default_token_generator.chec_token(user,token):
        request.session['uid']= uid
        messages.success(request,"Please reset your password")
        return redirect('resetpassword')

    else:
        messages.error(request,"This link is expired")
        return redirect('login')



def resetpassword(request):
    if request.method =='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.sessions.get['uid']
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfully ')
            return redirect('login')
        else:
            messages.error(request,"Password does not match ")
            return redirect('resetpassword')

    return render(request,'accounts/resetPassword.html')