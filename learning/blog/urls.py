from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('registration', views.registration, name="registration"),
    path('login_page', views.login_, name="login_page"),
    path('logout_page', views.logout_, name="logout_page"),
    path('new_post', views.new_post, name="new_post"),
    path('post_edit', views.post_edit, name="post_edit"),
    path('post_save', views.post_save, name="post_save"),
    path('user_account', views.account, name="account"),
    path('post_delete', views.post_delete, name="post_delete"),
]\
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)