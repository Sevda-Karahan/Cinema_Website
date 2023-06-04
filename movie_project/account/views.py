from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "account/login.html", {"error":"username ya da parola yanlış"})
    else:
        return render(request, "account/login.html")


def user_register(request):
    if request.method=="POST":
        adsoyad= request.POST["adsoyad"]
        username= request.POST["username"]
        email= request.POST["email"]
        password= request.POST["password"]
        repassword= request.POST["repassword"]
        if password==repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {"error":"Bu kullanıcı adında kullanıcı vardır"})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", {"error":"Bu email adresi sisteme kayıtlıdır"})
                else:
                    user=User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    return redirect("user_login")
        else:
            return render(request, "account/register.html", {"error":"Parola eşleşmiyor"})
    else:
        return render(request, "account/register.html")

def user_logout(request):
    logout(request)
    request.session['show_welcome'] = False
    return redirect("index")

def bildiri(request):
    return render(request, "account/bildiri.html")

def send_registration_email(email):
    subject = 'Cinemaya Kaydınız Tamamlandı'
    message = 'Merhaba,\n\nCinemaya başarıyla kayıt oldunuz. İyi seyirler dileriz!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)