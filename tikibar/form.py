
class tag(object):
    self_closing = False

    def __init__(self, name, **attrs):
        if name.endswith('/'):
            self.self_closing = True
            name = name[:-1]
        self.name = name
        self.attrs = attrs
        self.children = ()

    def __call__(self, *children):
        def mkchild(x):
            if isinstance(x, str):
                x = text(x)
            x.parent = self
            return x
        self.children = tuple(mkchild(x) for x in children)
        return self

    def _render(self):
        if self.self_closing and not self.children:
            yield '<%s/>' % self.name
            return

        if self.attrs:
            attrs = ' ' + ' '.join(
                ('%s="%s"' % (k.lstrip('_'), v) for k, v in self.attrs.items())
            )
        else:
            attrs = ''
        yield '<%s%s>' % (self.name, attrs)
        for child in self.children:
            yield from child._render()
        yield '</%s>' % self.name

    def __str__(self):
        return ''.join(self._render())

    __html__ = __str__  # chameleon

    def __repr__(self):
        if self.self_closing and not self.children:
            return 'tag(%s)' % repr(self.name + '/')

        if self.attrs:
            attrs = ', ' + ', '.join(
                ('%s=%s' % (k, repr(v)) for k, v in self.attrs.items())
            )
        else:
            attrs = ''
        children = ('(%s)' % ', '.join(map(repr, self.children))
                    if self.children else '')
        return 'tag(%s%s)%s' % (repr(self.name), attrs, children)


class text(str):

    def _render(self):
        yield self
