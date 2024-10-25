import os
from decouple import config


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
print("EMAIL_HOST_USER: ", EMAIL_HOST_USER)
print("EMAIL_HOST_PASSWORD: ", EMAIL_HOST_PASSWORD)

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
