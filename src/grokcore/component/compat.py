import sys
import types
import martian
from zope.interface import classImplements
from zope.interface.interfaces import IInterface


if hasattr(types, 'ClassType'):
    class_types = (type, types.ClassType)
else:
    class_types = (type,)


if sys.version_info[0] < 3:
    from zope.interface import implements
else:

    class implements(martian.Directive):
        scope = martian.CLASS
        store = martian.ONCE
        default = None
        
        def factory(self, *interfaces):
            for interface in interfaces:
                if not IInterface.providedBy(interface):
                    raise Exception('%s is not a interface' % repr(interface))
            return interfaces


    class ClassImplementerGrokker(martian.ClassGrokker):
        martian.component(object)
        martian.directive(implements)
        martian.priority(2000)

        def execute(self, class_, implements, **kw):
            if implements is None:
                return True
            classImplements(class_, implements)
            return True
