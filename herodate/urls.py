from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('removedforrepo/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/',include('accounts.urls')),
    path('', include('heros.urls')),
]
