from flask import Flask
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("jaffucci.config")
app.config.from_pyfile("jaffucci_config.cfg")

import jaffucci.views
