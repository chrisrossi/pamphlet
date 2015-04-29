
def add_tikibar_content_type(config, content_type, name=None, add_view=None):
    """
    Add a content type.

    Arguments

    cls

      A class or dotted Python name which refers to a class for a content type.

    name

      The name for the content type.  If omitted, the name of the class is
      used.

    add_view

      The name of a view that can be used to add more instances of this type.
      If omitted, this type is not addable from Tiki Bar.

    """
    content_type = config.maybe_dotted(content_type)
    if not name:
        name = content_type.__name__
    discriminator = ('tikibar.content_type', name)
    introspectable = config.introspectable(
        'tikibar content types',
        discriminator,
        config.object_description(content_type),
        'tikibar content type')
    introspectable['name'] = name
    introspectable['add_view'] = add_view

    def register():
        types = config.registry['tikibar']['content_types']
        types.setdefault(name, {}).update({
            'factory': content_type,
            'add_view': add_view,
            'name': name})

    config.action(
        ('tikibar.content_type', content_type, name),
        register,
        introspectables=(introspectable,)
    )


def add_tikibar_widget(config, widget, name=None):
    """
    Add a widget to the tikibar.

    Arguments

    widget

      A widget callable or a dotted Python name which refers to a widget
      callable.  The callable must take two positional arguments: `context` and
      `request` and should return an HTML string for embedding in the Tiki Bar.

    name

      The name for this widget.  Naming widgets allows them to be overridden by
      other packages.  If omitted, the name of the callable is used.
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
        config.registry['tikibar']['widgets'][name] = widget

    config.action(
        ('tikibar.widget', widget, name),
        register,
        introspectables=(introspectable,)
    )


def includeme(config):
    config.registry['tikibar'] = {
        'widgets': {},
        'content_types': {},
    }
    config.add_directive('add_tikibar_content_type', add_tikibar_content_type)
    config.add_directive('add_tikibar_widget', add_tikibar_widget)
