from django.urls import path
from . import views

urlpatterns = [
	# path('messages/', views.msg_list, name = 'msg_list'),
	path('<int:var>/msgs/', views.msg_view, name = 'msg_view'),
	path('msgs/', views.msg_list, name = 'msg_list'),
	# path('messages/<int:pk>/', views.msg_detail, name = 'msg_detail'),
	# path('', views.welcome, name = 'welcome'),
	# path('post/345/', views.view_other_profile, name = 'view_other_profile'),
]