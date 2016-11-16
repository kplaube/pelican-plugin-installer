class BaseException(Exception):
    pass


class AlreadyInstalledError(BaseException):
    msg = 'The plugin is already installed, use the -u option to update.'


class PluginDoesNotExistError(BaseException):
    msg = "The specified plugin doesn't exist."
