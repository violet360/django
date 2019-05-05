from django.urls import path
from . import views

urlpatterns = [
	path('comments/<int:x>/', views.com_list, name = 'com_list'),
	# path('post/<int:pk>/delete/', views.com_del, name = 'com_del'),
]