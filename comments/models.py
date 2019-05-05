from django.db import models
from django.contrib.auth.models import User
# from blog.models import Post
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class commentManager(models.Manager):

	def all(self):
		qs = super(commentManager, self).filter(parent = None)

	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id = instance.id
		qs = super(commentManager, self).filter(content_type = content_type, object_id = obj_id).filter(parent = None)
		return qs



class comments(models.Model):

    objects = commentManager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1, on_delete = models.CASCADE)
    # post = models.ForeignKey(Post, on_delete = models.CASCADE)


    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null = True)
    object_id = models.PositiveIntegerField(null = True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null = True, blank = True, on_delete=models.CASCADE)


    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)


    


    class Meta():
    	ordering = ['-timestamp']

    def __str__(self):
    	return str(self.user.username)


    def get_absolute_url(self):
        return reverse("comments:com_list", kwargs = {"x":self.id})

    def children(self):
    	return comments.objects.filter(parent = self)


    def is_parent(self):
    	if self.parent is not None:
    		return False

    	return True


# Create your models here.
