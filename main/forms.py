from django import forms
from django.core.mail import send_mail
import logging
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    UsernameField
)
from . import models
logger = logging.getLogger(__name__)
class ContactForm(forms.Form):
    name = forms.CharField(label="Your name",max_length=100)
    message = forms.CharField(max_length=600,label="Your Message", widget=forms.Textarea)

    def send_mail(self):
        logger.info("Envoie d'email")
        message = "From :{0}\n{1}".format(
            self.cleaned_data['name'],
            self.cleaned_data['message']
        )
        send_mail("Test mail",
                    message,
                    "marolahy@zoho.com",
                    ["marolahy@gmail.com"],
                    fail_silently=False)

class UserCreationForm( DjangoUserCreationForm ):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email":UsernameField}

    def send_mail(self):
        logger.info(
            "Sending signup email for email=%s",
            self.cleaned_data["email"],
        )
        message = "Welcome {}".format(self.cleaned_data["email"])
        send_mail(
            "Welcome to Booktime",
            message,
            "site@bootime.mg",
            [self.cleaned_data["email"]],
            fail_silently=True,
        )