import grokcore.component as grok


class Cave(grok.Context):
    pass


class Club(grok.Context):
    pass


grok.context(Cave)
grok.context(Club)
