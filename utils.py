from django.conf import settings

import hmac
from hashlib import sha1
from time import time
import urllib2

def generate_form_post_key(path, redirect):
    path = "/v1/%s/testainer/%s/" % (settings.TENANT_ID, path)
    method = 'POST'
    expires = 2147483647
    max_file_size = 1073741824
    hmac_body = "%s\n%s\n%s\n%s\n%s" % (
        path, redirect, max_file_size, "10", expires,
        )
    return "%s:%s:%s" % (
        settings.TENANT_ID, settings.HP_ACCESS_KEY,
        hmac.new(settings.HP_SECRET_KEY, hmac_body, sha1).hexdigest()
        )

def generate_share_url(path):
    path = "%s/%s/%s" % (gensettings.OBJECT_STORE_URL,
                         settings.TENANT_ID, path)
    hmac_body = "%s\n%s\n%s" % ("GET", 2147483647, path)
    return "%s:%s:%s" % (
        settings.TENANT_ID, settings.HP_ACCESS_KEY,
        hmac.new(settings.HP_SECRET_KEY, hmac_body, sha1).hexdigest()
        )

def get_object_list(path):
    raise NOTFUCKINGIMPLEMENTEDERROR,YO
    path = "%s%s/" % (settings.OBJECT_STORE_URL,
                          settings.TENANT_ID)
    handle = urllib2.urlopen(req)
    return response.read()
