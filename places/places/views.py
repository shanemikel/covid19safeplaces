from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def redirect_to_search(request):
    return HttpResponseRedirect(reverse('search'))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('report')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form}) 

def report(request):
    return HttpResponse(status=500)