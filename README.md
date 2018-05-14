
# IPcollector Diagnostic Tool

## Synopsis
This tool is used for diagnose and identify any setup and configuration on IPcollector
## Assumptions
1. ipcenter url passed as environment variable IPCENTER_URL
2. /root/.my.cnf is setup for passwordless access with root account to run MySQL queries
## Code Example
This is written in Python thus limiting to available built-in Python modules on IPcollector
## Motivation
To provide quick troubleshooting help in identifying setup or configuration issues on IPcollector
## Installation
Just check out ipcd.pl from the repository
## API Reference
None
## Contributors
Ming Yung
## License
To be filled out.
## Tests
[root@ipcollector01 utils]# ./ipcd.py
        ERROR: IPCENTER_URL environment variable must be set!
[root@ipcollector01 utils]# export IPCENTER_URL=jersey.ipcenter.com
[root@ipcollector01 utils]# ./ipcd.py

    Validating connectivities to openvpn, ntp ...


        *** Validating NTP connection ...

        SUCCESS: NTP, ntp.svc.ipsoft.com, has been setup correctly and operational.

        *** Validating OVPN connection ...

        SUCCESS: HTTPS connection is established to OpenVPN 10.140.167.22.

    Find and extract VIP from configuration file ...

        *** VIP 10.140.167.132 has been extracted from /etc/keepalived/keepalived.conf ...

    Validating VIP setup and configuration ...

        SUCCESS: VIP, 10.140.167.132, has been setup correctly.

    Testing DNS resolution for essential operations and diagnose possible misconfiguration ...

        *** jersey.ipcenter.com has been validated ...
        *** mx1-jersey.ipcenter.com has been validated ...
        SUCCESS: DNS for jersey.ipcenter.com and its mx records are resolvable.

    Validating esper rules or non-esper rules ...

        SUCCESS: All 13 esper rules are active.

    Inject IPradar event and validate ...

        SUCCESS: Radar event test passed with httpd code 200

    Running test cases ...

        SUCCESS: MySQL is running...
        SUCCESS: OpenVPN is running...
        SUCCESS: Keepalived is running...
        SUCCESS: IPcollector is running...


All validations completed successfully
# demo-code
