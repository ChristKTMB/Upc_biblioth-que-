from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import random, string

@shared_task
def send_confirmation_email(email, username_send, random_password):
    subject = 'Confirmation de votre inscription'
    message = render_to_string('email/confirmation.html', {
        'username': username_send,
        'password': random_password,
    })
    plain_message = strip_tags(message)  # Version texte brut du message pour les clients de messagerie qui ne prennent pas en charge HTML
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=message,
    )

def generate_random_password(length=8):
    # Génère un mot de passe aléatoire
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))
