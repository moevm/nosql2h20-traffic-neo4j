# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_toastr import Toastr

csrf_protect = CSRFProtect()
cors = CORS()
toastr = Toastr()