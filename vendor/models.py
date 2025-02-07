from django.db import models
from accounts.models import User,UserProfile



from accounts.utils import send_notification
# Create your models here.

class Vendor(models.Model):
  user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
  user_profile = models.OneToOneField(UserProfile, related_name="user_profile", on_delete=models.CASCADE)
  vendor_name = models.CharField(max_length=50)
  vendor_liscense = models.ImageField(upload_to='vendor/liscense')
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.vendor_name

  def save(self, *args, **kwargs):
    if self.pk is not None:
      # above self.pk not none means that vendor is already present in the vendor db and so now we are doin Update operation not creation
      orig = Vendor.objects.get(pk=self.pk)
      if orig.is_approved != self.is_approved:
        #the above orig contains the original values of vendor we have fetched and in the above if block it is checking whehther there is a change happened on the is_approved variable
        context = {
          "is_approved" : self.is_approved,
          "user" : self.user
          }
        if self.is_approved == True:
          # Notify admin
          mail_subject = "Congrats! Restaurant has been approved to publish the menu"
          mail_template = "accounts/emails/admin_notification_template.html"
          send_notification(mail_subject, mail_template, context)
        else:
          mail_subject = "Sorry! Your Restaurant cannot publish the menu"
          mail_template = "accounts/emails/admin_notification_template.html"
          send_notification(mail_subject, mail_template, context)
    return super(Vendor, self).save(*args, **kwargs)