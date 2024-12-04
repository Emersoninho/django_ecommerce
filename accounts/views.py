from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm

def logout_view(request):
    logout(request)
    return redirect('home:home')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo usuário no banco de dados
            messages.success(request, 'Sua conta foi criada com sucesso! Faça login.')
            return redirect('accounts:login')  # Redireciona para a página de login
        else:
            messages.error(request, 'Erro ao criar a conta. Verifique os dados e tente novamente.')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})