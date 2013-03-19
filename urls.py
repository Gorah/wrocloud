from django.conf.urls import patterns, include, url

from wrocloud import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.direct_to_template, {"template":"index.html"}),
    url(r'^about/?$', views.direct_to_template, {"template": "about.html"}),
    url(r'^fail_upload/?$', views.direct_to_template,
        {"template": "post_upload.html", "success": False}),
    url(r'^success_upload/?$', views.direct_to_template,
        {"template": "post_upload.html", "success": True}),
    url(r'^stored/', views.stored),
    url(r'^login/?$', views.login),
    url(r'^user/?$', views.userpage),
    )
