from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(Base):
    title = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
    product_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, Base):
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class UserData(Base):
    user = models.OneToOneField(User, related_name='data', on_delete=models.CASCADE, null=True)
    activation_key = models.CharField(null=True, max_length=40)
    is_key_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email