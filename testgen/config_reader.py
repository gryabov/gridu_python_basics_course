import logging.config
import os

from configparser import ConfigParser

from testgen.exceptions import ConfigNotFoundException


class Defaults:
    def __init__(self):
        parser = ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testgen.ini')
        status = parser.read(config_path)
        self._check_config_status(status, config_path)
        self.config = parser['DEFAULT']

    @property
    def path_to_save_files(self):
        return self.config['path_to_save_files']

    @property
    def data_schema(self):
        return self.config['data_schema']

    @property
    def file_name(self):
        return self.config['file_name']

    @property
    def file_prefix(self):
        return self.config['file_prefix']

    @property
    def files_count(self):
        return self.config.getint('files_count')

    @property
    def data_lines(self):
        return self.config.getint('data_lines')

    @property
    def clear_path(self):
        return self.config.getboolean('clear_path')

    def _check_config_status(self, status, path):
        if len(status) == 0:
            raise ConfigNotFoundException(f'Cannot find config file in path={path}')
