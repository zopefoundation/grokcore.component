import grok

class Cave(grok.Context):
    pass

class Club(grok.Context):
    pass

class Anything(object):
    grok.context(Cave)
    grok.context(Club)
