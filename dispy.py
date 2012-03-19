import avahi
import dbus
import inspect
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer


ZC_NAME = 'DisPyNode'


class ZeroconfService:
    """ Avahi zeroconf for server discovery
    """

    def __init__(self, name, port, stype="_http._tcp", domain="", host="",
                 text=""):
        self.name = name
        self.port = port
        self.stype = stype
        self.domain = domain
        self.host = host
        self.text = text

    def publish(self):
        bus = dbus.SystemBus()
        server = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
                                               avahi.DBUS_PATH_SERVER),
                                avahi.DBUS_INTERFACE_SERVER)

        g = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
                                          server.EntryGroupNew()),
                           avahi.DBUS_INTERFACE_ENTRY_GROUP)

        g.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC, dbus.UInt32(0),
                     self.name, self.stype, self.domain, self.host,
                     dbus.UInt16(self.port), self.text)

        g.Commit()
        self.group = g

    def unpublish(self):
        self.group.Reset()


class Server(object):

    def __init__(self, port=8000):
        self.port = port
        self.server = SimpleXMLRPCServer(("localhost", port))
        self.server.register_function(self._init, 'init')
        self.server.register_function(self._call, 'call')
        self.server.register_function(self._get, 'get')
        self.server.register_function(self._set, 'set')
        self.cls = {}

    def start(self):
        self.service = ZeroconfService(name=ZC_NAME, port=self.port)
        self.service.publish()
        self.server.serve_forever()

    def stop(self):
        self.service.unpublish()
        self.server.shutdown()

    def _init(self, cls_src, *args):
        """ Register some code - only to be called via xml-rpc, returns a
            class id.
        """
        classes = dir()
        exec(cls_src)
        newclass = [c for c in dir() if c not in classes][0]
        next_id = len(self.cls)
        self.cls[next_id] = eval(newclass)(*args)
        return next_id

    def _call(self, cls_id, method, *args):
        """ Call a method, only to be called via xml-rpc
        """
        return getattr(self.cls[cls_id], method)(*args)

    def _get(self, cls_id, attr):
        """ Return the value of an attribute.
        """
        return getattr(self.cls[cls_id], attr)

    def _set(self, cls_id, attr, val):
        """ Return the value of an attribute.
        """
        setattr(self.cls[cls_id], attr, val)
        return 0


class DisPy(object):

    def __init__(self):
        
        self.proxy = xmlrpclib.ServerProxy('http://localhost:8000')
        self.id = None

    def init(self, cls, *args):
        # get the source code of the class
        src = inspect.getsource(cls)

        # copy the source code to the server, instantiate with args
        instance_id = self.proxy.init(src, *args)

        for member in inspect.getmembers(cls):
            if inspect.isfunction(member[1]):
                setattr(cls, member[0], lambda x, *y: self.proxy.call(instance_id, member[0], *y))

        setattr(cls, '__init__', lambda x: None)
        setattr(cls, '__getattr__', lambda x, y: self.proxy.get(instance_id, y))
        setattr(cls, '__setattr__', lambda x, y, z: self.proxy.set(instance_id, y, z))

        return cls()
