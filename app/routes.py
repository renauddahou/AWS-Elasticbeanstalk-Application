from flask import render_template, redirect, url_for, flash
from app import application # importing the application module
from app.forms import SignUpForm
import boto3

# dynamodb
db = boto3.resource('dynamodb', region_name='us-east-2')
table = db.Table('signuptable')

# sns
notification = boto3.client('sns', region_name='us-east-2')
topic_arn = 'arn:aws:sns:us-east-2:614768946157:flask-aws-sns'


@application.route('/')
@application.route('/home')
def home_page():
    return render_template('home.html')


@application.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        table.put_item(
            Item={
                'name': form.name.data, 'email': form.email.data,
                'mobile': form.mobile.data, 'country': form.country.data,
                'newsletter': form.newsletter.data
            }
        )
        msg = 'Congratulations !!! {} is now a Premium Member !'.format(form.name.data)
        flash(msg)
        # email to owner
        email_message = '\nname: {} ' \
                        '\nmobile: {} ' \
                        '\nemail: {} ' \
                        '\ncountry: {}'.format(form.name.data, form.mobile.data, form.email.data, form.country.data)
        notification.publish(Message=email_message, TopicArn=topic_arn, Subject="You've Got A Mail")
        return redirect(url_for('home_page'))
    return render_template('signup.html', form=form)
