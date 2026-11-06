def singleton(cls):
    """
    Decorator for making a singleton
    :param cls: The class to be decorated
    :return: The decorated class instance
    """
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
