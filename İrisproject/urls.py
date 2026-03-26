from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # route for the built in admin interface
    path('admin/', admin.site.urls),

    # include URL configurations from the main app
    path('', include('main.urls')), 
]
