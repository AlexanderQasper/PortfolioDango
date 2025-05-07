import os
import magic
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def validate_file_type(file):
    """Validate file type based on MIME type and extension."""
    # Get file extension
    ext = os.path.splitext(file.name)[1][1:].lower()
    
    # Get MIME type
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file.read(1024))
    file.seek(0)  # Reset file pointer
    
    # Check if file type is allowed
    allowed_types = settings.ALLOWED_FILE_TYPES
    for category, extensions in allowed_types.items():
        if ext in extensions:
            return True
    
    raise ValidationError(
        _('File type not allowed. Allowed types: %(types)s'),
        params={'types': ', '.join([ext for exts in allowed_types.values() for ext in exts])}
    )

def validate_file_size(file):
    """Validate file size."""
    if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(
            _('File too large. Maximum size is %(max_size)s MB'),
            params={'max_size': settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)}
        )

def get_file_category(file):
    """Get file category based on extension."""
    ext = os.path.splitext(file.name)[1][1:].lower()
    for category, extensions in settings.ALLOWED_FILE_TYPES.items():
        if ext in extensions:
            return category
    return None

def generate_unique_filename(file):
    """Generate a unique filename for the uploaded file."""
    import uuid
    ext = os.path.splitext(file.name)[1]
    return f"{uuid.uuid4()}{ext}" 