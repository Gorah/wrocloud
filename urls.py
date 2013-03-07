from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from wrocloud import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', direct_to_template, {"template":"index.html"}),
    url(r'^about/?$', direct_to_template, {"template": "about.html"}),
    url(r'^fail_upload/?$', direct_to_template, 
        {"template": "post_upload.html", "extra_context":{"success": False}},),
    url(r'^success_upload/?$', direct_to_template, 
        {"template": "post_upload.html", "extra_context":{"success": True}},),
    url(r'^stored/', views.stored),
    url(r'^login/?$', views.login),
    url(r'^user/?$', views.userpage),
    )
