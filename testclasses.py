class ToWrap(object):

    def __init__(self, num):
        self.num = num

    def do_stuff(self, word):
        return word + " stuff done: " + str(self.num)
