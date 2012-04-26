"""
Webadmin functionality
"""
import cookielib
import os

from lxml.html import parse
from urllib import urlencode
from urllib2 import (Request, urlopen, HTTPCookieProcessor, build_opener,
                     install_opener)

from .config import conf_map


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
        req = Request("%s/login" % self._get_site(), urlencode(data))
        urlopen(req)

    def get_csrf(self, path):
        page = urlopen(Request("%s/%s" % (self._get_site(), path)))
        doc = parse(page).getroot()
        csrf = doc.cssselect("input[name=_CSRF_Check]")
        if csrf:
            return csrf[0].value

    @staticmethod
    def generate_config(znc_conf, user=''):
        webadmin_conf = []

        for znc, wa in znc_conf.iteritems():
            if znc == 'Servers':
                webadmin_conf.append((conf_map.get(znc),
                                     "\n". join(server for server in wa)))
                continue
            elif znc == 'LoadModule':
                webadmin_conf.extend((conf_map.get(znc), mod) for mod in wa)
                continue

            key = conf_map.get(znc)
            val = {True: 1,
                   False: None}.get(wa, str(wa).replace('<%user%>', user))
            if key and val:
                webadmin_conf.append((key, val))

        return webadmin_conf

    def add_user(self, user, passwd=12345, conf=None):
        path = "mods/global/webadmin/adduser"

        data = [("_CSRF_Check", self.get_csrf(path)),
                ("submitted", 1),
                ("newuser", user),
                ("password", passwd),
                ("password2", passwd)]
        if conf:
            data.extend(WebAdmin.generate_config(conf, user=user))

        req = Request("%s/%s" % (self._get_site(), path), urlencode(data))
        urlopen(req)
        print "%s created." % user
