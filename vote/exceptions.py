class DailyValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ValidationVoteException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ValidationReVoteTimeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ValidationTimeCreateVoteException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ValidationUserRatingException(Exception):
    def __init__(self, message):
        super().__init__(message)