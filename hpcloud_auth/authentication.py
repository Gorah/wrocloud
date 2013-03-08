from django.conf import settings
from wrocloud.hpcloud_auth.models import AuthToken

import hmac
from hashlib import sha1
from time import time
import urllib2
import simplejson

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

def generate_share_url(path, expires=2147483647):
    hmac_path = "/v1.0/%s/testainer/%s" % (settings.TENANT_ID, path)
    print hmac_path
    hmac_body = "%s\n%s\n%s" % ("GET",expires, hmac_path)
    hmac_code = "%s:%s:%s" % (
        settings.TENANT_ID, settings.HP_ACCESS_KEY,
        hmac.new(settings.HP_SECRET_KEY, hmac_body, sha1).hexdigest()
        )
    path = "%s%s/testainer/%s?temp_url_sig=%s&temp_url_expires=%s" % (
        settings.OBJECT_STORE_URL, settings.TENANT_ID, path,
        hmac_code, expires)
    return path

def get_object_list(path):
    path = "%s%s/testainer/" % (settings.OBJECT_STORE_URL, settings.TENANT_ID)
    req = urllib2.Request(path)
    req.add_header("Content-type", "application/json")
    req.add_header("X-Auth-Token", get_auth_token())
    response = urllib2.urlopen(req)
    return response.read().split('\n')

def get_auth_token():
    if AuthToken.objects.all().count() > 0:
        return AuthToken.objects.all()[0].token
    json_data = {
        "auth": {
            "passwordCredentials": {
                "username": settings.HPCLOUD_USERNAME,
                "password": settings.HPCLOUD_PASSWORD
                },
            "tenantId": settings.TENANT_ID
            }
        }
    payload = simplejson.dumps(json_data)
    print payload
    req = urllib2.Request(
        settings.REGION_URL + "tokens",
        )
    req.add_header("Content-type", "application/json")
    json = simplejson.loads(urllib2.urlopen(req, payload).read())
    AuthToken(token=json['access']['token']['id']).save()
    return json['access']['token']['id']
