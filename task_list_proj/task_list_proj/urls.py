
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

from googleSheets import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('gSheet/', include('googleSheets.urls')),
    path('accounts/', include('accounts.urls')),
    path("user/", include('userSheets.urls')),

]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
