# Datadog Agent Check Plugin for OpenLDAP
# debug for:
# sudo -u dd-agent dd-agent check openldap

from checks import AgentCheck
from ldap3 import *

class OpenLDAPCheck(AgentCheck):
    def check(self, instance):
        res = {}
        verbose = self.init_config.get('verbose', False)
        server = Server(instance['url'])
        c = Connection(server, auto_bind = True, user=instance['user'], password=instance['password'])
        c.search(search_base = 'cn=Threads,cn=Monitor',
                 search_filter = '(objectClass=monitoredObject)',
                 search_scope = LEVEL,
                 attributes = ['monitoredInfo'])
        for entry in c.response:
            if 'monitoredInfo' in entry['attributes']:
                res[entry['dn']] = entry['attributes']['monitoredInfo']

        c.search(search_base = 'cn=Connections,cn=Monitor',
                 search_filter = '(objectClass=monitorCounterObject)',
                 search_scope = SUBTREE,
                 attributes = ['monitorCounter'])
        for entry in c.response:
            if 'monitorCounter' in entry['attributes']:
                res[entry['dn']] = entry['attributes']['monitorCounter']

#        for dn, value in res.iteritems():
#            print dn, value

        self.gauge('openldap.connections.current', 'cn=Current,cn=Connections,cn=Monitor')
        self.gauge('openldap.threads.max', 'cn=Max,cn=Threads,cn=Monitor')
        self.gauge('openldap.threads.open', 'cn=Open,cn=Threads,cn=Monitor')
        self.gauge('openldap.threads.active', 'cn=Active,cn=Threads,cn=Monitor')
