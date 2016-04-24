# -*- coding: utf-8 -*-

import HTMLParser

class HParser(HTMLParser.HTMLParser):
    xs = []
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.xs.append(value)