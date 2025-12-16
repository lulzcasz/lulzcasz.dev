from .base import *

DEBUG = False

AWS_S3_REGION_NAME = getenv("AWS_S3_REGION_NAME")

CSRF_TRUSTED_ORIGINS = getenv('DJANGO_CSRF_TRUSTED_ORIGINS').split(',')
