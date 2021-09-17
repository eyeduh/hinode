from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
# from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils.translation import ugettext_lazy as _

from .validators import MinAgeValidator

User = settings.AUTH_USER_MODEL

# Create your models here.


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         if not email:
#             raise ValueError('Users must have an email address!')

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None):
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name=_('email address'),
#         max_length=255,
#         unique=True,
#     )
#     is_active = models.BooleanField(verbose_name=_('is active'), default=True)
#     is_admin = models.BooleanField(verbose_name=_('is admin'), default=False)

#     USERNAME_FIELD = 'email'

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True


class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name=_('first name'), max_length=100)
    last_name = models.CharField(verbose_name=_('last name'), max_length=100)
    nickname = models.CharField(verbose_name=_('nickname'), max_length=100, null=True, blank=True)
    bio = models.TextField(verbose_name=_('bio'), null=True, blank=True)
    date_of_birth = models.DateField(verbose_name=_('date of birth'), validators=[MinAgeValidator])
    avatar = models.ImageField(verbose_name=_('avatar'), blank=True, upload_to='media/avatars')
    location = models.CharField(verbose_name=_('location'), max_length=100, null=True, blank=True)
    job = models.CharField(verbose_name=_('job'), max_length=100)
    phone_number = models.PositiveBigIntegerField(verbose_name=_('phone number'), unique=True)
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)
    followers = models.ManyToManyField(User, verbose_name=_('followers'), related_name='following', blank=True)
    GENDERS = (
        (1, 'Female'),
        (2, 'Male'),
        (3, 'Rather Not Say')
    )
    gender = models.IntegerField(verbose_name=_('gender'), choices=GENDERS, default=1)

    class Meta:
        db_table = 'userprofiles'
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return '{}, {}'.format(self.user.id, self.phone_number)


def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


post_save.connect(user_did_save, sender=User)
