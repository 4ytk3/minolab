class ProcessingRegistry:
    _processing = {}

    @classmethod
    def register(cls, category):
        def wrapper(processing_cls):
            if category in cls._processing:
                raise ValueError(f"Category '{category}' is already registered with {cls._processing[category]}.")
            cls._processing[category] = processing_cls
            return processing_cls
        return wrapper

    @classmethod
    def get_processing(cls, category):
        processing_cls = cls._processing.get(category)
        if not processing_cls:
            raise ValueError(f"Filter '{category}' is not registered.")
        return processing_cls()
