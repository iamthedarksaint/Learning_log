from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))

def signup(request):
  form = UserCreationForm(data=request.POST)
  if form.is_valid():
    new_user = form.save()
    authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
    login(request, authenticated_user)
    return HttpResponseRedirect(reverse('index'))
  else:
    form = UserCreationForm()
  context = {'form':form}
  return render(request, 'users/signup.html', context)



# # Create your views here.
# def login(request):
#   if request.method == 'POST':
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#       login(request, user)
#       return HttpResponseRedirect('/index/')
#     else:
#       return render(request, 'users/login.html', {'error': 'Invalid credentials'})
#   else:
#     return render(request, 'users/login.html')