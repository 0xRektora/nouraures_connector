"""
    Class containing utility classses and functions
"""



class Singleton():
    """
        Class that'll apply the Singleton design pattern to the passed
    """
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]
