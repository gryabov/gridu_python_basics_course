**Project description:**

Imagine that you have a data pipeline and you need some test data to check the correctness of data transformations and validations on this data pipeline.
You need to generate different input data.In our Capstone project, we will solve it by creating a universal console utility that will generate our data for us. Format - only JSON.

Create all descriptions, names for commands, etc by yourself.

**You need to implement:**

1. **Name, description, help.** Console Utility (CU) must have a name. You need to set a name on it and the name must be shown in "help". Each command must have a help. Use argparse to get all those features from the box.
2. **All params could be set up from cmd (command line).** CU must take all params needed to generate data from the command line, but most of them must have default values.
3. **Default values**. All params for CU must have default values. All those values must be shown in CU help. All default values must be stored in "default.ini" file and read from it with configparser. Names of options in default.ini must be identical to those options in console utility help.
4. **Logging**. All steps must have output in the console. If you've got some error, you must print it to the console with logging.error and only after that exit. If you start data generating - you need to write about it in the console, same if you finish. All logs must be printed in console. If you want to, you can also duplicate all logs in a log file, but it is optional for this project.
5. **Random data generation dependent on field type and data schema**. Described in detail in the "Data Schema Parse" point.

**Data Schema Parse:**

Your script must parse data schema and generate data based on it.
All keys in data schema == keys in the final data event line.

**Example of data schema:**

    {"date":"timestamp:", "name": "str:rand", "type":"str:['client', 'partner', 'government']", "age": "int:rand(1, 90)"}

**All values support special notation** "**type**:what_to_generate":

":" in value indicate that left part of the value is a type.

**Type could be**: timestamp, str, and int.

If in the schema there is another type on the left part of ":" statement in a value, write an error.
For example, "str:rand" means that value of this key must be a str type and it's generated randomly.

**For right part of values with ":" notation, possible 4 types:**

1. **rand** - random generation,<br/>
if on the left there is "str" type, for generation use uuid4 (need to use only one function to generate uuid prefix - https://docs.python.org/3.6/library/uuid.html#uuid.uuid4), str(uuid.uuid4())
If on the left there is "int" type, use random.randint(0, 10000)

2. **list with values []**. <br/>
For example, "str:['client', 'partner', 'government']" or "int:[0, 9, 10, 4]". A generator must take a random value from a list for each generated data line. Use random.choice.
    
3. **rand(from, to)** - random generation for int values in the prescribed range. <br/>
Possible to use only with "int" type. If on the left part "str" or "timestamp", write an error.
    
4. **Stand alone value.** <br/>
If in schema after ":" a value is written, which has a type corresponding with the left part, and the word "rand" is not reserved, use it on each line of generated data. For example, "name": "str:cat". So your script generates data where in each line attr "name":"cat" will be. But if in schema there is "age":"int:head", it is an error and you must write about it in console because "head" could not be converted to int type.

5. **Empty value**.<br/>
It's normal for any type. If type "int" is with empty value, use None in value, if type "str", use empty string - "". 

**For timestamp type** ignore all values after ":". If a value exists in the scheme, write logging.warning with a note that timestamp does not support any values and it will be ignored. Continue correct script work.

**Value for timestamp is always current unix timestamp** - enough to use time.time().

    {"date":"timestamp:", "name": "str:rand", "type":"str:['client', 'partner', 'government']", "age": "int:rand(1, 90)"}

**List of input params for CU:**

**Name and Description you can freely change**
    
|Name|Description|Behavior|
| ------------- |-------------| ----- |
| path_to_save_files  | Where all files need to save | User can define path in 2 ways: relatively from cwd (current working directory) and absolute. You CU must correct work with both ways and check exist such path or not. If path exist and it is not a directory - exit with error log  |
| files_count | How much json files to generate|if files_count < 0 - error <br/> if files_count == 0 - print all output to console.|
| file_name | Base file_name. If no prefix, final file name will be file_name.json. With prefix full file name will be file_name_file_prefix.json ||
| file_prefix | What prefix for file name to use if more than 1 file needs to be generated | prefix is a set of possible choices (https://docs.python.org/3.6/library/argparse.html#choices) <b><br/>   -count <br/>-random <br/> -uuid</b><br/>(need to use only one function to generate uuid prefix - https://docs.python.org/3.6/library/uuid.html#uuid.uuid4, str(uuid.uuid4()))|
| data_schema | It's a string with json schema.<br/> It could be loaded in two ways:<ol><li>With path to json file with schema</li><li>with schema entered to command line.</li></ol>Data Schema must support all protocols that are described in <b>"Data Schema Parse"</b>| Read schema and check if it's correct or not (see "Data Schema Parse" with details of schema). |
| data_lines | Count of lines for each file. Default, for example: 1000.| |
| clear_path | If this flag is on, before the script starts creating new data files, all files in path_to_save_files that match file_name will be deleted.| If this flag is on, store true (https://docs.python.org/3.6/library/argparse.html#action , see action='store_true') |

**Example of CU launch with provided data_schema from cmd:**

     $ testgen.py . --files_count 3 --file_name super_data --file_prefix count --data_schema {"date":"timestamp:", "name": "str:rand", "type":"['client', 'partner', 'government']", "age": "int:rand(1, 90)"}

**Data schema from file:**

    $ testgen.py . --files_count 3 --file_name super_data --file_prefix count --data_schema ./path/to/schema.json

**Do not use Traceback errors and raise:**<br/>
If it's a console utility, it must have the correspondent behavior. You do not need to send Interpreter traceback or raise errors. All errors that caused exit from script must be processed with "sys.exit(1)" or "exit(1)", not with raise.

**Acceptance Criteria:** 
- All features are implemented and work;
- All possible errors are processed and they have a logging and correct exit (impossible to create a file, incorrect values, etc.);
- Code must be divided into functions/classes/ logic blocks. It must not be a a monolithic sheet of code;
- Unit tests exist (at least 3 tests);
- All steps from the Project Checklist module are done.