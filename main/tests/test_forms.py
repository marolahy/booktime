from django.test import TestCase
from django.core import mail
from main import forms
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
        
