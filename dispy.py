import inspect
import xmlrpclib

from SimpleXMLRPCServer import SimpleXMLRPCServer


PORT = 8000


class Server(object):
    """ A general purpose XML-RPC-exposing server.
    """

    def __init__(self, listen_ip='0.0.0.0'):
        """ Prepare the XML-RPC server, map the exposed functions.
        """
        self.server = SimpleXMLRPCServer((listen_ip, PORT))
        self.server.register_function(self._init, 'init')
        self.server.register_function(self._call, 'call')
        self.server.register_function(self._get, 'get')
        self.server.register_function(self._set, 'set')
        self.cls = {}

    def start(self):
        """ Start the server.
        """
        self.server.serve_forever()

    def stop(self):
        """ Stop the server.
        """
        self.server.shutdown()

    def _init(self, cls_src, *args):
        """ Register and initialise a class, class id. Only to be called via
            XML-RPC.
        """
        classes = dir()
        exec(cls_src)
        newclass = [c for c in dir() if c not in classes][0]
        next_id = len(self.cls)
        self.cls[next_id] = eval(newclass)(*args)
        return next_id

    def _call(self, cls_id, method, *args):
        """ Call a method. Only to be called via XML-RPC.
        """
        return getattr(self.cls[cls_id], method)(*args)

    def _get(self, cls_id, attr):
        """ Return the value of an attribute. Only to be called via XML-RPC.
        """
        return getattr(self.cls[cls_id], attr)

    def _set(self, cls_id, attr, val):
        """ Set the value of an attribute. Only to be called via XML-RPC.
        """
        setattr(self.cls[cls_id], attr, val)
        return 0


class WrapperTool(object):
    """ A toolkit to wrap class instances to allow them to be accessed
        transparently over XML-RPC.
    """

    def __init__(self, server_ip='127.0.0.1'):
        """ Create the XML-RPC proxy connection to the server.
        """
        address = 'http://' + server_ip + ':' + str(PORT)
        self.proxy = xmlrpclib.ServerProxy(address)

    def _get_src(self, cls):
        """ Return the source code of a class
        """
        return inspect.getsource(cls)

    def _map_methods(self, cls, instance_id):
        """ Map the methods to XML-RPC calls.
        """
        for name, member in inspect.getmembers(cls):
            if inspect.isfunction(member):
                setattr(cls, name,
                        lambda x, *y: self.proxy.call(instance_id,
                                                      name, *y))

    def _map_members(self, cls, instance_id):
        """ Map the members to XML-RPC calls via the magic methods.
        """
        setattr(cls, '__init__', lambda x: None)
        setattr(cls, '__getattr__',
                lambda x, y: self.proxy.get(instance_id, y))
        setattr(cls, '__setattr__',
                lambda x, y, z: self.proxy.set(instance_id, y, z))

    def init_cls(self, cls, *args):
        """ Wrap a class, returning a stubb'd instance.
        """
        cls_src = self._get_src(cls)
        instance_id = self.proxy.init(cls_src, *args)
        self._map_methods(cls, instance_id)
        self._map_members(cls, instance_id)
        return cls()
