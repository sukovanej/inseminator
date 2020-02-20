class InseminatorError(Exception):
    pass


class ContainerError(InseminatorError):
    pass


class ContainerRegisterError(ContainerError):
    pass


class ResolverError(InseminatorError):
    pass
