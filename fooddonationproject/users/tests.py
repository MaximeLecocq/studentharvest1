from django.test import TestCase
from users.forms import RegistrationForm

#test for the RegistrationForm class, which ensures that validation rules and form fields function as expected
class RegistrationFormTests(TestCase):
    def test_invalid_form_password_mismatch(self):
        #test that the form is invalid if the passwords do not match
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'minnie',
            'password2': 'paul',
            'role': 'student',
        }
        form = RegistrationForm(data=form_data)
        
        if not form.is_valid():
            print("Form Errors:", form.errors)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    

    def test_invalid_form_missing_field(self):
        #test that the form is invalid if the required password2 field is missing
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'jean',
            'password2': '',
            'role': 'student',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)