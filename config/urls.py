from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import (
    home, post_create, post_detail, 
    post_update, post_delete, search,
    about
)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # User Management
    path('accounts/', include('allauth.urls')),

    # Local apps
    path('', home, name='home'),
    path('about/', about, name='about-page'),
    path('search/', search, name='search'),
    path('create/', post_create, name='post-create'),
    path('<id>/post/', post_detail, name='post-detail'),
    path('<id>/post/update/', post_update, name='post-update'),
    path('<id>/post/delete/', post_delete, name='post-delete'),
    # path('<id>/post/delete/', PostDeleteView.as_view(), name='post-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
