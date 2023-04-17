
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

from googleSheets import views


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('gSheet/', include('googleSheets.urls')),

]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
