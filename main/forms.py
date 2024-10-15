from typing import Any
from .models import Post,Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=40,widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegisterForm,self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'

class Postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption','image',]
        exclude = ['user']

        widgets = {
            'caption': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter a caption'}),
        }

class ProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_picture']

        widgets = {
            'bio': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter A Bio'}),
        }


