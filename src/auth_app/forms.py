from django import forms
from django.contrib.auth.models import User
#from auth_app.models import Engineer
from django.contrib.auth.forms import PasswordChangeForm

#Form based on Engineer model
class RegistrationForm(forms.ModelForm):
    
    # Makes the user's password invisible or masked (thatis, *****)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))
    verify_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta():
        model = User #Internal Django User class
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)  


    #Styling of SignUp form    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Last Name'})


    #Used to validate the user input for registration
    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']
        verify_password = all_clean_data['verify_password']

        #Validate user's password
        if password != verify_password:
            raise forms.ValidationError("Passwords don't match")    

#Style the password change form
class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Current Password'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm New Password'})
