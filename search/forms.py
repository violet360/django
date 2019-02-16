from django import forms
from .models import searchbox

class SearchField(forms.ModelForm):

	class Meta:
		model = searchbox
		fields = ('text', )