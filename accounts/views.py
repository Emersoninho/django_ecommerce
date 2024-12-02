from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Usuário registrado com sucesso!')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Voçê foi logado com sucesso!')
            return redirect('home:home')
        else:
            messages.error(request, 'Credenciais inválidas')
    else:
        form = AuthenticationForm(request)
    return render(request, 'registration/login.html', {'form': form})    

def logout_user(request):
    logout(request)
    messages.success(request, 'Voçê foi deslogado com sucesso!')
    return redirect('home:home')

def logout_confirmation(request):
    return render(request, 'registration/logout_confirmation.html')