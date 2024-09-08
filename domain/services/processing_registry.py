class SpatialProcessingRegistry:
    _spatial_processing = {}

    @classmethod
    def register(cls, category):
        def wrapper(processing_cls):
            if category in cls._spatial_processing:
                raise ValueError(f"Category '{category}' is already registered with {cls._spatial_processing[category]}.")
            cls._spatial_processing[category] = processing_cls
            return processing_cls
        return wrapper

    @classmethod
    def get_processing(cls, category):
        processing_cls = cls._spatial_processing.get(category)
        if not processing_cls:
            raise ValueError(f"Filter '{category}' is not registered.")
        return processing_cls()

class FrequencyProcessingRegistry:
    _frequency_processing = {}

    @classmethod
    def register(cls, category):
        def wrapper(processing_cls):
            if category in cls._frequency_processing:
                raise ValueError(f"Category '{category}' is already registered with {cls._frequency_processing[category]}.")
            cls._frequency_processing[category] = processing_cls
            return processing_cls
        return wrapper

    @classmethod
    def get_processing(cls, category):
        processing_cls = cls._frequency_processing.get(category)
        if not processing_cls:
            raise ValueError(f"Filter '{category}' is not registered.")
        return processing_cls()
