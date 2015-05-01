
class tag(object):

    def __init__(self, name, **attrs):
        self.name = name
        self.attrs = attrs
        self.children = ()

    def __call__(self, *children):
        def totext(x):
            if isinstance(x, str):
                x = text(x)
            return x
        self.children = tuple(totext(x) for x in children)
        return self

    def _render(self):
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
        if self.attrs:
            attrs = ', ' + ', '.join(
                ('%s=%s' % (k, repr(v)) for k, v in self.attrs.items())
            )
        else:
            attrs = ''
        children = ', '.join(map(repr, self.children))
        return 'tag(%s%s)(%s)' % (repr(self.name), attrs, children)


class text(str):

    def _render(self):
        yield self
