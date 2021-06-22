from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('discerndlearn-staff/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),  
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)