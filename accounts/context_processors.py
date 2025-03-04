from vendor.models import Vendor
from django.conf import settings

def get_vendor(request):
  try:
    user = request.user
    vendor = Vendor.objects.get(user=user)
  except:
    vendor = None
  return {'vendor': vendor}

def get_google_api_key(request):
  return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}