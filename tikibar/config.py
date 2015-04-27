

def add_tikibar_widget(config, widget, name=None):
    """
    Add a widget to the tikibar.

    Arguments (all required)

    widget

      A widget callable or a dotted Python name which refers to a widget
      callable.  The callable must take two positional arguments: `context` and
      `request` and should return an HTML string for embedding in the Tiki Bar.

    name

      The name for this widget.  Naming widgets allows them to be overridden by
      other packages.  If ommitted, the name of the callable is used.
    """
    widget = config.maybe_dotted(widget)
    if not name:
        name = widget.__name__
    discriminator = ('tikibar.widget', name)
    introspectable = config.introspectable(
        'tikibar widgets',
        discriminator,
        config.object_description(widget),
        'tikibar widget')
    introspectable['name'] = name

    def register():
        registry = config.registry
        widgets = registry.get('tikibar_widgets')
        if not widgets:
            registry['tikibar_widgets'] = widgets = {}
        widgets[name] = widget

    config.action(
        ('tikibar.widget', widget, name),
        register,
        introspectables=(introspectable,)
    )


def includeme(config):
    config.add_directive('add_tikibar_widget', add_tikibar_widget)
