class ToWrap(object):

    def __init__(self, num):
        self.num = num

    def do_stuff(self, word):
        return word + " stuff done: " + str(self.num)


class Static(object):
    num = 13


class Decorated(object):

    def __init__(self):
        self.val = 42

    @property
    def a_num(self):
        return self.val
