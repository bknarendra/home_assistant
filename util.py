import platform


class Util():

    @staticmethod
    def is_system_mac():
        return platform.system() == 'Darwin'

    @staticmethod
    def is_system_linux():
        return platform.system() == 'Linux'
