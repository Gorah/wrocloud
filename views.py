import simplejson
import urllib
import ntpath
import mimetypes
mimetypes.init()

from django.http import (HttpResponseRedirect, HttpResponse, Http404,
                         HttpResponseServerError)
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

from django_hpcloud import objectstore
from django_hpcloud.authentication import (generate_form_post_key,
                                           get_object_list,
                                           generate_share_url)

from wrocloud.objectstore.models import StoredObject



def userlogin(request):
    '''Logs user in or redirects to a page with error message'''
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/user/")
        else:
            return render_to_response("auth_error.html",
                                      {"msg": 'Error: User disabled!'},
                                      RequestContext(request))
    else:
        return render_to_response("auth_error.html",
                                  {"msg": 'Error: invalid login!'},
                                  RequestContext(request))

def userlogout(request):
    '''Logs user out and redirects to main page'''
    logout(request)
    return HttpResponseRedirect("/")

@ensure_csrf_cookie
@login_required
def userpage(request, directory=None):
    '''userpage serves up the base page for the lists of containers and
    the files that they contain.

    It will take an optional directory which means that this page
    helpfully is also used for subdirectories. Without the directory
    argument we just serve up the base set of folders in the Wrocloud
    container.
    '''
    # TODO: A user's path should be prefixed with their username.
    user_id = settings.OBJECT_STORE_CONTAINER
    print directory
    if directory:
        stuff = StoredObject.objects.filter(
            container=request.user.username,
            dirparent=directory + "/"
        ).exclude(
            content_type="application/directory"
        )
        directories = StoredObject.objects.filter(
            container=request.user.username,
            content_type="application/directory",
            dirparent=directory
        )
    else:
        directories = StoredObject.objects.filter(
            container=request.user.username,
            content_type="application/directory"
        ).exclude(
            is_subdir=True
        )
        stuff = None
    user_id += "/" + directory if directory else ""
    full_uri = request.build_absolute_uri(
        "/stored/%s" % directory + "/" if directory else ""
    )
    return render_to_response(
        "userpage.html",
        {
            "show_file_upload": bool(directory),
            "tenant_id": settings.TENANT_ID,
            "signature": generate_form_post_key(user_id, full_uri),
            "redirect_url":  full_uri,
            "user_id": user_id,
            "stuff": stuff,
            "directories": directories,
            "path": directory
        },
        RequestContext(request))

@login_required
def stored(request, directory=None):
    '''Stored is the endpoint which is redirected to when we've uploaded a
    new file into the Object Store via a Form Post. The underlying HPCloud
    bindings shouldn't take care of this since it's a front-end related
    thing.

    stored will take care of updating our local cache of metadata when
    we're adding files.
    '''
    if request.GET.get('status') == '201':
        filename_unclean = request.COOKIES.get("lastfile")
        if not filename_unclean:
            raise Http404
        # TODO: Unfuck this code.
        filename = ntpath.split(urllib.unquote(filename_unclean).decode("utf8"))[-1]
        mimetype = mimetypes.guess_type(filename)
        # Disgusting crap ends here ------
        obj, created = StoredObject.objects.get_or_create(
            container=request.user.username,
            dirparent=directory,
            name=directory+filename,
            content_type="" if not mimetype[0] else mimetype[0],
            url=generate_share_url(
                "%s/%s" % (settings.OBJECT_STORE_CONTAINER, directory+filename)
            )
        )
        if created:
            obj.save()
        return HttpResponseRedirect("/success_upload/")
    else:
        return HttpResponseRedirect("/fail_upload/?=" + request.GET.get('message'))

def direct_to_template(request, template=None, **kwargs):
    '''This is a remake of a helper which used to be in the django
    standard distribution. Simply returns a template with a single
    piece of context.
    '''
    return render_to_response(
        template, {"success": kwargs.get('success')},
        RequestContext(request))

@login_required
def create_directory(request):
    '''Create directory will funnily enough create a new directory in the
    HPCloud ObjectStore. The resulting directory will be 'invisible'
    on the HPCloud objectstore interface but it will exist when the
    container is queried so we store a local entry for this directory
    so we can display it later.
    '''
    dir = request.POST.get("directory")
    if not dir:
        raise Http404
    status = objectstore.create_directory(dir)
    parent = ("/").join(dir.split("/")[:-1])
    if status == 201: # TODO: see if there's a module for all these
                      # magic numbers.
        obj, created = StoredObject.objects.get_or_create(
            is_subdir=parent != "",
            container=request.user.username,
            dirparent=parent,
            name=dir,
            content_type="application/directory"
        )
        if created:
            obj.save()
        return HttpResponse(simplejson.dumps({"status": status}))
    raise HttpResponseServerError
