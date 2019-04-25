from django.contrib import admin
from .models import Post

# Register your models here.


class PostModelAdmin(admin.ModelAdmin):

	list_display = ["created_date", "author"]

	list_filter = ["created_date", "x"]

	search_fields = ["title", "text"]
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)