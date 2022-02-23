import json

class NotFoundResponse():

    def __init__(self, message):
        self.msg = message

    def toJson(self):
        return self.__dict__