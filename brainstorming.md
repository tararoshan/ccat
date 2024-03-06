# Brainstorming/Casserole Document
## Inspiration
I want to do the project in Golang to get more experience with using Go (it's
been a while, but it remember it being fun).

I think [merlin](https://github.com/Ne0nd0g/merlin) and [backdoor projects](https://github.com/topics/backdoor?l=go)
and [remote access trojans](https://github.com/topics/remote-access-trojan) offer good inspiration.

## Resources (could be useful when writing the blog)
- for building [your own Go authentication service from scratch](https://mattermost.com/blog/how-to-build-an-authentication-microservice-in-golang-from-scratch/)
  - I chose not to do this because of time constraints
- a [comparison of Go authentication services](https://www.jetbrains.com/guide/go/tutorials/authentication-for-go-apps/auth/)
  - I chose to use JSON Web Token-based authentication because of the flexibility of encryption
  - also, I later found out that the server doesn't store the tokens for the sessions, it's the *client's* responsibility
    - if I understood the assignment correctly, that means that the backdoor won't store any info that could be used for compromise
- [Okta blogpost JWT with Go](https://auth0.com/blog/authentication-in-golang/)
- [LogRocket example walkthrough](https://blog.logrocket.com/jwt-authentication-go/)
- [jwt library](https://github.com/golang-jwt/jwt)
- [TCP and UDP servers in Go](https://www.linode.com/docs/guides/developing-udp-and-tcp-clients-and-servers-in-go/)

## Sending/receiving commands
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

