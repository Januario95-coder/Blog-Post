from django import forms
from django.contrib.auth.models import User
from .models import Comment


class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	comments = forms.CharField(required=False,
					widget=forms.Textarea)
					
	
	
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['name', 'email', 'body']
		
		
		
		
class SearchForm(forms.Form):
	query = forms.CharField(
		widget=forms.TextInput(attrs={
			'placeholder': 'Search ...'
		})
	)


class UserLogin(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model = User 
		fields = ['username', 'password']
		
	
		
	