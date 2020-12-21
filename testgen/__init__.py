import logging.config
import os
import sys

from testgen.command import parse_arguments
from testgen.config_reader import Defaults
from testgen.exceptions import TestgenBaseException
from testgen.generator import DataGenerator
from testgen.options import Options

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
log = logging.getLogger("testgen")


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    try:
        parsed_args = parse_arguments(args)
        defaults = Defaults()
        opt = Options(parsed_args, defaults)
        DataGenerator().generate(opt)
    except TestgenBaseException as e:
        log.exception(e)
        print("ERROR: " + str(e))
        sys.exit(1)
    except Exception as e:
        log.exception(e)
        print("ERROR: internal error")
        sys.exit(1)