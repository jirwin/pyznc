"""
Webadmin functionality
"""
import cookielib
import os

from lxml.html import parse
from urllib import urlencode
from urllib2 import (Request, urlopen, HTTPCookieProcessor, build_opener,
                     install_opener)


class WebAdmin:
    host = None
    port = None
    user = None
    passwd = None
    cookies = "cookiejar"
    cookiejar = cookielib.LWPCookieJar()

    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def _get_site(self):
        return "%s:%s" % (self.host, self.port)

    def _install_cookiejar(self):
        if os.path.isfile(self.cookies):
            self.cookiejar.load(self.cookies)
        install_opener(build_opener(HTTPCookieProcessor(self.cookiejar)))

    def login(self):
        self._install_cookiejar()
        data = {'submitted': '1',
                'user': self.user,
                'pass': self.passwd}
        conn = Request("%s/login" % self._get_site(), urlencode(data))
        print conn.get_full_url()
        for line in urlopen(conn):
            print line

    def get_csrf(self, path):
        page = urlopen(Request("%s/%s" % (self._get_site(), path)))
        doc = parse(page).getroot()
        csrf = doc.cssselect("input[name=_CSRF_Check]")
        if csrf:
            return csrf[0].value
