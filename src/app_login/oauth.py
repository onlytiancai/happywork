# -*- coding: utf-8 -*-

import urllib
import urllib2
import logging


class OAuth(object):
    __headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/json",
        "User-Agent": "onlytiancai oauth/0.0.1 (onlytiancai@gmail.com)"}

    def __init__(self, name, client_id, client_secret, base_url, access_token_url, authorize_url):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.access_token_url = access_token_url
        self.authorize_url = authorize_url

    def _request(self, method, uri, data):
        try:
            if method == 'GET':
                uri = uri + '?' + urllib.urlencode(data)
                response = urllib2.urlopen(uri)
            else:
                request = urllib2.Request(uri, urllib.urlencode(data), headers=self.__headers)
                response = urllib2.urlopen(request)
            response = response.read()
            logging.debug('_request:%s [%s]', uri, response)
            return response
        except urllib2.URLError, ue:
            logging.debug('_request:%s [%s]', uri, ue.read())
            raise

    def get_authorize_url(self, **kargs):
        data = dict(client_id=self.client_id)
        data.update(kargs)
        return self.authorize_url + '?' + urllib.urlencode(data)

    def get_access_token(self, method, **kargs):
        data = dict(client_id=self.client_id, client_secret=self.client_secret)
        data.update(kargs)
        return self._request(method=method, uri=self.access_token_url, data=data)

    def request(self, method, uri, **kargs):
        if not uri.startswith('http://'):
            uri = self.base_url + uri
        return self._request(method=method, uri=uri, data=kargs)
