class MetaSingleton(type):
    """Metaclass to create singleton classes.
    Include 'metaclass=MetaSingleton' keyword to use."""
    _instance = None
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
