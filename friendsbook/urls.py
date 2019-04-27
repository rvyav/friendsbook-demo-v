from django.contrib import admin
from django.urls import path, include
# Media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', include('accounts.urls', namespace='accounts')),
	path('posts/', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
]

# Media files URL 
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)