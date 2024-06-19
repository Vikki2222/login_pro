from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import pyrebase
from .models import AccessRule


config = {
    'apiKey': "AIzaSyAofazqS6Ulrgx0t19L9BYldCZa2NnJCWw",
    'authDomain': "intern-7453c.firebaseapp.com",
    'projectId': "intern-7453c",
    'storageBucket': "intern-7453c.appspot.com",
    'messagingSenderId': "692692269732",
    'appId': "1:692692269732:web:c9e83e952aef460f998431",
    'measurementId': "G-VNRSJXYZWB",
    'databaseURL' : "https://intern-7453c-default-rtdb.asia-southeast1.firebasedatabase.app/"
  };

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()



def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            # Check if user already exists
            if User.objects.filter(username=uname).exists():
                return HttpResponse("Username already exists!")
            elif User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists!")
            else:
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.save()
                user = auth.create_user_with_email_and_password(email, pass1)
                return redirect('login')  # Ensure 'login' is a valid URL name in your urls.py

    return render(request, 'signup.html')



def login(request):
    return render(request,'login.html')

def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    user = auth.sign_in_with_email_and_password(email, passw)
    return render(request,"home.html",{"e":email})



@login_required(login_url='login')

def HomePage(request):
     return render (request,'home.html')


def LogoutPage(request):
     logout(request)    
     return redirect('login')



@login_required
def toggle_access_rule(request):
    if request.user.is_staff and request.user.is_superuser:
        access_rule, created = AccessRule.objects.get_or_create(id=1)
        access_rule.is_enabled = not access_rule.is_enabled
        access_rule.save()
    return redirect('home')

def home(request):
    access_rule, created = AccessRule.objects.get_or_create(id=1)
    return render(request, 'base.html', {'access_rule': access_rule})

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import LoginSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                return Response({'token': user['idToken']}, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
