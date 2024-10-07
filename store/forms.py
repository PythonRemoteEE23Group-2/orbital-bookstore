from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import the custom User model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')