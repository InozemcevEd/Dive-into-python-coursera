class Value:
    def __init__(self):
        self.value = None

    @staticmethod
    def _prepare_value(value, obj):
        return value * (1 - obj.commission)

    def __get__(self, obj, obj_type):
        return self.value

    def __set__(self, obj, value):
        self.value = self._prepare_value(value, obj)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
