#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import abort
from flask import jsonify as flask_jsonify

from Models.auth import AdminUser

def authenticate(username, password):
    return None

def identity(payload):
    return AdminUser.new_from_token(payload)

def has_role(identity, roles_required=[]):
    def real_decorator(f):
        def wrapped_f(*args, **kwargs):
            for r in roles_required:
                if identity.roles is None or r not in identity.roles:
                    print('%s does not contains %s role' % (identity, r))
                    abort(401)
            return f(*args, **kwargs)
        return wrapped_f
    return real_decorator
