from django import forms
from django.contrib.auth import authenticate

from .models import CustomUser


class UserSignInForm(forms.ModelForm):
    username = forms.EmailField(label='Почта', widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username','password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        authenticated_user = authenticate(email=email, password=password)
        if not authenticated_user:
            raise forms.ValidationError('Пароли не совпадают.')

        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Пароли не совпадают.')
        else:
            raise forms.ValidationError('Пароли не заполнены.')

        return cleaned_data