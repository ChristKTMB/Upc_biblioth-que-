from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .forms import LoginUser
import requests, random, string

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# Create your views here.

def generate_random_password(length=8):
    # Génère un mot de passe aléatoire
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def login_user(request):
    if request.method == 'POST':
        form = LoginUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('GestionRH:BASE')
            else:
                api_url = "http://localhost:5000/api"
                api_data = {
                    "method": "login",
                    "username": username,
                    "password": password
                }
                response = requests.post(api_url, json=api_data)
                if response.status_code == 200:
                    api_response = response.json()
                    if 'user' in api_response:
                        # Récupération des informations de l'utilisateur depuis la réponse API
                        utilisateur_externe = api_response['user']
                        random_password = generate_random_password()

                        new_user = User.objects.create_user(
                            username=username,
                            email=utilisateur_externe.get('email'),
                            first_name=utilisateur_externe.get('first_name'),
                            last_name=utilisateur_externe.get('last_name'),
                            password=random_password
                        )

                        # Envoyer un email de confirmation
                        subject = 'Confirmation de votre inscription'
                        message = render_to_string('email/confirmation.html', {
                            'user': new_user,
                            'password': random_password,
                        })
                        plain_message = strip_tags(message)  # Version texte brut du message pour les clients de messagerie qui ne prennent pas en charge HTML
                        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [new_user.email], html_message=message)

                        messages.success(request, f'Votre compte a été créé. Un email avec un mot de passe temporaire vous a été envoyé sur {new_user.email}')
                        return redirect('accounts:login')
                    
                else:
                    messages.error(request, 'Une erreur s\'est produite lors de la vérification des informations de connexion.')
    else:
        form = LoginUser()
    return render(request, 'auth/login.html', {'form': form})







def logout_user(request):
    logout(request)
    return redirect('accounts:login')
