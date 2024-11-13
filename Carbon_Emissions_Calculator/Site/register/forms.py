from django.contrib.auth import login, authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import register
from django import forms


houses = (
    ("Bari","Bari"),
    ("Ikhaya","Ikhaya"),
    ("Ruka","Ruka"),
    ("Meraki","Meraki"),
    ("Balie","Balie"),
    ("Hogan","Hogan"),
    ("Heimat","Heimat"),
    ("Bandele","Bandele"),
    ("Bayt","Bayt"),
    ("Efie","Efie"),
    ("Ohana","Ohana"),
    ("Faculty", "Faculty")
)
accounts = {
    ("Resident","Resident"),
    ("Operator","Operator"),
    ("Administrator","Administrator"),
}

class RegisterForm(UserCreationForm):

    class Meta:
        model = register.models.User
        fields = ("username","house","password1","account_type")

class LoginForm(AuthenticationForm):
    account = forms.ChoiceField(choices = accounts)
    class Meta:
        model = register.models.User
        fields = ("account","username","password")


            

            
    

