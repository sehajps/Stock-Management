from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,SelectField,DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, NumberRange,ValidationError,EqualTo,Regexp
from Login.models import user
olimit=100
class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired()])
    submit=SubmitField('Login')
class inputForm(FlaskForm):
    place=SelectField('Place',validators=[DataRequired()],choices=[('office','Office'),('godown','Godown')])
    cell_no=IntegerField('Cell Number',validators=[DataRequired(),NumberRange(min=0,max=olimit,message='Please enter number in limit')])
    n_b=SelectField('Product',validators=[DataRequired()],choices=[('nut','Nut'),('bolt','Bolt'),('washer','Washer')])
    size=StringField('Size',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed"),DataRequired()])
    quantity=IntegerField('Quantity (in kg)',validators=[DataRequired(),NumberRange(min=0,message='Please enter number in limit')])
    description=StringField('Description',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed"),DataRequired()])
    sender=StringField('Sender',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed"),DataRequired()])
    submit=SubmitField('Submit')
class searchCellForm(FlaskForm):
    place=SelectField('Place',validators=[DataRequired()],choices=[('office','Office'),('godown','Godown')])
    cell_no=IntegerField('Cell Number',validators=[DataRequired(),NumberRange(min=0,max=olimit,message='Please enter number in limit')])
    submit=SubmitField('Search')
class updateForm(FlaskForm):
    quantity=IntegerField('Quantity',validators=[DataRequired(),NumberRange(min=0,message='Please enter number in limit')])
    recipient=StringField('Recipient',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed"),DataRequired()])
    submit=SubmitField('Update')
class searchsizeForm(FlaskForm):
    size=StringField('Size',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed")])
    description=StringField('Description',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed")])
    sender=StringField('Sender',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed")])
    submit=SubmitField('Search')

class sortedlistForm(FlaskForm):
    place=SelectField('Place',validators=[DataRequired()],choices=[('office','Office'),('godown','Godown')])
    submit=SubmitField('Search')

class requestResetForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    submit=SubmitField('Request Password Reset') 

    def vaidate_email(self,email):
        user2=user.query.filter_by(email=email.data).first()
        if user2 is None:
            raise ValidationError('Please Enter Correct Email')

class restPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Passowrd',validators=[DataRequired(),EqualTo('password')])   
    submit=SubmitField('Reset Password')

def my_date_check(FlaskForm, field):
        if field.start>field.end:
            raise ValidationError('End Date must be greater than start date. Stupid')

class searchLogForm(FlaskForm):
    start=DateField('Start Date',format='%Y-%m-%d')
    end=DateField('End Date',format='%Y-%m-%d')
    submit=SubmitField('Search')

class searchRecentForm(FlaskForm):
    start=DateField('Start Date',format='%Y-%m-%d')
    end=DateField('End Date',format='%Y-%m-%d')
    submit=SubmitField('Search')
    
class editLogForm(FlaskForm):
    place=SelectField('Place',validators=[DataRequired()],choices=[('office','Office'),('godown','Godown')])
    cell_no=IntegerField('Cell Number',validators=[DataRequired(),NumberRange(min=0,max=olimit,message='Please enter number in limit')])
    n_b=SelectField('Product',validators=[DataRequired()],choices=[('nut','Nut'),('bolt','Bolt'),('washer','Washer')])
    size=StringField('Size',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed"),DataRequired()])
    quantity=IntegerField('Quantity',validators=[DataRequired(),NumberRange(min=0,message='Please enter number in limit')])
    description=StringField('Description',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed"),DataRequired()])
    recipient=StringField('Recipient',validators=[Regexp(r'^[\w.@+-]+$',message="Spaces are not allowed"),DataRequired()])
    submit=SubmitField('Submit')