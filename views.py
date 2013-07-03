import simplejson
import urllib
import ntpath
import mimetypes
mimetypes.init()

from django.http import (HttpResponseRedirect, HttpResponse, Http404,
                         HttpResponseServerError)
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

from django_hpcloud import objectstore
from django_hpcloud.authentication import (generate_form_post_key,
                                           get_object_list,
                                           generate_share_url)

from wrocloud.objectstore.models import StoredObject


def login(request):
    return HttpResponseRedirect("/user/")

@ensure_csrf_cookie
def userpage(request, directory=None):
    user_id = settings.OBJECT_STORE_CONTAINER
    if directory:
        stuff = StoredObject.objects.filter(container=user_id, name__startswith=directory + "/")
    else:
        stuff = StoredObject.objects.filter(container=user_id, content_type="application/directory")
    user_id += "/" + directory if directory else ""
    full_uri = request.build_absolute_uri("/stored/%s/" % directory if directory else "/stored/")
    return render_to_response(
        "userpage.html",
        {
            "tenant_id": settings.TENANT_ID,
            "signature": generate_form_post_key(user_id, full_uri),
            "redirect_url":  full_uri,
            "user_id": user_id,
            "stuff": stuff,
            "path": directory
        },
        RequestContext(request))

def stored(request, directory=None):
    if request.GET.get('status') == '201':
        filename_unclean = request.COOKIES.get("lastfile")
        if not filename_unclean:
            raise Http404
        filename = ntpath.split(urllib.unquote(filename_unclean).decode("utf8"))[-1]
        mimetype = mimetypes.guess_type(filename)
        StoredObject.get_or_create(
            container=settings.OBJECT_STORE_CONTAINER,
            name=directory+filename,
            content_type="" if not mimetype[0] else mimetype[0],
            url=generate_share_url(settings.OBJECT_STORE_CONTAINER + "/" + directory+filename)
        ).save()
        return HttpResponseRedirect("/success_upload/")
    else:
        return HttpResponseRedirect("/fail_upload/?=" + request.GET.get('message'))

def direct_to_template(request, template=None, **kwargs):
    return render_to_response(
        template, {"success": kwargs.get('success')},
        RequestContext(request))

def create_directory(request):
    dir = request.POST.get("directory")
    if not dir:
        raise Http404
    status = objectstore.create_directory(dir)
    if status == 201:
        StoredObject(
            container=settings.OBJECT_STORE_CONTAINER,
            name=dir,
            content_type="application/directory"
        ).save()
        return HttpResponse(simplejson.dumps({"status": status}))
    raise HttpResponseServerError
