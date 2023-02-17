"""

If the grok.order directive is specified with other classes that don't
have the order specified, then the order will be determined by first
sorting on the order specified, and then by the definition order.

  >>> components = [First(), Second(), Third(), Fourth(), Fifth()]

  >>> from grokcore.component import sort_components
  >>> sort_components(components)
  [<...Fifth object at ...>,
   <...Third object at ...>,
   <...First object at ...>,
   <...Fourth object at ...>,
   <...Second object at ...>]

"""

import grokcore.component as grok


class First:
    grok.order()


class Second:
    grok.order(1)


class Third:
    pass


class Fourth:
    grok.order()


class Fifth:
    pass
