from django.test import TestCase
from django.core import mail
from main import forms
from django.urls import reverse
from unittest.mock import patch
from django.contrib import auth
from main import models
class TestForms(TestCase):
    def test_valid_contact_us_form_sends_email(self):
        form = forms.ContactForm({
            'name': 'Maitre Yoda',
            'message': 'Que la force soit avec toi'
        })
        self.assertTrue(form.is_valid())

        with self.assertLogs('main.forms',level='INFO') as cm:
            form.send_mail()

        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].subject,'Test mail')
        self.assertGreaterEqual(len(cm.output),1)
    
    def test_invalid_contact_us_form(self):
        form = forms.ContactForm({
            'message': 'Que la force soit avec toi'
        })
        self.assertFalse(form.is_valid())

    def test_valid_signup_form_send_email(self):
        form = forms.UserCreationForm(
            {
                "email": "test@test.com",
                "password1": "abcabcabc",
                "password2": "abcabcabc",
            }
        )
        self.assertTrue( form.is_valid() )
        with self.assertLogs( "main.forms", level="INFO" ) as cm :
            form.send_mail()
        
        self.assertEquals( len(mail.outbox), 1 )
        self.assertEquals(
            mail.outbox[0].subject,
            "Welcome to Booktime"
        )

        self.assertGreaterEqual( len(cm.output), 1)

    def test_user_signup_page_submission_works( self ):
        post_data = {
            "email":"test@test.com",
            "password1": "abcabcabc",
            "password2": "abcabcabc",
        }
        with patch.object(
            forms.UserCreationForm,
            "send_mail"
        ) as mock_send:
            response = self.client.post(
                reverse("signup"),
                post_data
            )
        self.assertEquals(response.status_code,302)
        self.assertTrue(
            models.User.objects.filter(
                email="test@test.com"
            ).exists()
        )
        self.assertTrue(
            auth.get_user(self.client).is_authenticated
        )
        mock_send.assert_called_once()

    

        
