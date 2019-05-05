# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from comments.models import comments
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    x = models.BooleanField(default = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



    # @property
    def comments(self):
        instance = self
        qs = comments.objects.filter_by_instance(instance)
        return qs



    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)

        return content_type