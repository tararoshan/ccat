# Brainstorming/Casserole Document
I think I misinterpreted the assignment. 🤡

## Resources
- 

#### TODO
1. Have the compromised client periodically call out/launch
    - make the program sleep for 2 minutes in a loop if it couldn't connect
2. Provide a remote shell
    - once they've connected, have the client stay awake and listen
**    - hide behind a commonly used process name or try to change the name in the
      kernel? to make it not appear. Could also have the program run this before
      actually trying to connect for the first time
    - HOW DO I DO THIS AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
3. Persist if the machine reboots
**    - store in memory
**    - Rootkit: can modify system files, kernel modules, or boot processes to
      conceal malicious processes and network connections. Advanced rootkits may
      employ techniques such as kernel-level hooking, process hiding, and memory
      manipulation to evade detection by security tools.
    - Process Injection
      - python https://ancat.github.io/python/2019/01/01/python-ptrace.html
4. Configuration for testing
    - edit the source code. create them as variables at the top of the files
5. Authenticate communication
**    - chp 9 of the book I found
    - check it works with firewalls!
6. Hide from detection
**    - wipe out system logs in /var/log
**    - process hiding (process list) rootkit
    - sleep to avoid lots of network traffic
7. Extra credit script
**    - something?

----------------------------------------------------------------------------------------------------

# Future Work
Making the C version.
- [Beej's Networking Guide](https://beej.us/guide/bgnet/html//index.html#client-server-background).
- https://github.com/prownd/remote-shell/tree/master

## How ccat works
- maybe draw an outline, add in pictures

### Remote shell access to host
- do it SSH-style

### Persist across reboots
- EITHER store it on disk as a binary
  - OR have it in a cron job
  - OR find a way to keep it in memory. eg modify bootup (UEFI?) so that it cURLs from a server
    - abnormal network traffic; *ask others for advice!*

### Authenticate communication
- asymmetric encryption? it'll take much longer

### Attempt to hide itself
- any commands originating from ccat must be obfuscated in files and process lists
- stretch: how to hide network traffic?

## Detecting ccat
- Tripwire
- network traffic (Wireshark, maybe Burp?)
- not sure what else. ask for advice to make it more advanced
