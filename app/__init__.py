from flask import Flask
from flask import request

app = Flask(__name__)

app.config.from_object('settings')

__import__('app.views')
