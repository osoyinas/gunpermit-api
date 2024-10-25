import os
from decouple import config


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER', "example@gmail.com")
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', "password")

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
