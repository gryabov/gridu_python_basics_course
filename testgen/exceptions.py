class TestgenBaseException(Exception):
    pass


class DataSchemaParsingError(TestgenBaseException):
    pass


class DataGenerationException(TestgenBaseException):
    pass


class ConfigNotFoundException(TestgenBaseException):
    pass

class OptionConstrainException(TestgenBaseException):
    pass

