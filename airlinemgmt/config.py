import os
import json

# with open('../config.json') as config_file:
#     config = json.load(config_file)

class Config:
    SECRET_KEY = '8f143d1fa5bd5094887f0f2176d08ec3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = config.get('EMAIL_USER')
    # MAIL_PASSWORD = config.get('EMAIL_PASS')