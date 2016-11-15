class AlreadyInstalledError(Exception):
    msg = 'The plugin is already installed, use the -u option to update.'


class PluginDoesNotExistError(Exception):
    msg = "The specified plugin doesn't exist."
