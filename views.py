from django.http import HttpResponseRedirect

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from django_hpcloud.authentication import (generate_form_post_key,
                                                  get_object_list,
                                                  generate_share_url)


def login(request):
    return HttpResponseRedirect("/user/")

def userpage(request):
    user_id = "testainer"
    stuff = [(generate_share_url(user_id + item), item)
             for item in filter(lambda x: len(x) > 0,
                                get_object_list(user_id))]
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
        return HttpResponseRedirect("/fail_upload/")

def direct_to_template(request, template=None, success=False):
    return render_to_response(
        template, {"success": success},
        RequestContext(request))
