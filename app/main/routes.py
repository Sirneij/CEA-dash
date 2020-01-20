from flask import url_for, render_template, request, Blueprint, Response, jsonify
from flask_login import current_user, login_required
from app.models import User
import os, shutil, re, cgi, json, random, time
from datetime import datetime
main = Blueprint('main', __name__)

@main.route('/index')
@login_required
def index():
    inactiveCustomers = 34546
    activeCustomers = 7654984
    numberOfCalls = 123456
    numberOfRetailCustomers = 455674666
    return render_template('pages/index.html', numberOfCalls=numberOfCalls, numberOfRetailCustomers=numberOfRetailCustomers, inactiveCustomers=inactiveCustomers, activeCustomers=activeCustomers)


@main.route('/emailescalation')
@login_required
def emailescalation():
    return render_template( 'pages/emailescalation.html', title='Email & Escalation', description='ipNX Dashboard')


@main.route('/retailsupport')
@login_required
def retailsupport():
    totalCalls = 144452637733663

    return render_template( 'pages/retailsupport.html',  title='Retail Support Center', description='ipNX Dashboard', totalCalls=totalCalls)
@main.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield "data:{}\n\n".format(json_data)
            time.sleep(1)

    return Response(generate_random_data(), mimetype='text/event-stream')


@main.route('/ishop')
@login_required
def ishop():
    return render_template( 'pages/ishop.html', title='i-Shop', description='ipNX Dashboard' )

@main.route('/ticketingresolution')
@login_required
def ticketingresolution():
    return render_template( 'pages/ticketingresolution.html', title='Ticketing and Resolution', description='ipNX Dashboard' )

@main.route('/social')
@login_required
def social():

    return render_template( 'pages/social.html', title='Social Media', description='ipNX Dashboard')

@main.route('/cxretention')
@login_required
def cxretention():
    return render_template('pages/cxretention.html', title='Customer Experience and Retention', description='ipNX Dashboard')