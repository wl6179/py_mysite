# -*- coding: utf-8 -*-
# Django settings for mysite project.
import logging
import os.path


DEBUG = True
TEMPLATE_DEBUG = DEBUG

HERE = os.path.dirname(os.path.abspath(__file__))


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '666666',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {  
                    'init_command': 'SET storage_engine=INNODB',  
        },#制定只用MySQL的InnoDB引擎！暂时OK没发现什么问题！！~
    }
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'test',                      # Or path to database file if using sqlite3.
#        'USER': 'abc',                      # Not used with sqlite3.
#        'PASSWORD': '666666',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'
#TIME_ZONE = 'PRC'
#TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'
#LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(HERE, 'media').replace('\\','/')
#MEDIA_ROOT = 'D:\Test\DjangoWeb\mysite\media'

#CAPTCHA_FONT = os.path.join(HERE,'static/Vera.ttf')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#import os
#STATIC_ROOT = os.path.join( os.path.dirname(__file__), 'static').replace('\\', '/')
STATIC_ROOT = os.path.join( HERE, 'static' ).replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ("images", os.path.join( STATIC_ROOT,'images' ).replace('\\','/')),
    ("css",    os.path.join( STATIC_ROOT,'css' ).replace('\\','/')),
    ("js",     os.path.join( STATIC_ROOT,'js' ).replace('\\','/')),
    
    ("javascript", os.path.join( STATIC_ROOT,'javascript' ).replace('\\','/')),		#为了能让Ueditor文件可以访问！
    #HERE + STATIC_URL,
    #("media",  os.path.join(MEDIA_ROOT,'media').replace('\\','/')),
    #("media",  MEDIA_ROOT),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8w(l(#&c7zqmdrck6$v4g&j&aolvmt4s*)m$(fh1r010-vz%2)'




#UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join( HERE, 'media/temp/' ).replace('\\', '/')
# for user upload
ALLOW_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
# unit byte
#ALLOW_MAX_FILE_SIZE = 1024 * 1024




# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'django.middleware.locale.LocaleMiddleware',
    
    
    "functions.IgnoreCrsfMiddleware",				#为了让Ueditor的flash上传功能可以忽略掉Csrf屏蔽的——自定义中间件！（清理浏览器缓存先！）
    'django.middleware.csrf.CsrfViewMiddleware',		#该中间件必须在 SessionMiddleware 之后 执行，因此在列表中 CsrfMiddleware 必须出现在SessionMiddleware 之前 （因为响应中间件是自后向前执行的）。CsrfMiddleware 必须在 GZipMiddleware 之后执行。
    #'django.middleware.csrf.CsrfResponseMiddleware',	#？要加它吗？？！
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    'd:/Test/DjangoWeb/mysite/templates',
    #os.path.join( HERE, 'templates' ).replace('\\','/'),
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
     
    'mysite.books',
    'mysite.news',
    'mysite.polls',
    'mysite.classes',
    'mysite.classes2',
    'mysite.tests',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    
    #################################################'south',		#South数据库迁移组件！
    #'south',
    
    
    
    'django.contrib.comments',		#点评插件
    
    
    
    
    #'depot.depotapp',			#购物车插件~
    
    
    
    
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
