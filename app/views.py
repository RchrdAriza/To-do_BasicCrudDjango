from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Tarea
from .forms import TareasForms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def signup(request):
    if request.method == 'GET':
        data = {
            'form': UserCreationForm
        }
        return render(request, 'signup.html', data)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(to='tareas')
            except:
                messages.warning(request, 'El usuario ya existe')
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                })
        messages.error(request, 'Las contraseñas no coinciden')
        return render(request, 'signup.html', {
            'form': UserCreationForm,
        })


def signin(request):
    if request.method == 'GET':
        data = {
            'form': AuthenticationForm
        }
        return render(request, 'signin.html', data)
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST['password'])
        if user is None:
            messages.warning(request, "El usuario o contrasena no son validos")
            data = {
                'form': AuthenticationForm,
                }
            return render(request, 'signin.html', data)
        login(request, user)
        return redirect('tareas')

@login_required
def listar_tareas(request):
    objecto = Tarea.objects.filter(user=request.user)
    data = {
        'tareas': objecto
    }
    return render(request, 'tareas.html', data)


@login_required
def crear_tarea(request):
    if request.method == 'GET':
        data = {
            'form': TareasForms
        }
        return render(request, 'crear_tarea.html', data)
    else:
        formulario = TareasForms(data=request.POST)
        if formulario.is_valid():
            nueva_tarea = formulario.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            return redirect(to='tareas')

@login_required
def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def modificar_tarea(request, id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tarea, id=id, user=request.user)
        data = {
            'form': TareasForms(instance=tarea)
        }
        return render(request, 'modificar.html', data)
    else:
        try:
            tarea = get_object_or_404(Tarea, id=id, user=request.user)
            form = TareasForms(request.POST, instance=tarea)
            form.save()
            return redirect('tareas')
        except:
            tarea = get_object_or_404(Tarea, id=id, user=request.user)
            data = {
                'form': TareasForms(instance=tarea),
                'error': 'Hubo un error actualizando'
            }
            return render(request, 'modificar.html', data)

@login_required
def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id, user=request.user)
    tarea.delete()
    return redirect('tareas')

@login_required
def ver_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id, user=request.user)
    data = {
        'tarea': tarea
    }
    return render(request, 'ver_tarea.html', data)
