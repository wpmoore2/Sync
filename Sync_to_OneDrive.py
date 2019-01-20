import subprocess as sp
import yaml
import sys

# /S  - copy subdirectories, if not empty
# /xo - only copy newer files (included those edited)
SYNC_CMD = "robocopy /S /xo"
CONFIG_PATH = 'C:/Users/wmsoc/home/Documents/P.Projects/Sync/sync_config.yml'

#
# Can specify to only print sync commands that would be executed
PRINT_ONLY = False
if "-n" in sys.argv:
    print ("Print only")
    PRINT_ONLY = True

QUIET = False
if "-q" in sys.argv:
    print ("Quiet mode")
    QUIET = True

# Define sync function to be used below
def sync(src, dest, base_path, mirror):
    ''' Define the recursive sync function. Essentially parses the config dict
        and calls 'sync_process' for each src:dest pair
    '''
    if isinstance(dest, str):
        src = "\"{}\"".format(src)
        dest = "\"{}\\{}\"".format(base_path, dest)
        full_cmd = "{} {} {} {}".format(SYNC_CMD, src, dest, mirror)

        if not QUIET:
            print (full_cmd)
        if not PRINT_ONLY:
            process = sp.Popen(full_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        return
    else:
        for item in dest:
            if src != "":
                new_src = "{}\{}".format(src, item)
            else:
                new_src = item
            sync(new_src, dest[item], base_path, mirror)

#
# Parse in config file, and use sync function
try:
    config = yaml.load(open(CONFIG_PATH, 'r'))
except Exception as err:
    print ("ERROR: Failed to parse {}.\n{}".format(CONFIG_PATH, str(err)))
    raise err

# Can define OndeDrive path in config, or assume in default user directory
if config.get('OneDrive_base'):
    base_path = config['OneDrive_base']
else:
    try:
        user = sp.check_output("echo %USERNAME%", shell=True).decode('UTF-8').strip()
    except Exception as err2:
        print ("ERROR: Failed to get current user.\n{}".format(str(err2)))
        raise err2
    base_path = "C:\\Users\\{}\\OneDrive".format(user)

if config.get("NO_MIRROR") and config['NO_MIRROR'] is not None:
    sync("", config['NO_MIRROR'], base_path, "")

if config.get('MIRROR') and config['MIRROR'] is not None:
    sync("", config['MIRROR'], base_path, "/MIR")


print ("Press any key to continue...")
input()