def singleton(func):
    """
    Decorator for making a singleton
    :param func: The function to be decorated
    :return: The decorated function
    """
    __instance = [None]
    def __call__(*args, **kwargs):
        if __instance[0] is None:
            __instance[0] = func.__init__(*args, **kwargs)
        return __instance[0]
    return __call__
