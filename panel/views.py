from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache  import cache_control
from django.http.response import  HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings #
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import Group, User
import logging
db_logger = logging.getLogger('django_auth_ldap')

#login 
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    login(request, user)
                    return redirect('/dashboard')
                else:
                    messages.error(request, "'"+str(username)+"' is Inactive Username.")
                    return redirect('/login')
            else:
                messages.error(request, "'"+str(username)+"' is not found.")
                return redirect('/')
    else:
            form = LoginForm()
    
    context = {"form": form,}
    return render(request, 'login.html', context)

#logout
@login_required(login_url="/login")  # - if not logged in redirect to /
def logout_view(request):
    try:
        logout(request)
        return redirect('/login')
    except Exception as e:
        return e

#dashboard
@login_required(login_url="/login")  # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)