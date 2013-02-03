#!/usr/bin/env python

import time
import sys
import os
import json
import config
from flask import Flask, Request, Response, Blueprint
from views import home
application = Flask('wsgi')
application.secret_key = config.SECRET_KEY
application.config.from_object(config)

application.register_blueprint(home)

if __name__ == '__main__':
    application.run(debug=True)
