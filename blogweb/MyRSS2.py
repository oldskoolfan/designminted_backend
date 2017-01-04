import PyRSS2Gen

class MyRSS2(PyRSS2Gen.RSS2):
    def publish_extensions(self, handler):
        PyRSS2Gen._element(handler, 'atom:link', None, {
            "href": "http://designminted.com/rss/",
            "rel": "self",
            "type": "application/rss+xml",
        })