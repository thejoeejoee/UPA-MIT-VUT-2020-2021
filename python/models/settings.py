from decouple import AutoConfig

config = AutoConfig()

INSTALLED_APPS = (
    'models.apps.ModelsAppConfig',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'upa',
        'USER': 'computer',
        'PASSWORD': 'computer',
        'HOST': 'postgres',
    }
}

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = config('SECRET_KEY')

del config
