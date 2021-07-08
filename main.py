import os
from flask import Blueprint, render_template, request, url_for, session
from werkzeug.utils import secure_filename, redirect
from camera import VideoCamera, RECOGNIZER
import logging

main = Blueprint('main', __name__)
ALLOWED_EXTENSIONS = {'webm', 'mp4'}
LOGGER = logging.getLogger(__name__)


@main.route('/', methods=('GET', 'POST'))
def index():
    return render_template('home.html')


@main.route('/profile', methods=('GET', 'POST'))
def profile():
    return render_template('profile.html')


@main.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('contact.html')


def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/upload', methods=['POST'])
def upload_file():
    # Get the video blob file from server side
    file = request.files['video']
    LOGGER.info('The video file accepted')

    # Get the username from user via name of the video blob
    user_name = request.form['username']
    LOGGER.info('The username field accepted')

    # Get the state to distinguish sign up from sign in
    attribute = request.form['attribute']
    LOGGER.info('The attribute field accepted')

    # if user_name == None:
    #     flash('Please enter your username!', 'warning')
    #     return redirect(url_for('auth.sign_up'))

    if attribute == "sign_up":
        LOGGER.info('The attribute field is equal SIGN UP')
        filename = secure_filename(file.filename)

        # Check and create a dir of a User
        if not os.path.isdir(f'./datasets/{user_name}'):
            os.mkdir(f'./datasets/{user_name}')
            LOGGER.info(f'The {user_name} directory was created in dataset')

        file.save(os.path.join(f'./datasets/{user_name}', filename))
        LOGGER.info(f'The {filename} saved in dataset')

        LOGGER.info(f'Starting create_recognizer function..')
        create_recognizer(user_name)
        LOGGER.info(f'Stop create_recognizer function.')
        return redirect(url_for('auth.sign_in'))

    elif attribute == "sign_in":
        LOGGER.info('The attribute field is equal SIGN IN')
        filename = secure_filename(file.filename)

        # Check and create a dir of a User
        if not os.path.isdir(f'./tempdata/{user_name}'):
            os.mkdir(f'./tempdata/{user_name}')
            LOGGER.info(f'The {user_name} directory was created in tempdata')

        file.save(os.path.join(f'./tempdata/{user_name}', filename))
        LOGGER.info(f'The {filename} saved in tempdata')

        # Get the confidence value between the registered users and trying to sign in
        conf = recognize(user_name)

        session['conf'] = conf
    return f"{conf}"


@main.route('/create_recognizer', methods=['POST'])
def create_recognizer(user_name):
    # Creating an instance of the class
    LOGGER.info(f'Creating {user_name} to SIGN UP')
    rec = VideoCamera(username=user_name)
    LOGGER.debug(f"{rec}")
    LOGGER.info(f'{user_name} created!')

    # To transform the video to pics
    rec.transform_to_jpeg(count=10)

    # To delete the video from storage
    rec.delete_video()

    # To create a trainer file to recognize
    faces, labels = rec.create_recognizer()
    LOGGER.info(f' faces, labels returned from create_recognizer function')

    # Training the file to recognize
    RECOGNIZER.train(faces, labels)
    LOGGER.info(f'The trainer file compiled')

    # Save the training file in datasets
    RECOGNIZER.save(f"datasets/{user_name}/{user_name}" + ".yml")
    LOGGER.info(f'The trainer file saved in datasets')


@main.route('/recognize', methods=['POST'])
def recognize(user_name):
    LOGGER.info(f'Creating {user_name} to SIGN IN')
    rec = VideoCamera(username=user_name)
    LOGGER.debug(f"{rec}")
    LOGGER.info(f'{user_name} created!')

    # Get confidence value in % to compare 2 faces
    conf = round(100-rec.recognize(), 1)

    LOGGER.info(f'The confidence value received from recognizer')

    # To delete the video from storage
    rec.delete_video_from_tempdata()

    LOGGER.debug(f"Confidence = {conf} %")
    return conf
