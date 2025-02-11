from django.core.exceptions import ValidationError
import os

def validate_image_extension(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.jpg', '.jpeg', '.png']
  if not ext.lower() in valid_extensions:
    raise ValidationError("Invalid image extension and the supported extensions are" + str(valid_extensions))