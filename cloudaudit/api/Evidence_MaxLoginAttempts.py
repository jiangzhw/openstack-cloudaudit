__author__ = 'joshd'

import cloudaudit.SystemAccess_Ssh
import re

class Evidence_MaxLoginAttempts(object):

    def __init__(self):
        self.accessor = cloudaudit.SystemAccess_Ssh.SystemAccess_Ssh()
        self.systems = None
        self.evidence = { }
        self.evidence_source = { }

    def getSystems(self):

        self.systems = self.accessor.getAllSshSystems()

        return self.systems
    
    def getEvidence(self):

        if self.systems == None:
            self.getSystems()

        for server in self.systems:
            source = "No enforcement present"
            osdef = self.accessor.getOS(server)
            ip = server.addresses['private'][0]
            maxLogins = -1  # -1 means unlimited loging attempts
            if osdef[ip] == 'Linux':
                lines = self.accessor.getCommandOutput(ip, "cat /etc/pam.d/system-auth | grep tally | grep deny")
                if len(lines) == 1:
                    matches = re.search("deny=(\d+)", lines[0])
                    if matches.lastindex == 1:
                        num = matches.group(1)
                        maxLogins = int(num)
                        source = "PAM Tally Module"

                if maxLogins == -1:
                    lines = self.accessor.getCommandOutput(ip, "od -x /var/log/faillog")
                    # TODO parse out maxlogins here
                    # source = "Faillog"

                self.evidence[ip] = maxLogins
                self.evidence_source[ip] = source

        return self.evidence

    def getEvidenceSources():
        return self.evidence_source
                


