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

if settings.INSTALLED_APPS.count("inventory"):
    urlpatterns += i18n_patterns(path('inventory/', include('inventory.urls')), prefix_default_language=True)
else:
    print("not connecting inventory app")

if settings.INSTALLED_APPS.count("tickets"):
    urlpatterns += i18n_patterns(path('dm-tickets/', include('tickets.urls')), prefix_default_language=True)
else:
    print("not connecting ticket app")

if settings.INSTALLED_APPS.count("oceanography"):
    urlpatterns += i18n_patterns(path('oceanography/', include('oceanography.urls')), prefix_default_language=True)
else:
    print("not connecting oceanography app")

if settings.INSTALLED_APPS.count("grais"):
    urlpatterns += i18n_patterns(path('grais/', include('grais.urls')), prefix_default_language=True)
else:
    print("not connecting grais app")

if settings.INSTALLED_APPS.count("herring"):
    urlpatterns += i18n_patterns(path('hermorrhage/', include('herring.urls')), prefix_default_language=True)
else:
    print("not connecting hermorrhage app")

if settings.INSTALLED_APPS.count("camp"):
    urlpatterns += i18n_patterns(path('camp/', include('camp.urls')), prefix_default_language=True)
else:
    print("not connecting camp app")

if settings.INSTALLED_APPS.count("diets"):
    urlpatterns += i18n_patterns(path('diets/', include('diets.urls')), prefix_default_language=True)
else:
    print("not connecting diets app")

if settings.INSTALLED_APPS.count("projects"):
    urlpatterns += i18n_patterns(path('projects/', include('projects.urls')), prefix_default_language=True)
else:
    print("not connecting projects app")

if settings.INSTALLED_APPS.count("ihub"):
    urlpatterns += i18n_patterns(path('ihub/', include('ihub.urls')), prefix_default_language=True)
else:
    print("not connecting ihub app")

if settings.INSTALLED_APPS.count("scifi"):
    urlpatterns += i18n_patterns(path('scifi/', include('scifi.urls')), prefix_default_language=True)
else:
    print("not connecting scifi app")

if settings.INSTALLED_APPS.count("masterlist"):
    urlpatterns += i18n_patterns(path('master-list/', include('masterlist.urls')), prefix_default_language=True)
else:
    print("not connecting masterlist app")

if settings.INSTALLED_APPS.count("shares"):
    urlpatterns += i18n_patterns(path('gulf-shares/', include('shares.urls')), prefix_default_language=True)
else:
    print("not connecting shares app")

if settings.INSTALLED_APPS.count("travel"):
    urlpatterns += i18n_patterns(path('travel-plans/', include('travel.urls')), prefix_default_language=True)
else:
    print("not connecting travel app")

if settings.INSTALLED_APPS.count("ios2"):
    urlpatterns += i18n_patterns(path('ios2/', include('ios2.urls')), prefix_default_language=True)
else:
    print("not connecting ios2")

if settings.INSTALLED_APPS.count("spot"):
    urlpatterns += i18n_patterns(path('grants-and-contributions/', include('spot.urls')), prefix_default_language=True)
else:
    print("not connecting spot")

if settings.INSTALLED_APPS.count("publications"):
    urlpatterns += i18n_patterns(path('publications/', include('publications.urls')), prefix_default_language=True)
else:
    print("not connecting publications app")

if settings.INSTALLED_APPS.count("staff"):
    urlpatterns += i18n_patterns(path('staff/', include('staff.urls')), prefix_default_language=True)
else:
    print("not connecting staff app")

if settings.INSTALLED_APPS.count("whalesdb"):
    urlpatterns += i18n_patterns(path('whalesdb/', include('whalesdb.urls')), prefix_default_language=True)
else:
    print("not connecting whalesdb app")

if settings.INSTALLED_APPS.count("trapnet"):
    urlpatterns += i18n_patterns(path('trapnet/', include('trapnet.urls')), prefix_default_language=True)
else:
    print("not connecting TrapNet")

if settings.INSTALLED_APPS.count("sar_search"):
    urlpatterns += i18n_patterns(path('sar-search/', include('sar_search.urls')), prefix_default_language=True)
else:
    print("not connecting SAR Search")

if settings.INSTALLED_APPS.count("vault"):
        urlpatterns += i18n_patterns(path('vault/', include('vault.urls')), prefix_default_language=True)
else:
    print("not connecting vault app")


if settings.INSTALLED_APPS.count("spring_cleanup"):
    urlpatterns += i18n_patterns(path('spring-cleanup/', include('spring_cleanup.urls')), prefix_default_language=True)
else:
    print("not connecting spring_cleanup app")


if settings.INSTALLED_APPS.count("shiny"):
    urlpatterns += i18n_patterns(path('shiny-apps/', include('shiny.urls')), prefix_default_language=True)
else:
    print("not connecting shiny app repo")

if settings.INSTALLED_APPS.count("csas"):
    urlpatterns += i18n_patterns(path('csas/', include('csas.urls')), prefix_default_language=True)
else:
    print("not connecting csas app")


# if not settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                       document_root=settings.MEDIA_ROOT)
