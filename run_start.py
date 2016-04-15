import subprocess

def run_start(cmd):
    cmd, start = cmd.split('|')
    if not start.split()[-1].endswith('.obj'):
        raise IOError('.obj needs to be the last command')
    ps = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    start_process = subprocess.Popen(['start', start.split()[-1]], 
                                     stdin=ps.stdout, stderr=subprocess.PIPE)
    #start_process.wait()
    error = None
    for line in start_process.stderr:
        print line
	if line.startswith('rat') or line.startswith('error'):
		error = True

    return error

