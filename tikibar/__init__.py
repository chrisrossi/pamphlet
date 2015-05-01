from pyramid.events import BeforeRender, subscriber
import venusian


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

    add_view

      The name of a view that can be used to add more instances of this type.
      If omitted, this type is not addable from Tiki Bar.

    See :meth:`tikibar.config.add_tikibar_content_type`.
    """
    def __init__(self, name=None, add_view=None):
        self.name = name
        self.add_view = add_view

    def __call__(self, wrapped):
        name = self.name
        if not name:
            name = wrapped.__name__

        def callback(context, name, ob):
            config = context.config.with_package(info.module)
            config.add_tikibar_content_type(
                wrapped,
                name,
                add_view=self.add_view)

        info = venusian.attach(wrapped, callback, category='tikibar')
        return wrapped


@subscriber(BeforeRender)
def add_tikibar_renderer_globals(event):
    request = event['request']
    event['tikibar_url'] = request.resource_url(
        request.context, '@@tikibar')
    event['tikibar_js_url'] = request.static_url('static/js/tikibar_launch.js')


def includeme(config):
    config.add_static_view('tikibar-static', 'tikibar:static')
    config.include('.config')
    config.scan()
