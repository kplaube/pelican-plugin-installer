class BaseException(Exception):
    pass


class AlreadyInstalledError(BaseException):
    msg = 'The plugin is already installed, use the -u option to update.'


class NotInstalledError(BaseException):
    msg = "The specified plugin isn't installed. Use -i option to install it."


class PluginDoesNotExistError(BaseException):
    msg = "The specified plugin doesn't exist."
