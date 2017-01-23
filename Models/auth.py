#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class AdminUser():
    def __init__(self, id=None, user_name=None, php_token=None, scope=[], exp=None, authorities=[], jti=None, client_id=None):
        self.id = id
        self.user_name = user_name
        self.scope = scope
        self.exp = exp
        self.authorities = authorities
        self.jti = jti
        self.client_id = client_id

    def __repr__(self):
        return '<AdminUser id=%s, user_name=%s >' % (self.id, self.user_name)

    @classmethod
    def new_from_token(cls, token):
        o = cls()
        o.id = token['id'] if 'id' in token else None
        o.user_name = token['user_name'] if 'user_name' in token else None
        o.scope = token['scope'] if 'scope' in token else None
        o.exp = token['exp'] if 'exp' in token else None
        o.authorities = token['authorities'] if 'authorities' in token else None
        o.jti = token['jti'] if 'jti' in token else None
        o.client_id = token['client_id'] if 'client_id' in token else None
        return o

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, idd):
        self._id = idd

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        self._user_name = user_name

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, scope):
        self._scope = scope

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, exp):
        self._exp = exp

    @property
    def authorities(self):
        return self._authorities

    @authorities.setter
    def authorities(self, authorities):
        self._authorities = authorities

    @property
    def jti(self):
        return self._jti

    @jti.setter
    def jti(self, jti):
        self._jti = jti

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id


    @property
    def roles(self):
        return self.authorities
