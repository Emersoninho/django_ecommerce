from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza o campo username
        self.fields['username'].label = 'Nome de usuário'
        self.fields['username'].help_text = None  # Remove o texto de ajuda

    # Sobrescreve o campo username para remover validação padrão
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Nome de usuário",
        help_text="Escolha um nome de usuário.",
        widget=forms.TextInput(attrs={"placeholder": "Nome"}),
    )