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

Tested on Python 2.7 on Ubuntu 11.10.


Limitations
-----------

 * No static members


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

We can wrap a class during the initialisation of it.

    >>> import testclasses
    >>> d = dispy.WrapperTool('127.0.0.1')
    >>> wrapped = d.init_cls(testclasses.ToWrap, 7)

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

The instances are separate still, their instance data is stored
remotely.

    >>> wrapped_again = d.init_cls(testclasses.ToWrap, 7)
    >>> wrapped_again.do_stuff("boo")
    'boo stuff done: 7'

    >>> s.cls
    {0: <dispy.ToWrap object at 0x...>, 1: <dispy.ToWrap object at 0x...>}

    >>> s.cls[0].num
    5

    >>> s.cls[1].num
    7


Static members
--------------

This is how changing static members would normally work

    >>> class Static(object):
    ...     num = 12

    >>> st = Static()
    >>> st.num
    12

    >>> Static.num = 5
    >>> st.num
    5

This doesn't happen correctly with DisPy - changes to static members
aren't copied out to the servers, but they are reflected locally. Long
story short: don't use them.

    >>> testclasses.Static.num
    13

    >>> stat = d.init_cls(testclasses.Static)
    >>> stat.num
    13

    >>> testclasses.Static.num = 7
    >>> stat.num
    7

    >>> s.cls[2].num
    13


Decorators
----------

Decorators work fine

    >>> dec = d.init_cls(testclasses.Decorated)
    >>> dec.a_num
    42

    >>> dec.val = 14
    >>> dec.val
    14

    >>> dec.a_num
    14

    >>> s.cls[3].a_num
    14


Server finish
-------------

And we need to stop the server

    >>> s.stop()



