from django import forms
from .models import searchbox

class SearchField(forms.ModelForm):
	text = forms.CharField(label='')
	class Meta:
		model = searchbox
		fields = ('text', )