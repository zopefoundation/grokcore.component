"""

If the grok.order directive is present with no arguments, sorting will
be done by definition order.

  >>> components = [First(), Second(), Third(), Fourth(), Fifth()]

  >>> from grokcore.component import sort_components
  >>> sort_components(components)
  [<...First object at ...>,
   <...Second object at ...>,
   <...Third object at ...>,
   <...Fourth object at ...>,
   <...Fifth object at ...>]

"""

import grokcore.component as grok


class First:
    grok.order()


class Second:
    grok.order()


class Third:
    grok.order()


class Fourth:
    grok.order()


class Fifth:
    grok.order()
