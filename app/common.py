



# Для удобтва получения из dict:
class DictObj:
    def __init__(self, d):
        for key, value in d.items():
            setattr(self, key, value)