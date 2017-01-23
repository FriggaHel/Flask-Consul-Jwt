#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Utils.exceptions import BadRequestException, \
    ForbiddenAccessException, NotFoundException, \
    NotAuthenticatedException, NotImplementedException, \
    HttpConflictException

from flask import jsonify as fjsonify

def init_app(app):
    @app.errorhandler(401)
    def page_unauthorized(e):
        return fjsonify({
            'message': 'Unauthorized',
            'code': 401
        }), 401

    @app.errorhandler(403)
    def page_forbidden(e):
        return fjsonify({
            'message': 'Forbidden',
            'code': 403
        }), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return fjsonify({
            'message': 'Not Found',
            'code': 404
        }), 404

    @app.errorhandler(BadRequestException)
    def error_bad_Request(e):
        return fjsonify({
            'message': 'Bad Request',
            'code': 400
        }), 400

    @app.errorhandler(ForbiddenAccessException)
    def error_not_authenticated(e):
        return fjsonify({
            'message': 'You are not authorized to access this',
            'code': 401
        }), 401

    @app.errorhandler(NotAuthenticatedException)
    def error_forbidden(e):
        return fjsonify({
            'message': 'You are not authorized to access this',
            'code': 403
        }), 403


    @app.errorhandler(NotFoundException)
    def error_not_found():
        return fjsonify({
            'message': 'Resource has not been found',
            'code': 404
        }), 404

    @app.errorhandler(HttpConflictException)
    def error_conflict(e):
      return fjsonify({
            'message': 'Conflict',
            'code': 409
      }), 409

    @app.errorhandler(NotImplementedException)
    def error_not_implemented(e):
        return fjsonify({
            'message': 'This feature is for now Not Implemented',
            'code': 501
        }), 501

    @app.errorhandler(Exception)
    def error_internal_error(e):
      return fjsonify({
            'message': 'Internal server error',
            'code': 500
      }), 500
