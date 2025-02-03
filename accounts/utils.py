
def detectuser(user):
  if user.role == 1:
    return 'vendordashboard'
  elif user.role == 2:
    return 'custdashboard'
  elif user.role == None and user.is_superadmin:
    return '/admin'