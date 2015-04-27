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


def includeme(config):
    config.add_tween('tikibar.tween.tikibar_tween_factory')
    config.add_static_view('tikibar-static', 'tikibar:static')
    config.include('.config')
    config.scan()
