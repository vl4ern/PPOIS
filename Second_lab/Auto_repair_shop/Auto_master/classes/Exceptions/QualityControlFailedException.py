from classes.Exceptions.AutomasterException import AutomasterException

class QualityControlFailedException(AutomasterException):
    """Контроль качества не пройден"""
    pass