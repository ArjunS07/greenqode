from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from main.models import Community, CommunityItem

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

            return redirect("/communitycollection")

    else:
        form = RegisterForm()
    return render(request, "users/signup.html", {"form": form})
