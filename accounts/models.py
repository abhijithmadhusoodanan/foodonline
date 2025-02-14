from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
  def create_user(self, first_name,last_name, username, email, password=None):
    if not email:
      raise ValueError("user must have an email address")

    if not username:
      raise ValueError("User must have a username")

    user = self.model(
      email = self.normalize_email(email),
      username = username,
      first_name = first_name,
      last_name = last_name
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, first_name, last_name, username, email, password=None):
    user = self.create_user(
      email = self.normalize_email(email),
      username=username,
      password = password,
      first_name = first_name,
      last_name = last_name
    )

    user.is_admin = True
    user.is_active = True
    user.is_staff = True
    user.is_superadmin = True
    user.save(using=self._db)
    return user

class User(AbstractBaseUser):
  RESTAURENT = 1
  CUSTOMER = 2
  ROLE_CHOICE = (
    (RESTAURENT,'Restaurent'),
    (CUSTOMER,'Customer')
    )
  first_name=models.CharField(max_length=100)
  last_name=models.CharField(max_length=100)
  username=models.CharField(max_length=100,unique=True)
  email = models.EmailField(max_length=100,unique=True)
  phone_number = models.CharField(max_length=12, blank=True)
  role = models.SmallIntegerField(choices=ROLE_CHOICE,null=True,blank=True)

  #required fields
  date_joined=models.DateTimeField(auto_now_add=True)
  last_login=models.DateTimeField(auto_now_add=True)
  created_date=models.DateTimeField(auto_now_add=True)
  modified_date=models.DateTimeField(auto_now_add=True)
  is_admin=models.BooleanField(default=False)
  is_staff=models.BooleanField(default=False)
  is_active=models.BooleanField(default=False)
  is_superadmin=models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  objects = UserManager()

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self, appl_label):
    return True

  def get_user_role(self):
    if self.role == 1:
      role = 'Restaurant'
    elif self.role == 2:
      role = 'Customer'
    return role

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
  profile_photo = models.ImageField(upload_to='users/profile_photo', null=True, blank=True)
  cover_photo = models.ImageField(upload_to='users/coverphoto', null=True, blank=True)
  address = models.CharField(max_length=250, null=True, blank=True)
  country = models.CharField(max_length=50, null=True, blank=True)
  state = models.CharField(max_length=50, null=True, blank=True)
  city = models.CharField(max_length=50, null=True, blank=True)
  pin_code = models.CharField(max_length=6, null=True, blank=True)
  latitude = models.CharField(max_length=20, null=True, blank=True)
  longitude = models.CharField(max_length=20, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)

  # def full_address(self):
  #   return f'{self.address_line_1}',f'{self.address_line_2}'
  def __str__(self):
      return self.user.email

