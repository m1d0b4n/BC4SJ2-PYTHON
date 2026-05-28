from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
