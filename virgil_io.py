import flask
from flask import Flask, render_template, url_for, send_file
from config import Config

import io
from io import BytesIO
import os
import sys

from PIL import Image
import tensorflow as tf

from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
app = Flask( __name__ )

'''
$env:FLASK_APP = "virgil_io"
$env:POSTGRES_URL = "127.0.0.1:5432"
$env:POSTGRES_USER = "rfitz123"
$env:POSTGRES_PW = "321ztifr"
$env:POSTGRES_DB = "virgil-io"
'''

# Logic

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

# Create an application

APP = Flask(__name__)
APP.config.from_object(Config)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

APP.config['SQLALCHEMY_DATABASE_URI'] = DB_URL # Silence the deprecation warning
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(APP)

db = SQLAlchemy(APP)

# Inject into webpage


@APP.route('/virgil_io/static/images/')
def serve_image():
    img = Image.new('RGB', (512, 512), (255, 0, 0))
    return serve_pil_image(img)


@APP.route('/virgil_io/')
def index():
    return flask.render_template('index.html')


if __name__ == '__main__':
    APP.debug = True
    APP.run()
