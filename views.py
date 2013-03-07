from django.http import HttpResponseRedirect

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from wrocloud.utils import generate_form_post_key, get_object_list


def login(request):
    return HttpResponseRedirect("/user/")

def userpage(request):
    user_id = "aaron"
    return render_to_response(
        "userpage.html",
        {
            "tenant_id": settings.TENANT_ID,
            "signature": generate_form_post_key(user_id, "http://16.55.133.228:8080/stored/"),
            "redirect_url": "http://16.55.133.228:8080/stored/",
            "user_id": user_id,
            "stuff": get_object_list(user_id)
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
