""" Custom storages for AWS file storage. """
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """ Custom static file storage location. """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """ Custom media file storage location. """
    location = settings.MEDIAFILES_LOCATION
