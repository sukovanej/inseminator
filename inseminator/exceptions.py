class InseminatorError(Exception):
    """The base inseminator exception."""

    pass


class ContainerError(InseminatorError):
    """Base exception for errors from the Container class."""

    pass


class ContainerRegisterError(ContainerError):
    """Error when calling `register` method on the Container."""

    pass


class ResolverError(InseminatorError):
    """Error from the Resolver."""

    pass
