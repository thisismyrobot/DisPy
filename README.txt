dispy - distributed python
==========================

Totally general purpose distributed python computation.

Introduction
------------

Firstly, you run up one or more "server" instances. Then, general Python code
can then be wrapped by some "magic sauce" that copies the code to
a server (via xml-rpc), replacing the method calls with stubs that call the
methods on the servers transparently.

Ref
---

http://docs.python.org/release/3.1.3/library/xmlrpc.server.html#simplexmlrpcserver-example

Server
------

First, we need a server

    >>> import dispy
    >>> s = dispy.Server()

And we start it via threading in the doctest

    >>> import threading
    >>> ts = threading.Thread(target=s.start)
    >>> ts.start()

Wrapping
--------

    >>> import testclasses
    >>> d = dispy.DisPy()
    >>> wrapped = d.register(testclasses.ToWrap, 7)

    >>> wrapped.do_stuff("yay")
    'yay stuff done: 7'

    >>> wrapped.num
    7

    >>> wrapped.num = 5
    >>> wrapped.num
    5

Server finish
-------------

And we need to stop the server

    >>> s.stop()
