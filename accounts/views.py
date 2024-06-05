from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginUser
from .tasks import send_confirmation_email, generate_random_password, check_external_api

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
                # Appel de la tâche Celery pour vérifier l'API externe de manière asynchrone
                result = check_external_api.delay(username, password)
                while not result.ready():
                    pass
                # Récupérer le résultat de la tâche
                api_response = result.result
                if api_response and 'user' in api_response:
                    random_password = generate_random_password()
                        
                    # Récupération des informations de l'utilisateur depuis la réponse API
                    utilisateur_externe = api_response['user']
                    email_send = utilisateur_externe.get('email')
                    username_send = utilisateur_externe.get('username')

                    # Envoyer l'email de confirmation de manière asynchrone
                    send_confirmation_email.delay(email_send, username_send, random_password)

                    new_user = User.objects.create_user(
                        username=username,
                        email=utilisateur_externe.get('email'),
                        first_name=utilisateur_externe.get('first_name'),
                        last_name=utilisateur_externe.get('last_name'),
                        password=random_password
                    )

                    messages.success(request, f'Votre compte a été créé. Un email avec un mot de passe temporaire vous a été envoyé sur {new_user.email}')
                        
                    return redirect('accounts:login')
                else:
                    messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
    else:
        form = LoginUser()

    return render(request, 'auth/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('accounts:login')
