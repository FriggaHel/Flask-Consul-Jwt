#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class BadRequestException(Exception):
    def __init__(self):
        Exception.__init__(self)

class ForbiddenAccessException(Exception):
    def __init__(self):
        Exception.__init__(self)

class ConflictException(Exception):
    def __init__(self):
        Exception.__init__(self)

class NotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self)

class NotAuthenticatedException(Exception):
    def __init__(self):
        Exception.__init__(self)

class NotImplementedException(Exception):
    def __init__(self):
        Exception.__init__(self)

class HttpConflictException(Exception):
    def __init__(self):
        Exception.__init__(self)
