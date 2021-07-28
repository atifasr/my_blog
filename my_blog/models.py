from django.db import models

# Create your models here.

# from typing_extensions import Required
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.base import Model, ModelState
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.forms import widgets


from django.conf import settings


CHOICES = [("Food", "Food"),
           ('Travel', 'Travel'), ('Music', 'Music'), ('Lifestyle', 'Lifestyle'), ('Fitness', 'Fitness'), ('Sports', 'Sports')]


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """ Creates and saves a superuser with the given email, date ofbirth and password.
        """
        user = self.create_user(
            username=username,
            first_name='',
            last_name='',
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        blank=True
    )
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    date_of_birth = models.DateField(default='1995-03-25')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Category(models.Model):
    name = models.CharField(max_length=25, choices=CHOICES, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Category'

    def __str__(self):
        return str(self.name)

    @property
    def descrip(self):
        return self.description[:3]

    def get_descrip(self):
        return self.description[:30]


class Topic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    article_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Entry(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='images', blank=True)
    video = models.FileField(upload_to='videos', blank=True)

    class Meta:
        verbose_name_plural = 'entries'

    @property
    def get_photo_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        else:
            return " "

    def __str__(self):
        return f'{self.text[:80]}...'


class Comment(models.Model):
    post = models.ForeignKey(Entry, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comment'


class Subscriber(models.Model):

    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"
