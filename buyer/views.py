from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from random import randint
from buyer.models import Buyer
from django.conf import settings
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def checkout_view(request):
    return render(request, 'checkout.html')

def faqs_view(request):
    return render(request, 'faqs.html')

def contact_view(request):
    return render(request, 'contact.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        if request.POST['password'] == request.POST['cpassword']:
            global c_otp
            c_otp = randint(100_000, 999_999)
            global user_data
            user_data ={
                'full_name': request.POST['full_name'],
                'email': request.POST['email'],
                'address': request.POST['address'],
                'phone_no': request.POST['phone_no'],
                'password': request.POST['password'],
                'cpassword':request.POST['cpassword']
            }

            sender = settings.EMAIL_HOST_USER
            return render(request,'otp.html')
        else:
            return render(request,'register.html',{'msg':'Password do not match'})
        # create one row in db table
        # add user in our db

def shopnow(request):
    return render(request, 'product.html')

def header_view(request):
    return render(request, 'header.html')

def otp_view(request):
    if str(c_otp)==request.POST['u_otp']:
        Buyer.objects.create(
            full_name=user_data['full_name'],
            email_id=user_data['email'],
            password=user_data['password'],
            address=user_data['password'],
            phone_no=user_data['phone_no']
        )
        return render(request,'index.html',{'msg':'Account successfully created!!'})
    else:
        return render(request,'otp.html',{'msg':'Entered otp is not vaild!!'})
    
def send_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = randint(100_000, 999_999)
        subject = 'OTP for registration'
        message = f'Your OTP for registration is {otp}'
        sender = settings.EMAIL_HOST_USER
        receiver = [email]
        send_mail(subject, message, sender, receiver)
        return render(request, 'otp.html', {'msg': 'OTP sent successfully'})
    else:
        return render(request, 'otp.html', {'msg': 'OTP not sent'})