__author__ = 'andrew'
from rest_framework import renderers

class ImageRenderer(renderers.BaseRenderer):
    render_style = 'binary'
    media_type = 'image/*'
    format = '.multipart'
    charset = None

    def render(self, data, media_type=None, renderer_context=None):
        return data