from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Order


class pachange(PasswordChangeForm):
    field=['old_password','new_password1','new_password2']
    old_password=forms.CharField(label="Old password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password1=forms.CharField(label="New password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    new_password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))

class profilechangeform(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields =['username','first_name','last_name','email']
        widgets={'username':forms.TextInput(attrs={"class":"form-control"}),
                  'first_name':forms.TextInput(attrs={"class":"form-control"}),
                  'last_name':forms.TextInput(attrs={"class":"form-control"}),
                   'email':forms.EmailInput(attrs={"class":"form-control"})}

class Signupform(UserCreationForm):
    password1=forms.CharField(label='Enter Password' ,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label='Confirm Password' ,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model = User
        fields=['username','first_name','last_name','email']
        widgets={'username':forms.TextInput(attrs={"class":"form-control"}),
                  'first_name':forms.TextInput(attrs={"class":"form-control"}),
                  'last_name':forms.TextInput(attrs={"class":"form-control"}),
                   'email':forms.EmailInput(attrs={"class":"form-control"})}

class adressform(forms.ModelForm):
    class Meta:
        model=Order
        fields=['shipping_adress','phone','payment_method']
        # widgets={'shipping_adress':forms.TextInput(attrs={"class":"form-control"}),
        #         'phone':forms.TextInput(attrs={"class":"form-control"})}

class loginform(AuthenticationForm):
    field=['username','password']
    username=UsernameField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
 