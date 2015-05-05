from pyramid.events import BeforeRender, subscriber
import venusian

from . import form  # api

assert form  # stfu pyflakes


class widget(object):
    """
    A function decorator which registers a Tiki Bar widget.

    Accepts one optional argument, ``name``, which defaults to the name of the
    decorated function.

    See :meth:`tikibar.config.add_tikibar_widget`.
    """
    def __init__(self, name=None):
        self.name = name

    def __call__(self, wrapped):
        name = self.name
        if not name:
            name = wrapped.__name__

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_tikibar_widget(wrapped, name)

        info = venusian.attach(wrapped, callback, category='tikibar')
        return wrapped


class content_type(object):
    """
    A class decorator which registers a Tiki Bar content type.

    Arguments

    name

      The name of the content type.  Defaults to the name of the decorated
      class.

    form_fields

      Form fields to be used for adding and editing instances of this type.

    See :meth:`tikibar.config.add_tikibar_content_type`.
    """
    def __init__(self, name=None, form_fields=None):
        self.name = name
        self.form_fields = form_fields

    def __call__(self, wrapped):
        name = self.name
        if not name:
            name = wrapped.__name__

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_tikibar_content_type(
                wrapped,
                name,
                form_fields=self.form_fields)

        info = venusian.attach(wrapped, callback, category='tikibar')
        return wrapped


def tikibar_content_type(request):
    cls = type(request.context)
    for ct in request.registry['tikibar']['content_types'].values():
        if ct['factory'] is cls:
            return ct


@subscriber(BeforeRender)
def add_tikibar_renderer_globals(event):
    request = event['request']
    if request:
        event['tikibar_url'] = request.resource_url(
            request.context, '@@tikibar')
        event['tikibar_js_url'] = request.static_url('static/js/tikibar_launch.js')


def includeme(config):
    config.add_static_view('tikibar-static', 'tikibar:static')
    config.add_request_method(tikibar_content_type, reify=True)
    config.add_renderer('html', '.views.html_renderer_factory')
    config.include('.config')
    config.scan()
