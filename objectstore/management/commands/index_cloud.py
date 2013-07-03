from django.core.management.base import BaseCommand, CommandError
from django_hpcloud.authentication import (get_object_list,
                                           generate_share_url,
                                           get_container_data)
from wrocloud.objectstore.models import StoredObject

class Command(BaseCommand):

    def handle(self, *args, **options):
        '''implementation'''
        storedobjects = []
        for obj in get_object_list("/"):
            objdata = get_container_data(obj["name"])
            for subobj in objdata:
                storedobjects.append(
                    StoredObject(
                        container=obj["name"],
                        name=subobj["name"],
                        url=generate_share_url(obj["name"] + "/" + subobj["name"]),
                        content_type=subobj["content_type"]
                    )
                )
        StoredObject.objects.bulk_create(storedobjects)
