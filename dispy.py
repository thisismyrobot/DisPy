class DisPy:

    def __init__(self):
        pass

    def register(self, cls, *args, **kwargs):
        cls_instance = cls(*args, **kwargs)
        return cls_instance
