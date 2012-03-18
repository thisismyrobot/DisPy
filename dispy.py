import inspect
import pickle
import xmlrpc.client
import xmlrpc.server

class Server(object):

    def __init__(self):
        self.server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000))
        self.server.register_function(self._register, 'register')
        self.server.register_function(self._call, 'call')
        self.server.register_function(self._get, 'get')
        self.server.register_function(self._set, 'set')
        self.cls = {}

    def start(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()

    def _register(self, cls_src, *args):
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
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8000')
        self.id = None

    def register(self, cls, *args):
        # get the source code of the class
        src = inspect.getsource(cls)

        # copy the rouce code to the server, instanciate with args
        instance_id = self.proxy.register(src, *args)

        for member in inspect.getmembers(cls):
            if inspect.isfunction(member[1]):
                if member[0] == '__init__':
                    setattr(cls, member[0], lambda x: None)
                else:
                    setattr(cls, member[0], lambda x, *y: self.proxy.call(instance_id, member[0], *y))

        setattr(cls, '__getattr__', lambda x, y: self.proxy.get(instance_id, y))
        setattr(cls, '__setattr__', lambda x, y, z: self.proxy.set(instance_id, y, z))

        return cls()
