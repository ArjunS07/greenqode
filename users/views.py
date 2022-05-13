from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from main.models import Community

from .forms import RegisterForm
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']

            newuser = User.objects.get(username=username)
            newCommunity = Community(account = newuser, name = username)
            newCommunity.save()

            return redirect("/login")

    else:
        form = RegisterForm()
    return render(request, "users/signup.html", {"form": form})

def login_user(request):

    print("logging in user")


    username = ''
    password = ''
    
    if request.method == 'POST':
        print('received post')
        username = request.POST['username']
        password = request.POST['password']

        print(username)
        print(password)

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
                login(request, user)
                return redirect('/communitycollection')

        else:
            print("user not found")
            return render(request, 'login.html', {'error_message': 'Invalid username or password. Please try again.'})

    else:
        return render(request, 'login.html', {'error_message': ''})

def logout_user(request):
    logout(request)
    return redirect('/')