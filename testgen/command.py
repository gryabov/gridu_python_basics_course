from argparse import ArgumentParser


def parse_arguments(args):
    parser = ArgumentParser(add_help=True, prog='testgen')

    parser.add_argument("path_to_save_files",
                        help="Where all files need to save",
                        nargs='*',
                        type=str)

    parser.add_argument("--file_name",
                        help="Base file_name. If no prefix, final file name will be file_name.json. "
                             "With prefix full file name will be file_name_file_prefix.json",
                        type=str)

    parser.add_argument("--data_schema",
                        help="It’s a string with json schema",
                        type=str)

    parser.add_argument("--files_count",
                        help="How much json files to generate",
                        type=int)

    parser.add_argument("--file_prefix",
                        help="What prefix for file name to use if more than 1 file needs to be generated",
                        choices=['count', 'random', 'uuid'],
                        type=str)

    parser.add_argument("--data_lines",
                        help="Count of lines for each file. ",
                        type=int)

    parser.add_argument("--clear_path",
                        help="If this flag is on, before the script starts creating new data files, "
                             "all files in path_to_save_files that match file_name will be deleted.",
                        type=bool)

    return parser.parse_args(args)
