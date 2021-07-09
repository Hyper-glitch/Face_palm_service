from flask import Blueprint, request, url_for, render_template, flash, session
from werkzeug.utils import redirect
from flask_sqlalchemy import sqlalchemy
from database import db
from forms import RegisterForm
from models import User
import logging


auth = Blueprint('auth', __name__)
LOGGER = logging.getLogger(__name__)


@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = RegisterForm()

    if request.method == 'POST':
        name = request.form['name']
        LOGGER.info(f'Username {name} data received')

        conf = session.get('conf', None)
        LOGGER.info(f'Confidence = {conf} data received')

        user = User.query.filter_by(name=name).first()
        LOGGER.info(f'Searching username {name} in the database')

        if user and conf >= 50:
            session['logged_in'] = True
            session['name'] = name
            flash('You are now logged in', 'success')
            LOGGER.info(f'Username {name} now logged in')
            return redirect(url_for('main.profile', name=name))
        else:
            LOGGER.info(f'Username {name} incorrect or confidence value < 50%')
            flash('Please, check your Face or Username and try again.', 'warning')
            return redirect(url_for('auth.sign_in'))

    # if the above check passes, then we know the user has the right credentials
    return render_template('sign_in.html', title='Sign In', form=form)


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        session['name'] = name
        LOGGER.info(f'Username data received')
        LOGGER.debug(f'Username data = {name}')

        user = User(name=name)
        LOGGER.info(f'Username {name} created')

        db.session.add(user)
        LOGGER.info(f'Username {name} added to database')

        try:
            db.session.commit()
            LOGGER.info(f'Username {name} commitedd to database')
        except sqlalchemy.exc.IntegrityError:
            LOGGER.critical(f'Username {name} is already exists.')
            flash(f"Username {name} is already exists.", 'danger')
            return redirect(url_for('auth.sign_up'))

        flash('Thanks for registering, you can Sign in', 'success')
        LOGGER.info(f'Username {name} registered successfully')
        return redirect(url_for('auth.sign_in'))
    return render_template('sign_up.html', title='Sign Up', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    name = session.get('name', None)
    session.clear()
    flash('You are now logged out', 'success')
    LOGGER.info(f'Username {name} logged out')
    return redirect(url_for('auth.sign_in'))
