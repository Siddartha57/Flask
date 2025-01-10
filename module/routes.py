from module import app,db,session
from flask import render_template, flash, redirect, url_for,session
from module.forms import Register, Login, Booking
from unicodedata import category
from module.models import User, Busses
from flask_login import login_user, logout_user, login_required
from geopy.geocoders import Nominatim
import numpy as np

global x
x=0

@app.route('/')
def base_page():
    return render_template('base.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = Register()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email_address= form.email_address.data, password=form.password1.data,phone=form.phone.data )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Mr.{new_user.username} your account has been created sucsessfully and you are logged in',category='success')
        return redirect(url_for('home_page'))
    if form.errors !={}:
        for error in form.errors.values():
            flash(f'There is an error while creating account {error}', category='danger')
            return render_template('register.html',form=form)
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = Login()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            session['username'] = form.username.data
            login_user(attempted_user)
            flash(f'Welcome Mr.{attempted_user.username}',category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password not matched', category='danger')

    return render_template('login.html', form=form)

@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/booking', methods=['POST','GET'])
@login_required
def booking_page():
    form = Booking()
    if form.validate_on_submit():
        global From, To, lat1, lon1, lat2, lon2, Date
        From = form.From.data
        To = form.To.data
        Date = form.Date.data
        geolocator = Nominatim(user_agent="my_user_agent")
        city1 = From
        city2 = To
        country = "India"
        loc1 = geolocator.geocode(city1 + ',' + country)
        loc2 = geolocator.geocode(city2 + ',' + country)

        lat1 = loc1.latitude
        lon1 = loc1.longitude

        lat2 = loc2.latitude
        lon2 = loc2.longitude
        return redirect(url_for('bus_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(f'Select the place correctly {error}', category='danger')
    return render_template('ticket_book.html', form=form)

@app.route('/dist')
def distance_cal():
    global lat1,lon1,lat2,lon2,dist
    r = 6371
    def deg_to_rad(degrees):
        return degrees * (np.pi / 180)
    def distcalculate(lat1, lon1, lat2, lon2):
        d_lat = deg_to_rad(lat2 - lat1)
        d_lon = deg_to_rad(lon2 - lon1)
        a = np.sin(d_lat / 2) ** 2 + np.cos(deg_to_rad(lat1)) * np.cos(deg_to_rad(lat2)) * np.sin(d_lon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return r * c
    dist = str(int(distcalculate(lat1,lon1,lat2,lon2)))
    return redirect(url_for('payment_page'))

@app.route('/payment')
@login_required
def payment_page():
    global dist,From,To,Time, Amount, Date,x
    Time = int(int(dist)/45)
    Amount = int(dist)*3
    x=x+1
    return render_template('payment.html',dist=dist,From=From,To=To, Time=Time, Amount=Amount, Date=Date)

@app.route('/my_booking')
@login_required
def my_booking_page():
    global Amount
    if x!=0:
        return render_template('my_booking.html',Amount=Amount)
    else:
        flash(f'Ticket not booked yet',category='info')
        return redirect(url_for('home_page'))

@app.route('/busses')
@login_required
def bus_page():
    global From,To,Date
    buses= Busses.query.all()
    return render_template('bus.html',buses=buses,From=From,To=To, Date=Date)


@app.route('/logout')
def logout_page():
    logout_user()
    session['username'] = None
    flash(f'logged out sucessfully',category='info')
    return redirect(url_for('base_page'))