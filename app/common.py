

# # Для удобтва получения из dict:
class DictObj:
    def __init__(self, data: dict):
        self.__dict__.update(data)
    
    def __repr__(self):
        return f"DictObj({self.__dict__})"


