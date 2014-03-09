#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from flask import *
    from conf import conf
except ImportError:
    import sys, warnings, traceback
    warnings.warn("matchtpl.web module need package Flask to run: http://flask.pocoo.org/")
    traceback.print_exc()
    sys.exit(-1)


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host=conf.get('host'), port=conf.get('port'))
