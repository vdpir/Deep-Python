
class Value:
    def __init__(self):
        self.value_ = None

    def __get__(self, obj, obj_type):
        return self.value_

    def __set__(self, obj, value):
        self.value_ = value * (1. - obj.commission)

class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
