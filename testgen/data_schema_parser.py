import ast
import logging
import random
import time
import uuid

from testgen.exceptions import DataSchemaParsingError

log = logging.getLogger("testgen.schema_parser")


class AbstractTypeParser:
    def assert_kv_len_eq2(self, kv):
        if len(kv) != 2 or not kv[1]:
            raise DataSchemaParsingError(f'{kv[0]} type name without type value')

    def _safe_eval(self, expression):
        try:
            return ast.literal_eval(expression)
        except:
            log.warning(f'_safe_eval: failed to parse expression={expression}')
            return None


class TimestampSchemaParser:
    def parse(self, kv):
        if len(kv) != 1:
            log.warning(f'timestamp type expression has additional elements: {kv}')
            pass
        return GenStrategy(time.time)


class StrSchemaParser(AbstractTypeParser):
    def parse(self, kv):
        self.assert_kv_len_eq2(kv)
        gen_type_value = kv[1].strip()
        if not gen_type_value:
            return GenStrategy(None, "")
        if gen_type_value == 'rand':
            return GenStrategy(uuid.uuid4)

        values = self._to_str_list(gen_type_value)
        if values:
            return GenStrategy(random.choice, values)
        else:
            return GenStrategy(None, gen_type_value)

    def _to_str_list(self, gen_type_value):
        as_list = self._safe_eval(gen_type_value)
        if type(as_list) == list:
            if len(as_list) == 0:
                raise DataSchemaParsingError(f'Type value should not be empty list')
            if not all(isinstance(x, str) for x in as_list):
                raise DataSchemaParsingError(f'Failed to convert type value {gen_type_value} to list of strings')

            as_list = [item.strip() for item in as_list]
            return as_list
        else:
            return None


class IntSchemaParser(AbstractTypeParser):
    def parse(self, kv):
        self.assert_kv_len_eq2(kv)
        gen_type_value = kv[1].strip()
        if not gen_type_value:
            return GenStrategy(None, "")
        if gen_type_value == 'rand':
            return GenStrategy(random.randint, 1, 10000)

        params = self._extract_rand_params(gen_type_value)
        if params:
            return GenStrategy(random.randint, params[0], params[1])

        list_params = self._to_int_list(gen_type_value)
        if list_params:
            return GenStrategy(random.choice, list_params)

        value = self._to_int_value(gen_type_value)
        return GenStrategy(None, value)

    def _to_int_list(self, gen_type_value):
        as_list = self._safe_eval(gen_type_value)
        if type(as_list) == list:
            if len(as_list) == 0:
                raise DataSchemaParsingError(f'Type value should not be empty list')
            if not all(isinstance(x, int) for x in as_list):
                raise DataSchemaParsingError(f'Failed to convert type value "{gen_type_value}" to list of int')
            return as_list
        else:
            return None

    def _to_int_value(self, gen_type_value):
        try:
            return int(gen_type_value)
        except ValueError:
            raise DataSchemaParsingError(f'Failed to convert type value "{gen_type_value}" to int')

    def _extract_rand_params(self, gen_type_value):
        if len(gen_type_value) > 4 and gen_type_value.startswith('rand'):
            possible_tuple = self._safe_eval(gen_type_value[4:])
            if not self._is_valid_randint_param(possible_tuple):
                raise DataSchemaParsingError(
                    f'Params for type value "{gen_type_value}" should be tuple of int with len == 2')
            return possible_tuple
        else:
            return None

    def _is_valid_randint_param(self, possible_tuple):
        return possible_tuple \
               and type(possible_tuple) == tuple \
               and len(possible_tuple) == 2 \
               and all(isinstance(x, int) for x in possible_tuple)


class GenStrategy:
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def run(self):
        if self.args:
            if self.func:
                result = self.func(*self.args)
            else:
                result = self.args[0]
        else:
            result = self.func()
        return str(result)

    def __str__(self):
        return f'GenStrategy[func={self.func}, args={self.args}]'


class DataSchemaParser:
    INT_PARSER = IntSchemaParser()
    STR_PARSER = StrSchemaParser()
    TIMESTAMP_PARSER = TimestampSchemaParser()

    def read_schema(self, schema_json_as_dict):
        log.info('Read data_schema={schema_json_as_dict}')
        strategies = {}
        for key, value in schema_json_as_dict.items():
            try:
                strategy = self._parse_value(value)
                strategies[key] = strategy
                log.info(f'Set schema key={key} strategy={strategy}')
            except DataSchemaParsingError as parseError:
                raise DataSchemaParsingError('key="{}": {}'.format(key, str(parseError)))
        return strategies

    def _parse_value(self, value):
        self._assert_value_is_parsable_string(value)
        kv = self._split_value(value)
        return self._parse_type_pair(kv)

    def _split_value(self, value):
        kv = str(value).split(':')
        if len(kv) > 2:
            raise DataSchemaParsingError(f'value={value} has wrong format. Additional :')
        return kv

    def _assert_value_is_parsable_string(self, value):
        if type(value) != str:
            raise DataSchemaParsingError(f'value={value} should be string')
        if not value:
            raise DataSchemaParsingError(f'value should not be empty string')

    def _parse_type_pair(self, kv):
        gen_type_name = kv[0].strip()
        if gen_type_name == 'timestamp':
            return DataSchemaParser.TIMESTAMP_PARSER.parse(kv)
        elif gen_type_name == 'str':
            return DataSchemaParser.STR_PARSER.parse(kv)
        elif gen_type_name == 'int':
            return DataSchemaParser.INT_PARSER.parse(kv)
        else:
            raise DataSchemaParsingError(f'Wrong format of generated type value "{gen_type_name}".'
                                         f' It should be separated by ":" as "type:value"')
