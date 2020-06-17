import os
class Config:
    SECRET_KEY=os.urandom(32)
    SQLALCHEMY_DATABASE_URI='mysql://sql12349216:G3bCkSkCQ9@sql12.freemysqlhosting.net/sql12349216'
    WHOOSH_BASE='whoosh'
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('EMAIL_USER')
    MAIL_PASSWORD=os.environ.get('EMAIL_PASS')