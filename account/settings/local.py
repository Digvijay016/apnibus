from .base import *
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
#
# DEBUG = False
#
# sentry_sdk.init(
#     dsn="https://52f08e8241574df69c1c68590673f6c1@o1371657.ingest.sentry.io/6676005",
#     integrations=[
#         DjangoIntegration(),
#     ],
#
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,
#
#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )

ENVIRONMENT = 'local'
ALLOWED_HOSTS = ['*']

# DATABASES = {
#         'default': {
#                 # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
#                 # 'NAME': "postgres",
#                 # 'USER': "ab_api_user",
#                 # 'PASSWORD': "3CKyynMLJTAp7cXt",
#                 # 'HOST': "test-ab-api-db.ckp07u2jsmkv.ap-south-1.rds.amazonaws.com",
#                 # 'HOST' : 'staging.ckp07u2jsmkv.ap-south-1.rds.amazonaws.com',
#                 # 'PORT': 5432
#                 # 'ENGINE': 'django.db.backends.postgresql',
#                 # 'NAME': 'mydatabase',
#                 # 'USER': 'mydatabaseuser',
#                 # 'PASSWORD': 'mypassword',
#                 # 'HOST': 'localhost',
#                 # 'PORT': '',
#         }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dummy_3.sqlite3',
    }
}

# Cashfree Payment Gateway Integration
CASHFREE_API_ENDPOINT = "https://sandbox.cashfree.com/pg"

# TODO: Will add credentials in environment file
CASHFREE_APPID = "2582424543ce560faf0369bf99242852"
CASHFREE_SECRET_KEY = "2b1e327adf5b3796491440bd340d050e105a0f85"
CASHFREE_API_VERSION = "2022-01-01"
SERVER_URL = "https://2ff8-2401-4900-40ba-49b6-8531-e7f4-753b-c139.ngrok.io"
