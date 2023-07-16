from core.bases.exception import Error


class AuthorizationError(Error):
    """ Class for authorization error. """

    def __init__(self, messages):
        Error.__init__(self)
        self.messages = messages


class HandlerError(Error):
    """ Class for handler error. """

    def __init__(self, messages):
        Error.__init__(self)
        self.messages = messages


class DatabaseError(Error):
    """ Class for database error. """

    def __init__(self, messages):
        Error.__init__(self)
        self.messages = messages


class NotFoundError(Error):
    """ Class for 404 error. """

    def __init__(self, messages):
        Error.__init__(self)
        self.messages = messages
