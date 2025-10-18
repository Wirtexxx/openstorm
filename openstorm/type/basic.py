from enum import Enum


class MongodbCommands(str, Enum):
    START = "start"
    STOP = "stop"
    STATUS = "status"
