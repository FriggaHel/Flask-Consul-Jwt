#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

health = Blueprint('health', __name__, url_prefix='/health')

@health.route("/")
def health_root():
    return jsonify({
        'message': 'OK',
        'code': 200
    }), 200
