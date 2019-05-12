from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

# Create your models here.
class message(models.Model):
	text = models.TextField(max_length=120)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, related_name = "sender")
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, related_name = "receiver")
	timestamp = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.sender)+' to '+str(self.receiver)
