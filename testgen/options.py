from __future__ import with_statement

import json
import os

from testgen.exceptions import OptionConstrainException


class Options:
    def __init__(self, args, defaults):
        self.args = args
        self.defaults = defaults
        self.__file_prefix_option_list = ['count', 'random', 'uuid']
        self.__path_to_save_files = self.init_path_to_save_files()
        self.__data_schema = self.init_data_schema()
        self.__file_name = self.init_file_name()
        self.__file_prefix = self.init_file_prefix()
        self.__files_count = self.init_files_count()
        self.__data_lines = self.init_data_lines()
        self.__clear_path = self.init_clear_path()

    def _default_if_none(self, value_name, value, default):
        value = default if value is None else value
        if value is None:
            raise OptionConstrainException(f"Cannot construct {value_name} option. "
                                           f"Check config or set the value explicitly.")
        return value

    @property
    def path_to_save_files(self):
        return self.__path_to_save_files

    def init_path_to_save_files(self):
        arg_raw_value = self.args.path_to_save_files[0] if len(self.args.path_to_save_files) > 0 else None
        path_to_save_files = self._default_if_none("path_to_save_files", arg_raw_value,
                                                   self.defaults.path_to_save_files)
        abs_path = os.path.abspath(path_to_save_files)
        if not os.path.exists(abs_path):
            raise OptionConstrainException(f"Path '{abs_path}' to file does not exists")
        if not os.path.isdir(abs_path):
            raise OptionConstrainException(f"Path '{abs_path}' is not directory")
        return abs_path

    @property
    def data_schema_json(self):
        return self.__data_schema

    def init_data_schema(self):
        data_schema = self._default_if_none("data_schema", self.args.data_schema, self.defaults.data_schema)

        if str(data_schema).strip().startswith("{"):
            try:
                json_content = json.loads(data_schema)
                return json_content
            except ValueError as e:
                raise OptionConstrainException(f"data_schema param is not valid json")

        abs_path = os.path.abspath(data_schema)
        if not os.path.exists(abs_path):
            raise OptionConstrainException(f"Path '{abs_path}' to file does not exists")
        if os.path.isdir(abs_path):
            raise OptionConstrainException(f"Path '{abs_path}' is directory")

        try:
            with open(abs_path) as f:
                json_content = json.load(f)
                return json_content
        except:
            raise OptionConstrainException("data_schema is not valid json")

    @property
    def file_name(self):
        return self.__file_name

    def init_file_name(self):
        return self._default_if_none("file_name", self.args.file_name, self.defaults.file_name)

    @property
    def file_prefix(self):
        return self.__file_prefix

    def init_file_prefix(self):
        file_prefix = self._default_if_none("file_prefix", self.args.file_prefix, self.defaults.file_prefix)
        if file_prefix not in self.__file_prefix_option_list:
            raise OptionConstrainException(f"file_prefix option should be one of {self.__file_prefix_option_list}")
        return file_prefix

    @property
    def files_count(self):
        return self.__files_count

    def init_files_count(self):
        files_count = self._default_if_none("files_count", self.args.files_count, self.defaults.files_count)
        if files_count < 0:
            raise OptionConstrainException("files_count option should be more or equal to 0")
        return files_count

    @property
    def data_lines(self):
        return self.__data_lines

    def init_data_lines(self):
        data_lines = self._default_if_none("data_lines", self.args.data_lines, self.defaults.data_lines)
        if data_lines <= 0:
            raise OptionConstrainException("data_lines option should be more than 0")
        return data_lines

    @property
    def clear_path(self):
        return self.__clear_path

    def init_clear_path(self):
        return self._default_if_none("clear_path", self.args.clear_path, self.defaults.clear_path)

    def __str__(self):
        return f'[ path_to_save_files={self.__path_to_save_files}, data_schema={self.__data_schema}, ' \
               f'file_name={self.__file_name}, file_prefix={self.__file_prefix}, files_count={self.__files_count}, '\
               f'data_lines={self.__data_lines}, clear_path={self.__clear_path} ]'
