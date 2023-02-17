"""

If the grok.order directive is absent, sorting will be done by class
name.

  >>> components = [First(), Second(), Third(), Fourth(), Fifth()]

  >>> from grokcore.component import sort_components
  >>> sort_components(components)
  [<...Fifth object at ...>,
   <...First object at ...>,
   <...Fourth object at ...>,
   <...Second object at ...>,
   <...Third object at ...>]

"""


class First:
    pass


class Second:
    pass


class Third:
    pass


class Fourth:
    pass


class Fifth:
    pass
