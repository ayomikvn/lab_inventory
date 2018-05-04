from django import forms
from django.contrib.auth.models import User
#from auth_app.models import Engineer

#Form based on Engineer model
class RegistrationForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput()) #Makes the user's password invisible or masked (thatis, *****)
    verify_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    class Meta():
        model = User #Internal Django User class
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)  #

    #Used to validate the user input for registration
    def clean(self):
        all_clean_data = super().clean()
        password = all_clean_data['password']
        verify_password = all_clean_data['verify_password']

        #Validate user's password
        if password != verify_password:
            raise forms.ValidationError("Passwords don't match")    