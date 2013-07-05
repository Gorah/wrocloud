from django.db import models


class User(models.AbstractBaseUser):
    userid = models.EmailField(max_length=254, unique=True)    
    USERNAME_FIELD = 'userid'

    def is_active(self):
        return True

    def get_full_name(self):
        return 'Full Name'
    
    def get_short_name(self):
        return 'Short Name'
    
