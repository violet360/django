from django import forms
from .models import message




class msg_form(forms.ModelForm):
	
	class Meta:
		model = message
		fields = ('text',)
	