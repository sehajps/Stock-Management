from Login import db,login_manager,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import pytz
@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

class user(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password=db.Column(db.String(60),nullable=False)

    def get_reset_token(self,expires_seconds=1800):
        s=Serializer(app.config['SECRET_KEY'],expires_seconds)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s=Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return user.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class inventory(db.Model,UserMixin):
    __searchable__=['n_b','size','description','sender']
    id=db.Column(db.Integer,primary_key=True)
    place=db.Column(db.String(6),nullable=False)
    cell_no=db.Column(db.Integer, nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    n_b=db.Column(db.String(10), nullable=False)
    size=db.Column(db.String(100), nullable=False)
    time=db.Column(db.DateTime,default=datetime.now(pytz.timezone('Asia/Kolkata')))
    description=db.Column(db.String(50),nullable=False)
    sender=db.Column(db.String(100),nullable=False)

    def __repr__(self):
       return f"User('{self.id}','{self.place}','{self.cell_no}','{self.quantity}','{self.size}','{self.description}','{self.sender}')"
class outgoing(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    place=db.Column(db.String(6),nullable=False)
    cell_no=db.Column(db.Integer, nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    n_b=db.Column(db.String(10), nullable=False)
    size=db.Column(db.String(100), nullable=False)
    time=db.Column(db.DateTime,default=datetime.now(pytz.timezone('Asia/Kolkata')))
    description=db.Column(db.String(50),nullable=False)
    recipient=db.Column(db.String(100),nullable=False)

    def __repr__(self):
       return f"User('{self.id}','{self.place}','{self.cell_no}','{self.quantity}','{self.size}','{self.description}','{self.recipient}')"