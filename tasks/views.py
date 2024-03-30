from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Tasks
from django.shortcuts import get_object_or_404, render


# Create your views here.

def home(request):
    return render(request, "home.html")


def signup(request):

    if request.method == "GET":
        return render(request, "signup.html",{
            'form' : UserCreationForm
        })


    else:
        if request.POST['password1'] == request.POST['password2']:
            #register

            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except:
                return render(request, "signup.html",{
                    'form' : UserCreationForm,
                    'error' : "El usuario ya existe"
                })


        return render(request, "signup.html",{
            'form' : UserCreationForm,
            'error' : "La contraseña no coincide"
        })



def signout(request):
    logout(request)
    return redirect('home')


def signin(request):

    if request.method == "GET":
        return render(request, 'signin.html',{
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form' : AuthenticationForm,
                'error' : "Nombre o contraseña son incorrectos"
            })
        else:
            login(request,user)
            return redirect('tasks')

def tasks(request):
    tasks = Tasks.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {'tasks' : tasks})



def create_task(request):

    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form' : TaskForm
        })
    else:
        try: 
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'create_task.html',{
                'form' : TaskForm,
                'error' : 'Introduce datos válidos'
            })
    
        
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Tasks ,pk=task_id, user=request.user)
        form = TaskForm(instance = task)
        return render (request, 'task_detail.html', {'task' : task, 'form' :form})
    else:
        try:
            task = get_object_or_404(Tasks, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance= task)
            form.save()
            return redirect('tasks') 
        except ValueError:
            return render (request, 'task_detail.html', {'task' : task, 'form' :form, 'eror' : "Error al actulizar"})

