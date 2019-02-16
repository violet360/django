from django.db import models

# Create your models here.
class searchbox(models.Model):
	text = models.CharField(max_length=120)

	def __str__(self):
		return self.text