from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = BASE_DIR / 'static',
STATIC_ROOT = BASE_DIR / 'staticfiles'
TEMPLATES_DIRS = BASE_DIR / 'templates',

MEDIA_URL = '/section/'

MEDIA_ROOT = BASE_DIR / 'static/section'

