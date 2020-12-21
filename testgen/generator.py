import json
import logging
import os
import uuid
from itertools import count
from random import randint

import base62

from testgen.data_schema_parser import DataSchemaParser
from testgen.exceptions import DataGenerationException


log = logging.getLogger("testgen.generator")


class DataGenerator:

    def generate(self, options):
        log.info(f'Start to generate with options={options}')
        strategies = DataSchemaParser().read_schema(options.data_schema_json)

        if options.files_count == 0:
            json_string = self.generate_file(strategies)
            print(json_string)
        else:
            filename_func = self.create_filename_func(options.file_name, options.file_prefix)
            if options.clear_path:
                self.cleanup(options.path_to_save_files, options.file_name)

            generated = {}
            for _ in range(1, options.files_count + 1):
                filename = filename_func()
                rows = []
                for _ in range(options.data_lines):
                    json_string = self.generate_file(strategies)
                    rows.append(json_string)
                    rows.append('\n')
                generated[filename]=rows
                log.info(f'Generated {filename}')
            self.store_files(options.path_to_save_files, generated)

    def generate_file(self, strategies):
        generated = {}
        for item_name, strategy in strategies.items():
            generated[item_name] = strategy.run()
        return json.dumps(generated)

    def store_files(self, path_to_save_files, generated_files):
        for filename, content_rows in generated_files.items():
            full_path = os.path.join(path_to_save_files, filename)
            with open(full_path, 'w') as file:
                file.writelines(content_rows)
        log.info('All files are stored. File generation is done.')

    def cleanup(self, path, file_name):
        for file in os.listdir(path):
            if file.startswith(file_name):
                os.remove(os.path.join(path, file))
                log.info(f'Cleanup: {file} is removed')

    def create_filename_func(self, file_name, file_prefix):
        counter = count(1)

        def with_postfix(postfix):
            return file_name + '_' + postfix

        def count_func():
            return with_postfix(str(next(counter)))

        def random_func():
            return with_postfix(base62.encode(randint(1, 1000000000)))

        def uuid_func():
            return with_postfix(str(uuid.uuid4()))

        if file_prefix == 'count':
            return count_func
        if file_prefix == 'random':
            return random_func
        if file_prefix == 'uuid':
            return uuid_func
        else:
            raise DataGenerationException("file_prefix has wrong value")
