import subprocess as sp
import yaml
import sys

# /S  - copy subdirectories, if not empty
# /xo - only copy newer files (included those edited)
# /fp - Include Full Pathname of files in the output.
# /ns - No Size - don’t log file sizes.
# /ndl - No Directory List - don’t log directory names.
SYNC_CMD = "robocopy /S /xo /fp /ns /ndl"

if "onedrive" in sys.argv:
    CONFIG_PATH = 'C:/Users/wmsoc/home/Documents/P.Projects/Sync/Onedrive/sync_config.yml'
elif "extdrive" in sys.argv:
    CONFIG_PATH = 'C:/Users/wmsoc/home/Documents/P.Projects/Sync/ExtDrive/sync_config.yml'
else:
    exit("No configured drive specified")

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
#
# # MAIN FUNCTION - sync
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
            # replace '' with b'' for Python 3
            if not QUIET:
                for c in iter(lambda: process.stdout.read(1), ''):
                    sys.stdout.write(c.decode("utf-8"))
        return
    else:
        for item in dest:
            if src != "":
                new_src = "{}\{}".format(src, item)
            else:
                new_src = item
            sync(new_src, dest[item], base_path, mirror)

#
# # FUNCTION - get_base_dir
# Can define drive path in config, or assume in default user directory (for onedrive)
def get_base_dir(config):
    if config.get('base_dest'):
        base_path = config['base_dest']
    else:
        try:
            user = sp.check_output("echo %USERNAME%", shell=True).decode('UTF-8').strip()
        except Exception as err2:
            print ("ERROR: Failed to get current user.\n{}".format(str(err2)))
            raise err2
        base_path = "C:\\Users\\{}\\OneDrive".format(user)
    return base_path

#
# Parse in config file, and use sync function
try:
    config = yaml.load(open(CONFIG_PATH, 'r'))
except Exception as err:
    print ("ERROR: Failed to parse {}.\n{}".format(CONFIG_PATH, str(err)))
    raise err

base_path = get_base_dir(config)

# Run NO-MIRROR version
if config.get("NO_MIRROR") and config['NO_MIRROR'] is not None:
    sync("", config['NO_MIRROR'], base_path, "")

# Run MIRROR version
if config.get('MIRROR') and config['MIRROR'] is not None:
    sync("", config['MIRROR'], base_path, "/MIR")

print ("Press any key to continue...")
input()
exit()
