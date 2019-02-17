from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse


# Override User model
class CustomUserManager(BaseUserManager):
    """
    Overriding BaseUserManager in order to allow users to register and authenticate by using email instead of username.
    """
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email field is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    RESPONDENT = 'respondent'
    SURVEYOR = 'surveyor'

    USER_TYPES = (
        (SURVEYOR, 'Surveyor'),
        (RESPONDENT, 'Respondent'),
    )

    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
        ),
    )
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('users:update_profile')


class Profile(models.Model):
    """
    User input data
    DEMOGRAPHICS
    """
    PA = 'pa'
    NY = 'ny'
    MY = 'my'
    VA = 'va'

    STATES = (
        (PA, 'Pennsylvania'),
        (NY, 'New York'),
        (MY, 'Maryland'),
        (VA, 'Virginia'),
    )

    company = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=500, blank=True)
    state = models.CharField(max_length=2, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile for {self.user.email}'



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()