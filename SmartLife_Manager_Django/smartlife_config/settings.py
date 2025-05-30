# SmartLife_Manager_Django/smartlife_config/settings.py

from pathlib import Path
import os # Diperlukan untuk os.path.join

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# QUICK-START DEVELOPMENT SETTINGS
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Ganti ini dengan kunci rahasia Anda sendiri yang kuat!
# Anda bisa menghasilkan kunci baru, misalnya menggunakan Djecrety (https://djecrety.ir/)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'ganti-dengan-kunci-rahasia-anda-yang-unik-dan-panjang')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # Set ke False saat production

ALLOWED_HOSTS = [] # Saat production, isi dengan domain Anda, misal ['www.smartlife.com', 'smartlife.com']


# APPLICATION DEFINITION

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'tasks.apps.TasksConfig',
    'schedule.apps.ScheduleConfig',
    'notes.apps.NotesConfig',
    'goals.apps.GoalsConfig',
    'contacts.apps.ContactsConfig',
    'education.apps.EducationConfig',
    'profiles.apps.ProfilesConfig'
    # Tambahkan aplikasi lain di sini nanti, misalnya 'notes', dll.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smartlife_config.urls' # Mengarah ke urls.py utama proyek Anda

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Beri tahu Django untuk mencari folder 'templates' di root proyek Anda
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True, # Agar Django juga mencari template di dalam folder aplikasi (mis. users/templates/)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth', # Membuat variabel 'user' tersedia di semua template
                'django.contrib.messages.context_processors.messages', # Untuk menampilkan pesan flash
            ],
        },
    },
]

WSGI_APPLICATION = 'smartlife_config.wsgi.application'


# DATABASE
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # File database akan ada di root proyek
    }
}


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# INTERNATIONALIZATION
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = 'id-id' # Ubah ke Bahasa Indonesia jika diinginkan

TIME_ZONE = 'Asia/Jakarta' # Sesuaikan dengan zona waktu Anda

USE_I18N = True

USE_TZ = True # Dianjurkan untuk menggunakan timezone-aware datetimes


# STATIC FILES (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = '/static/' # URL prefix untuk file statis

# Beri tahu Django untuk mencari folder 'static' di root proyek Anda
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# (Opsional) Jika Anda ingin mengelola file yang diunggah pengguna nanti
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# DEFAULT PRIMARY KEY FIELD TYPE
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# KONFIGURASI URL UNTUK LOGIN & LOGOUT
LOGIN_URL = 'users:login' # Nama URL (dengan namespace 'users') untuk halaman login
LOGIN_REDIRECT_URL = 'users:dashboard' # Ke mana diarahkan setelah login berhasil (jika tidak ada parameter 'next')
LOGOUT_REDIRECT_URL = 'home' # Ke mana diarahkan setelah logout (pastikan URL 'home' ada)

# (Opsional) Jika Anda menggunakan model User kustom di masa depan, definisikan di sini:
# AUTH_USER_MODEL = 'nama_app.NamaModelUserKustom'

# (Opsional) Untuk pesan flash dengan Bootstrap classes
# from django.contrib.messages import constants as messages_constants
# MESSAGE_TAGS = {
# messages_constants.DEBUG: 'debug',
# messages_constants.INFO: 'info',
# messages_constants.SUCCESS: 'success',
# messages_constants.WARNING: 'warning',
# messages_constants.ERROR: 'danger',
# }