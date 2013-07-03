from django.http import HttpResponseRedirect

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from django_hpcloud.authentication import (generate_form_post_key,
                                           get_object_list,
                                           generate_share_url)

from wrocloud.objectstore.models import StoredObject

def login(request):
    return HttpResponseRedirect("/user/")

def userpage(request, directory=None):
    user_id = settings.OBJECT_STORE_CONTAINER
    if directory:
        stuff = StoredObject.objects.filter(container=user_id, name__startswith=directory + "/")
    else:
        stuff = StoredObject.objects.filter(container=user_id, content_type="application/directory")
    full_uri = request.build_absolute_uri("/stored/")
    return render_to_response(
        "userpage.html",
        {
            "tenant_id": settings.TENANT_ID,
            "signature": generate_form_post_key(user_id, full_uri),
            "redirect_url":  full_uri,
            "user_id": user_id,
            "stuff": stuff
        },
        RequestContext(request))

def stored(request):
    if request.GET.get('status') == '201':
        return HttpResponseRedirect("/success_upload/")
    else:
        return HttpResponseRedirect("/fail_upload/?=" + request.GET.get('message'))

def direct_to_template(request, template=None, **kwargs):
    return render_to_response(
        template, {"success": kwargs.get('success')},
        RequestContext(request))
