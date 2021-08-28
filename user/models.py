


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db.models.fields import NullBooleanField

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Prefer not to answer', 'Prefer not to answer'),
]

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # date_of_birth = models.DateField()
    username=models.CharField(max_length=100,null=True,blank=True)
    phone_no=models.CharField(max_length=10, unique=True, null=True, blank=True,
                                      validators=[RegexValidator(r'^\d{3}\d{3}\d{4}$')])
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES, default='Prefer not to answer', null=True,
                              blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

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



class Product(models.Model):
    currencies = [
    ('dollar', "US Dollars"),
    ('rupees', "INR Rupees "),
    ]

    name = models.CharField(max_length=40)
    image=models.ImageField(upload_to='product_image',max_length=254, blank=True, null=True)
    description = models.TextField()
    currency = models.CharField(max_length=10, choices=currencies, default="rupees")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        ordering=('-created_at',)

    
    