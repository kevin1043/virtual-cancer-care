from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone

from django.conf import settings


class LungCancerResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    air_pollution = models.FloatField()
    alcohol_use = models.CharField(max_length=50)
    dust_allergy1 = models.CharField(max_length=50)
    dust_allergy2 = models.FloatField()
    occupational_hazard1 = models.CharField(max_length=50)
    occupational_hazard2 = models.CharField(max_length=50)
    genetic_risk = models.CharField(max_length=50)
    chronic_lung_disease = models.CharField(max_length=50)
    balanced_diet = models.FloatField()
    obesity = models.FloatField()
    passive_smoker = models.CharField(max_length=50)
    chest_pain1 = models.CharField(max_length=50)
    chest_pain2 = models.FloatField()
    coughing_blood = models.CharField(max_length=50)
    fatigue = models.CharField(max_length=50)
    prediction = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "LungCancerResult"


class BreastCancerResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    radius_mean = models.FloatField()
    perimeter_mean = models.FloatField()
    area_mean = models.FloatField()
    concavity_mean = models.FloatField()
    concave_points_mean = models.FloatField()
    radius_worst = models.FloatField()
    perimeter_worst = models.FloatField()
    area_worst = models.FloatField()
    concavity_worst = models.FloatField()
    concave_points_worst = models.FloatField()
    predicted_result = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Breast Cancer Result"


class LeukemiaCancerResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    sv = models.FloatField()
    prediction = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "LeukemiaCancerResult"


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(
            username=username,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, default='', blank=True)
    last_name = models.CharField(max_length=30, default='', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(
        Group, related_name='vcc_app_groups', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='vcc_app_user_permissions', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['is_active']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_user_permissions(self, obj=None):
        user = getattr(self, 'user', None)
        if user is not None and user.is_active and user.is_superuser:
            return Permission.objects.all()
        return super().get_user_permissions(obj)

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        db_table = 'vcc_app_user'
