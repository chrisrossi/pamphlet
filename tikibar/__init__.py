def includeme(config):
    config.add_tween('tikibar.tween.tikibar_tween_factory')
    config.add_static_view('tikibar-static', 'tikibar:static')
    config.scan()
