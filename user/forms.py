from django import forms
from .models import CustomUser


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Почта', )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if not email:
            raise forms.ValidationError('Почта не указана')

        if email and CustomUser.objects.filter(email=email).first():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')

        return email

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user