# Inspiration
I want to do the project in Golang to get more experience with using Go (it's
been a while, but it remember it being fun).

I think [merlin](https://github.com/Ne0nd0g/merlin) and [related projects](https://github.com/topics/backdoor?l=go) offer good inspiration.

# Sending/receiving commands
- the target needs root access
- also need some form of authentication

To communicate, keep a port open, listening to incoming messages
- make it seem like nothing's going on, redirect traffic to another port?

## How ccat works
- maybe draw an outline, add in pictures

## Requirement Completion
    Requirements:
    - provide remote root shell access to the system it's running on. From the
      controlling host, we should be able to send commands to the backdoored
      week4 machine.
    - persist even if the machine reboots. 
    - have some sort of configuration for where it gets commands from. This can
      be a file, argument, source code modification, etc. This way we can test
      it out, even if our controller host has a different address than yours.
    - authenticate its communication and/or commands. We don't want another
      attacker taking over our system.
    - attempt to hide itself from at least one detection method.

### Remote shell access to host
- do it SSH-style

### Persist across reboots
- EITHER store it on disk as a binary
  - OR have it in a cron job
  - OR find a way to keep it in memory. eg modify bootup (UEFI?) so that it cURLs from a server
    - abnormal network traffic; *ask others for advice!*

### Configuration for where to get commands
- maybe a simple file, maybe built into the code itself

### Authenticate communication
- asymmetric encryption? it'll take much longer

### Attempt to hide itself
- any commands originating from ccat must be obfuscated in files and process lists
- stretch: how to hide network traffic?

## Detecting ccat
- Tripwire
- network traffic (Wireshark, maybe Burp?)
- not sure what else. ask for advice to make it more advanced
