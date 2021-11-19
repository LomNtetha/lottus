class InvalidSelectedOptionError(Exception):
    """

    """

    def __init__(self, expression, message):
        """

        :param expression:
        :param message:
        """

        self.expression = expression
        self.message = message


class SessionAlreadyFinishedError(Exception):
    """

    """
    def __init__(self, expression, message):
        """

        :param expression:
        :param message:
        """

        self.expression = expression
        self.message = message


class WindowNotFoundError(Exception):
    """

    """

    def __init__(self, expression, message):
        """

        :param expression:
        :param message:
        """

        self.expression = expression
        self.message = message


class ProcessorNotFoundError(Exception):
    """

    """

    def __init__(self, expression, message):
        """

        :param expression:
        :param message:
        """

        self.expression = expression
        self.message = message


class ProcessorInvalidReturnError(Exception):
    """

    """

    def __init__(self, expression, message):
        """

        :param expression:
        :param message:
        """

        self.expression = expression
        self.message = message
