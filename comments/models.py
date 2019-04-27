from django.db import models
from django.contrib.auth.models import User
from blog.models import Post
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1, on_delete = models.CASCADE)
    # post = models.ForeignKey(Post, on_delete = models.CASCADE)


    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null = True)
    object_id = models.PositiveIntegerField(null = True)
    content_object = GenericForeignKey('content_type', 'object_id')



    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)


    def __str__(self):
    	return str(self.user.username)
# Create your models here.
