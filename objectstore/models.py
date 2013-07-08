from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class StoredObject(models.Model):
    container = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    url = models.URLField(max_length=1000)
    content_type = models.CharField(max_length=250)

class KeyValue(models.Model):
    storedobject = models.ForeignKey(
        StoredObject
    )
    key = models.CharField(max_length=250)
    value = models.TextField()

    def __unicode__(self):
        return "%s:%s" % (self.key, self.value)

class MyUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name,
                    password=None):
        """
        Creates and saves a User with the given email, name  and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,
                    password=None):
        """
        Creates and saves a User with the given email, name  and password.
        """

        if not email:
            raise ValueError('Users must have an email address')

        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')
        
        user = self.create_user(email, first_name, last_name,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    first_name = models.TextField()
    last_name = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_staff(self):
        #if user is an admin, then he's a staff member 
        return self.is_admin
