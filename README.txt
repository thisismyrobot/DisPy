dispy - distributed python
==========================

Totally general purpose distributed python computation.

    >>> class ToWrap:
    ...     def __init__(self, num, animal, **kwargs):
    ...         self.num = num
    ...         self.animal = animal
    ...         self.kwargs = kwargs
    ...     def do_stuff(self):
    ...         return "stuff done"

    >>> import dispy
    >>> d = dispy.DisPy()
    >>> wrapped = d.register(ToWrap, 1, 'duck', magickwarg='Jelly')
    >>> wrapped.num
    1

    >>> wrapped.animal
    'duck'

    >>> wrapped.kwargs
    {'magickwarg': 'Jelly'}
