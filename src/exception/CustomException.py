class HwpOpenError(Exception):
    def __init__(self, message="Can't open HWP file."):
        self.message = message
        super().__init__(self.message)


class HwpObjectNotFoundError(Exception):
    def __init__(self, message="Can't find HWP"):
        self.message = message
        super().__init__(self.message)


class NotFoundKeyWordError(Exception):
    def __init__(self, message="Can't find the keyword"):
        self.message = message
        super().__init__(self.message)


class NoneException(Exception):
    def __init__(self, message="Data is not found"):
        self.message = message
        super().__init__(self.message)
