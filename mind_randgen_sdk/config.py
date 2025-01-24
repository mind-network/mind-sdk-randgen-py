class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def setup(self, configs):
        for key, value in configs.items():
            setattr(self, key, value)


config = Config()
