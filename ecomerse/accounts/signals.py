from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from smtplib import SMTPException
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from .models import User

@receiver(post_save, sender=User)
def send_email_otp(sender, instance, created, **kwargs):
    if created:
        try:      
            htmly = get_template('Email.html')
            d = { 'username': instance.username, 'email_type': 'registration' }
            subject = 'Welcome to eCommerce'
            from_email = 'shashwat100k@gmail.com'
            to = instance.email
            html_content = htmly.render(d)
            text_content = 'Welcome to eCommerce'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send() 
        except SMTPException as e:
            print(f'unable to send the email {e}')

        print(f'=========signal is working correctly=========={instance.email} {instance.username}')