from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.core.mail import send_mail
import uuid

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("The given username must be set")
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True, verbose_name='ID', db_index=True)
    iden = ((0, '顧客'), (1, '廠商'))
    identity = models.IntegerField(choices=iden, default=True, blank=True, null=False)
    username = models.CharField(max_length=150, unique=True,
                                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
                                )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    gen = ((0, '女'), (1, '男'))
    gender = models.IntegerField(choices=gen, default=1, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    tax_ID_number = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=200, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False,
                                   help_text="Designates whether the user can log into this admin site.",)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

# settings.AUTH_USER_MODEL


class Brand(models.Model):
    brand_name = models.CharField(max_length=120, blank=True)  # char型態輸入
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=True, related_name='brand')
    description = models.TextField(blank=True, null=True)  # Text型態輸入、True需大寫、blank針對表格能否為空、null針對資料庫能否為空
    tax_ID_number = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=120, blank=True)
    email = models.EmailField(max_length=120, blank=True)

    def __str__(self):
        return self.brand_name
        # return '品牌名:{} 公司名:{} 敘述:{} 聯絡電話:{} 電子信箱:{}'.format(
        #     self.brand_name, self.account, self.description, self.phone_number, self.email)

    def get_absolute_url(self):
        return reverse("partners:brand-detail", kwargs={"b_id": self.id})  # 動態依據搜尋路徑名稱提取資料
        # return f"/products/{self.id}/" #依據產品編號提取資料


class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=False, related_name='cart')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, default=None, null=False, related_name='cart')

    def get_absolute_url(self):
        return reverse("partner-cart", kwargs={"c_id": self.id})  # 動態依據搜尋路徑名稱提取資料


class HandSize(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default=None, null=False, related_name='hand_size')
    thumb_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    thumb_width = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    index_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    index_width = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    middle_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    middle_width = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    ring_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    ring_width = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    little_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    little_width = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    palm_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)
    palm_width = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, blank=False, null=False)

    def get_absolute_url(self):
        return reverse("partner-hand-size", kwargs={"hs_id": self.id})  # 動態依據搜尋路徑名稱提取資料
