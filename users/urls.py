from django.urls import path
from . import views as core_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('home/', core_views.home, name='home'),
    path('signup/', core_views.signup, name='signup'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name = 'logout'),
]