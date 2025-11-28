class StudentSystemError(Exception):
    """Base exception for student system."""
class InvalidSelectionError(StudentSystemError):
    pass
class DuplicateIDError(StudentSystemError):
    pass
class EnrollmentError(StudentSystemError):
    pass
class CourseNotFoundError(StudentSystemError):
    pass
class TeacherNotFoundError(StudentSystemError):
    pass
class TimeSlotUnavailableError(StudentSystemError):
    pass
class PaymentError(StudentSystemError):
    pass
class AuthenticationError(StudentSystemError):
    pass
class InsufficientFundsError(StudentSystemError):
    pass
class LibraryError(StudentSystemError):
    pass
class HousingError(StudentSystemError):
    pass