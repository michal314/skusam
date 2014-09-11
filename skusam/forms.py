from django import forms
from skusam.models import UserProfile, Article, Page
from django.contrib.auth.models import User,Group

class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture']

class UsergroupForm(forms.ModelForm):
     
     class Meta:
         model=Group
         fields=['name']

class PageForm(forms.ModelForm):
    title=forms.CharField(max_length=128,help_text="Please enter the title of the page")
    url=forms.URLField(max_length=200,help_text="Please enter the url of the page")  
    views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
   
    class Meta:
       model=Page
       fields=('title','url','views')        