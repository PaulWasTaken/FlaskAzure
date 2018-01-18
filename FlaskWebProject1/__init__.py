"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
import FlaskWebProject1.views
