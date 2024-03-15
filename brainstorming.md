# Brainstorming/Casserole Document
## Inspiration
I think I misinterpreted the assignment. 🤡

## Resources
- [Beej's guide](https://beej.us/guide/bgnet/html//index.html#client-server-background).

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

#### TODO
1. Send a CUSTOM message to the server
  - have the server print out what it receives
  - have the client print out a message from the server (eg. timestamp)
2. Keep an open connection to the server
3. Run each message as a sh process input

4. figure out how to make it work with firewalls?
5. figure out more advanced authentication than just a password ;-;
6. hide from detection

## How ccat works
- maybe draw an outline, add in pictures

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
