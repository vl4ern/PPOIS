from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Role(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"