"""dm_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views as views
from accounts import views as acc_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('tracking/', include('tracking.urls')),
]

urlpatterns += i18n_patterns(
    path('', views.IndexView.as_view(), name="index"),
    path('accounts/', include('accounts.urls')),
    path('shared/', include('shared_models.urls')),

    # Password reset views. Views are part of accounts app #
    ########################################################
    path('password-reset/', acc_views.UserPassWordResetView.as_view(), name='password_reset'),
    path('reset/<str:uidb64>/<str:token>/', acc_views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    prefix_default_language=True)

try:
    urlpatterns += i18n_patterns(path('inventory/', include('inventory.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting inventory app")

try:
    urlpatterns += i18n_patterns(path('dm-tickets/', include('tickets.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting ticket app")

try:
    urlpatterns += i18n_patterns(path('oceanography/', include('oceanography.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting oceanography app")

try:
    urlpatterns += i18n_patterns(path('grais/', include('grais.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting grais app")

try:
    urlpatterns += i18n_patterns(path('hermorrhage/', include('herring.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting hermorrhage app")

try:
    urlpatterns += i18n_patterns(path('camp/', include('camp.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting camp app")

try:
    urlpatterns += i18n_patterns(path('diets/', include('diets.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting diets app")

try:
    urlpatterns += i18n_patterns(path('projects/', include('projects.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting projects app")

try:
    urlpatterns += i18n_patterns(path('ihub/', include('ihub.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting ihub app")

try:
    urlpatterns += i18n_patterns(path('scifi/', include('scifi.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting scifi app")

try:
    urlpatterns += i18n_patterns(path('master-list/', include('masterlist.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting masterlist app")

try:
    urlpatterns += i18n_patterns(path('gulf-shares/', include('shares.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting shares app")

try:
    urlpatterns += i18n_patterns(path('travel-plans/', include('travel.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting travel app")

try:
    urlpatterns += i18n_patterns(path('ios2/', include('ios2.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting spot")

try:
    urlpatterns += i18n_patterns(path('grants-and-contributions/', include('spot.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting spot")

try:
    urlpatterns += i18n_patterns(path('publications/', include('publications.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting publications app")

try:
    urlpatterns += i18n_patterns(path('staff/', include('staff.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting staff app")

try:
    urlpatterns += i18n_patterns(path('whalesdb/', include('whalesdb.urls')), prefix_default_language=True)
except RuntimeError as e:
    print(e)
    print("not connecting whalesdb app")

try:
    urlpatterns += i18n_patterns(path('trapnet/', include('trapnet.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting TrapNet")

try:
    urlpatterns += i18n_patterns(path('sar-search/', include('sar_search.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting SAR Search")

try:
    urlpatterns += i18n_patterns(path('vault/', include('vault.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting vault app")

try:
    urlpatterns += i18n_patterns(path('necropsy/', include('necropsy.urls')), prefix_default_language=True)
except RuntimeError:
    print("not connecting necropsy app")


if not settings.PRODUCTION_SERVER:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
