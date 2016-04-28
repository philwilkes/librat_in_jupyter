import subprocess
import os

def run_start(cmd):

    test_start = os.system('start')
    if test_start == 32512:
         raise Exception('You need to add librat environment variables to your path - refer to librat.wikispaces.com for more details')
    cmd, start = cmd.split('|')
    if not start.split()[-1].endswith('.obj'):
        raise IOError('.obj needs to be the last command')
    ps = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    start_process = subprocess.Popen(start.split(),
                                     stdin=ps.stdout,
                                     stderr=subprocess.PIPE)

    error = None
    for line in start_process.stderr:
        print line
        if line.startswith('rat'):
            error = True
        elif line.startswith('error'):
            error = True
        elif "multiple defined material" in line:
            error = True
        elif "error defining number of pulse samples" in line:
            error = True
        elif "not found for cloning" in line:
            error = True

    return error
