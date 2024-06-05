from django import forms
from django.contrib.auth.models import User

class ProfileUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': "Nom d'utilisateur",
            'first_name': "Prénom",
            'last_name': "Nom de famille",
            'email': "Adresse email"
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
        }

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'}), label="Ancien mot de passe")
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'}), label="Nouveau mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'}), label="Confirmer le nouveau mot de passe")
