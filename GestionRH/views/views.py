from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from ..forms import ProfileUser, ChangePasswordForm
from django.contrib import messages

def BASE(request):
    return render(request, 'home.html')

def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ProfileUser(request.POST, instance=user)
        if form.is_valid:
            form.save()
        return redirect('GestionRH:BASE')
    else:
        form = ProfileUser(instance=user)
    return render(request, 'user/profile.html', {'form': form })

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if new_password == confirm_password:
                user = request.user
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Important pour ne pas déconnecter l'utilisateur après le changement de mot de passe
                    messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
                    return redirect('GestionRH:BASE')
                else:
                    messages.error(request, 'L\'ancien mot de passe est incorrect.')
            else:
                messages.error(request, 'Les nouveaux mots de passe ne correspondent pas.')
    else:
        form = ChangePasswordForm()

    return render(request, 'user/change_password.html', {'form': form})