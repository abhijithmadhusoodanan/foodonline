from vendor.models import Vendor

def get_vendor(request):
  try:
    user = request.user
    vendor = Vendor.objects.get(user=user)
  except:
    vendor = None
  return {'vendor': vendor}
