#################################################################################
##
## bash.py
##  To run bash commands from python and stop on error
##  Useful when you know the bash command but are working in python.
##  Eventually commands that can be run natively in python can be replaced
##  But some things are better in bash
##
##  Nicholas Dietz
## 
#################################################################################
import os
import subprocess
import shlex

# https://stackoverflow.com/questions/4256107/running-bash-commands-in-python/51950538
def bash(cmd):
    # https://stackoverflow.com/questions/3503719/emulating-bash-source-in-python
    print(f'Runinng bash command: {cmd}')
    if "'" in cmd:
        print("warning: apostrophe's might cause trouble")
    bashCommand = f"env bash -c '{cmd}'"
    bashCommand = shlex.split(bashCommand)
    #bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    print(bashCommand)
    # pipe stderr to stdout so we don't miss error messages
    process = subprocess.Popen(bashCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, universal_newlines=True)

    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    output = ''
    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line, end="")
        output = output + stdout_line
    process.stdout.close()
    return_code = process.wait()
    if return_code:
        #raise subprocess.CalledProcessError(return_code, cmd)
    #    print(output)
        raise ValueError("Bash command failed")
    return output

# https://stackoverflow.com/questions/4256107/running-bash-commands-in-python/51950538
def bash_disown(cmd):
    # run command and let it go on running after python exits
    # https://stackoverflow.com/questions/3503719/emulating-bash-source-in-python
    # https://stackoverflow.com/questions/6011235/run-a-program-from-python-and-have-it-continue-to-run-after-the-script-is-kille
    print('ok')
    print(f'Runinng bash command: {cmd}')
    bashCommand = f"env bash -c 'nohup {cmd}'"
    bashCommand = shlex.split(bashCommand)

    #setpgrp used to let xdg-open not kill the pdf viewer
    process = subprocess.Popen(bashCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                               universal_newlines=True, preexec_fn=os.setpgrp)
    print('done with bash')


# https://stackoverflow.com/questions/4256107/running-bash-commands-in-python/51950538
def bash_return_str(cmd):
    # this was a duplicate function
    return bash(cmd)

def main():
    bash('echo "hello world"')

if __name__ == '__main__':
    main()
