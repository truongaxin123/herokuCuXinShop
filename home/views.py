from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from .forms import UserRegisterForm


def home(request):
    return render(request, 'home/home.html')


def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home:register_success'))
    return render(request, 'registration/register.html', context={'form': form})


def register_success(request):
    return render(request, template_name='registration/register_success.html')


