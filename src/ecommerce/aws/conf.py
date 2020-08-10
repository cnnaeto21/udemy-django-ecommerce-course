import datetime

AWS_GROUP_NAME = "udemy-ecommerce-group"
AWS_USER_NAME = "udemy-ecommerce"
AWS_ACCESS_KEY_ID = "AKIAUTVRCI47REI4JLOS"
AWS_SECRET_ACCESS_KEY = "4GUx1eHr2QUNs7xFAmn6mb3DBvBN/WYDOlVJivTI"


# AWS_ACCESS_KEY_ID = "<your_access_key_id>"
# AWS_SECRET_ACCESS_KEY = "<your_secret_access_key>"
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'ecommerce.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'ecommerce.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'udemy-ecommerce-bucket'
S3DIRECT_REGION = 'us-east-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
'Expires': expires,
'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}


PROTECTED_DIR_NAME = 'protected'
PROTECTED_MEDIA_URL = '//%s.s3.amazon.com/%s/' %(AWS_STORAGE_BUCKET_NAME, PROTECTED_DIR_NAME)

AWS_DOWNLOAD_EXPIRE = 5000


AWS_QUERYSTRING_AUTH = False