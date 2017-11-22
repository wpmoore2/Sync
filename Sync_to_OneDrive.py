import subprocess as sp
import yaml

cmd = "dir"

process = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)


for line in process.stdout:
    print (line.decode('UTF-8'))