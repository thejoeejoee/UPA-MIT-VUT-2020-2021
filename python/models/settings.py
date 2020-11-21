from decouple import AutoConfig

config = AutoConfig()

INSTALLED_APPS = (
    'bulk_update_or_create',
    'django_extensions',
    'models.apps.ModelsAppConfig',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'postgres',
        'NAME': 'upa',
        'USER': 'django_admin',
        'PASSWORD': 'django_admin',
    }
}

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = config('SECRET_KEY')

USE_TZ = True

del config
