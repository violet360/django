from django import forms

from .models import Post

class PostForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea,label='content')

	class Meta:
		model = Post
		fields = ('title', 'text',)