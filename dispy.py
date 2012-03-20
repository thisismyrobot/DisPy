import inspect
import xmlrpclib

from SimpleXMLRPCServer import SimpleXMLRPCServer


PORT = 8000


class Server(object):

    def __init__(self):
        self.server = SimpleXMLRPCServer(('0.0.0.0', PORT))
        self.server.register_function(self._init, 'init')
        self.server.register_function(self._call, 'call')
        self.server.register_function(self._get, 'get')
        self.server.register_function(self._set, 'set')
        self.cls = {}

    def start(self):
        self.server.serve_forever()

    def stop(self):
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


class WrapperTool(object):

    def __init__(self, server_ip):
        address = 'http://' + server_ip + ':' + str(PORT)
        self.proxy = xmlrpclib.ServerProxy(address)
        self.id = None

    def init_cls(self, cls, *args):
        cls_src = inspect.getsource(cls)
        instance_id = self.proxy.init(cls_src, *args)

        for member in inspect.getmembers(cls):
            if inspect.isfunction(member[1]):
                setattr(cls, member[0],
                        lambda x, *y: self.proxy.call(instance_id,
                                                      member[0], *y))

        setattr(cls, '__init__', lambda x: None)
        setattr(cls, '__getattr__',
                lambda x, y: self.proxy.get(instance_id, y))
        setattr(cls, '__setattr__',
                lambda x, y, z: self.proxy.set(instance_id, y, z))

        return cls()
