from flask import render_template,url_for,flash,redirect,request,Blueprint
from Login import db,bcrypt
from Login.models import user,inventory,outgoing
from Login.users.form import (LoginForm,inputForm,searchCellForm,updateForm,searchsizeForm,sortedlistForm,
                        requestResetForm,restPasswordForm,searchRecentForm,searchLogForm,editLogForm,RegisterForm)
from flask_login import login_user,current_user,logout_user,login_required
from Login.users.utils import send_reset_email
from datetime import datetime
import pytz
from sqlalchemy import desc,func
from flask_mail import Message
from numpy.core.defchararray import upper


users=Blueprint('users',__name__)

@users.route('/index',methods=['GET','POST'])
@login_required
def index():
    form=inputForm()
    if form.validate_on_submit():
        data=inventory(place=form.place.data,size=form.size.data.upper().upper(),quantity=form.quantity.data,
                        sender=form.sender.data.upper(),description=form.description.data.upper(),n_b=form.n_b.data,
                        cell_no=form.cell_no.data,time=datetime.now(pytz.timezone('Asia/Kolkata')))
        db.session.add(data)
        db.session.commit()
        flash(f'Data Submitted','success')
        return redirect(url_for('users.index'))

    return render_template('index.html',form=form,title='Enter Data')

@users.route('/register',methods=['GET','POST'])
def register():
    return 'Fuck Off'
    """form=RegisterForm()
    if form.validate_on_submit():
        hp=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        temp=user(username=form.username.data,email=form.email.data,password=hp)
        db.session.add(temp)
        db.session.commit()
        flash(f'User has been registered','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form,title='Register')"""

@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    form=LoginForm()
    if form.validate_on_submit():
        user1=user.query.filter_by(username=form.username.data).first()
        if user1 and bcrypt.check_password_hash(user1.password,form.password.data):
            login_user(user1,remember=form.remember.data)
            flash(f'Logged in','success')
            return redirect(url_for('users.index'))
        else:
            flash('Login Unsuccessful. Please check username and password!','danger')
    return render_template('login.html',form=form,title='Login')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form=requestResetForm()
    if form.validate_on_submit():
        user2=user.query.filter_by(username=form.username.data).first()
        send_reset_email(user2)
        flash('An email has been sent with instructions to reset password','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password',form=form)
    
@users.route("/reset_token/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    user2=user.verify_reset_token(token)
    if user2 is None:
        flash(f'That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form=restPasswordForm()
    if form.validate_on_submit():
            hp=bcrypt.generate_password_hash(form.password.data)
            user2.password=hp
            db.session.commit()
            flash(f'You password has been updated','success')
            return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password',form=form)


@users.route('/searchcell',methods=['GET','POST'])
@login_required
def searchcell():
    form=searchCellForm()
    if form.validate_on_submit():
        entries=inventory.query.filter_by(place=form.place.data,cell_no=form.cell_no.data).order_by(desc(inventory.time)).all()
        flash(f'Search Results are here','success')
        return render_template('searchcell.html',entries=entries,form=form)
    return render_template('searchcell.html',form=form,title='Search Cell')

@users.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    if current_user.username!='admin':
        return 'You are not Admin'
    form=updateForm()
    if form.validate_on_submit():
        temp=inventory.query.get(id)
        if form.quantity.data> temp.quantity:
            flash(f'You cannot send quantity greater than present','danger')
            return render_template('update.html',title='Update',form=form)
        temp2=outgoing(cell_no=temp.cell_no,quantity=form.quantity.data,place=temp.place,n_b=temp.n_b,
                        size=temp.size,recipient=form.recipient.data.upper(),description=temp.description,
                        time=datetime.now(pytz.timezone('Asia/Kolkata')))
        temp.quantity=temp.quantity-form.quantity.data
        if temp.quantity==0:
            db.session.delete(temp)
        db.session.add(temp2)
        db.session.commit()
        flash(f'Entry Updated','success')
        return redirect(url_for('users.index'))
    return render_template('update.html',title='Update',form=form)

@users.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    if current_user.username!='admin':
        return 'You are not Admin'
    form=inputForm()
    temp=inventory.query.get(id)
    if form.validate_on_submit():
        temp.cell_no=form.cell_no.data
        temp.place=form.place.data
        temp.quantity=form.quantity.data
        temp.sender=form.sender.data.upper()
        temp.n_b=form.n_b.data
        temp.description=form.description.data.upper()
        temp.size=form.size.data.upper()
        temp.time=datetime.now(pytz.timezone('Asia/Kolkata'))
        if temp.quantity==0:
            db.session.delete(temp)
        db.session.commit()
        flash(f'Data has been edited successfully','success')
        return redirect(url_for('users.index'))
    elif request.method=='GET':     
        form.cell_no.data=temp.cell_no
        form.place.data=temp.place
        form.quantity.data=temp.quantity
        form.sender.data=temp.sender
        form.n_b.data=temp.n_b
        form.description.data=temp.description
        form.size.data=temp.size
    if current_user.username=='admin':
        return render_template('edit.html',form=form,title='Edit')
    else:
        return 'You are not admin'

@users.route('/editlog/<int:id>',methods=['GET','POST'])
@login_required
def editlog(id):
    if current_user.username!='admin':
        return 'You are not Admin'
    form=editLogForm()
    temp=outgoing.query.get(id)
    if form.validate_on_submit():
        temp.cell_no=form.cell_no.data
        temp.place=form.place.data
        temp.quantity=form.quantity.data
        temp.recipient=form.recipient.data.upper()
        temp.n_b=form.n_b.data
        temp.description=form.description.data.upper()
        temp.size=form.size.data.upper()
        temp.time=datetime.now(pytz.timezone('Asia/Kolkata'))
        if temp.quantity==0:
            db.session.delete(temp)
        db.session.commit()
        flash(f'Log has been edited successfully','success')
        return redirect(url_for('users.index'))
    elif request.method=='GET':     
        form.cell_no.data=temp.cell_no
        form.place.data=temp.place
        form.quantity.data=temp.quantity
        form.recipient.data=temp.recipient
        form.n_b.data=temp.n_b
        form.description.data=temp.description
        form.size.data=temp.size
    if current_user.username=='admin':
        return render_template('editlog.html',form=form)
    else:
        return 'You are not admin'

@users.route('/viewlog',methods=['GET','POST'])
@login_required
def viewlog():
    if current_user.username!='admin':
        return 'You are not Admin'
    form=searchLogForm()
    if form.validate_on_submit():
        entry=outgoing.query.filter(outgoing.time>=form.start.data).filter(outgoing.time<=form.end.data).order_by(desc(outgoing.time)).all()
        return render_template('viewlog.html',form=form,entry=entry)
    if current_user.username=='admin':
        return render_template('viewlog.html',form=form)
    else:
        return 'You are not admin'

@users.route('/viewrecent',methods=['GET','POST'])
@login_required
def viewrecent():
    if current_user.username!='admin':
        return 'You are not Admin'
    form=searchRecentForm()
    if form.validate_on_submit():
        entry=inventory.query.filter(inventory.time>=form.start.data).filter(inventory.time<=form.end.data).order_by(desc(inventory.time)).all()
        return render_template('recent.html',form=form,entry=entry)
    if current_user.username=='admin':
        return render_template('recent.html',form=form)
    else:
        return 'You are not admin'

@users.route('/searchsize',methods=['GET','POST'])
@login_required
def searchsize():
    form=searchsizeForm()
    if form.validate_on_submit():
        if form.size.data=="" and form.sender.data=="" and form.description.data.upper()=="":
            flash(f'Please enter data to search','danger')
            return render_template('searchsize.html',form=form)
        if form.size.data=="":
            if form.sender.data=="":
                entry=inventory.query.filter_by(description=form.description.data.upper()).order_by(desc(inventory.time)).all()
            elif form.description.data.upper()=="":
                entry=inventory.query.filter_by(sender=form.sender.data.upper()).order_by(desc(inventory.time)).all()
            else:
                entry=inventory.query.filter_by(description=form.description.data.upper(),sender=form.sender.data.upper()).order_by(desc(inventory.time)).all()
        elif form.sender.data=="":
            if form.size.data=="":
                entry=inventory.query.filter_by(description=form.description.data.upper()).order_by(desc(inventory.time)).all()
            elif form.description.data.upper()=="":
                entry=inventory.query.filter_by(size=form.size.data.upper()).order_by(desc(inventory.time)).all()
            else:
                entry=inventory.query.filter_by(description=form.description.data.upper(),size=form.size.data.upper()).order_by(desc(inventory.time)).all()
        if form.description.data=="":
            if form.sender.data=="":
                entry=inventory.query.filter_by(size=form.size.data.upper()).order_by(desc(inventory.time)).all()
            elif form.size.data.upper()=="":
                entry=inventory.query.filter_by(sender=form.sender.data.upper()).order_by(desc(inventory.time)).all()
            else:
                entry=inventory.query.filter_by(size=form.size.data.upper(),sender=form.sender.data.upper()).order_by(desc(inventory.time)).all()
        return render_template('searchsize.html',entry=entry,title='Search Size',form=form)
    return render_template('searchsize.html',form=form,title='Search Size')

@users.route('/sortedlist',methods=['GET','POST'])
@login_required
def sortedlist():
    if current_user.username!='admin':
        return 'You are not Admin'
    form=sortedlistForm()
    total=0
    if form.validate_on_submit():
        #entry=inventory.query.filter_by(place=form.place.data).all()
        entry=inventory.query.with_entities(inventory.n_b,inventory.size,func.sum(inventory.quantity).label('quan'),
                    inventory.description).filter_by(place=form.place.data).group_by(inventory.size,inventory.description).all()
        total = inventory.query.with_entities(func.sum(inventory.quantity).label('totals')).filter_by(place=form.place.data).first()
        return render_template('sortedlist.html',form=form,entry=entry,total=total)

    return render_template('sortedlist.html',form=form,total=total)


