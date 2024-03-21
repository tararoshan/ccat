# ccat
Command &amp; control after trespassing (ccat) is built as a durable backdoor
for friendly hackers to continue interacting with a target machine after gaining
root access. The name is inspired by the naming of Iranian Advanced Persistent
Threats (APTs) as "kittens."

I originally wanted to write it in C (Ccat!), but I misinterpreted the project
and only realized it on Monday, two days before the project was due. I'd like to
come back to this in the future and create a C version as well. For now, it'll
exist in python form only.

## How to Install
Install the server folder onto the remote/target machine. Install the client
folder onto the controlling machine.
- cURL from a website (GitHub)
- add in pictures, gifs
- RUN THE SERVER BFORE THE CLIENT!!!
- cannot cd and expect the client to remember -- need to do cd && whatever other command
## How ccat works

## Requirement Completion
### Remote shell access to host

### Persist across reboots

### Configuration for where to get commands

### Authenticate communication

### Attempt to hide itself

## Detecting ccat


## Resources & Credit
I used [this](https://medium.com/@songchai.d01/how-to-create-a-reverse-shell-in-python-41fe75d88521)
Medium article to learn how to use the sockets, subprocess, and sys python libraries for building a
reverse shell. The code written using this article is contained in lines ?? - ?? in server.py 
and ?? - ?? client.py. I found similar resources
[here](https://medium.com/geekculture/breaking-down-a-python-reverse-shell-one-liner-752041733e5f)
and [here](https://stackoverflow.com/questions/28411960/execute-a-command-on-remote-machine-in-python/28413657#28413657),
as well as the [official docs](https://docs.python.org/2.6/library/socket.html).

I used the [PyCryptodome documentation](https://pycryptodome.readthedocs.io/en/latest/src/public_key/ecc.html)
for ECC (asymmetric).
