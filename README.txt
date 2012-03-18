DisPy - distributed python
==========================

General-purpose distributed Python processing


Introduction
------------

XML-RPC already allows for the calling of methods & access to members
over HTTP, via XML. DisPy takes this concept a little further, allowing
for class definitions to be pushed from client to server(s) at run-time
(again, via XML- RPC), instances to be created on the server and for
member & method access over the same XML-RPC connection.

It is very very very alpha, I only guarantee what's tested below :)


Requirements
------------

It currently works on Python 3.2.2 on Ubuntu.


Server
------

First, we need a server

    >>> import dispy
    >>> s = dispy.Server()

And we start it, via threading, in the doctest

    >>> import threading
    >>> ts = threading.Thread(target=s.start)
    >>> ts.start()


Wrapping
--------

We can wrap a class during the initialisation of it

    >>> import testclasses
    >>> d = dispy.DisPy()
    >>> wrapped = d.register(testclasses.ToWrap, 7)

Then we can use it as normal

    >>> wrapped.do_stuff("yay")
    'yay stuff done: 7'

    >>> wrapped.num
    7

    >>> wrapped.num = 5
    >>> wrapped.num
    5

    >>> wrapped.do_stuff("yay")
    'yay stuff done: 5'

Instances
---------

The instances are all separate still, their instance data is stored remotely.

    >>> wrapped_again = d.register(testclasses.ToWrap, 7)
    >>> wrapped_again.do_stuff("boo")
    'boo stuff done: 7'


Server finish
-------------

And we need to stop the server

    >>> s.stop()



