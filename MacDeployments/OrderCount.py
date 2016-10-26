#################################################################################The goal of this code is to run a grep command on remote servers, tally the tot#al order count and display or email it to an intended target.
#
#Servers:
# app1 - 172.16.10.102
# app2 - 172.16.10.103
# app3 - 172.16.10.104
# app4 - 172.16.10.105
# web1 - 172.16.100.20
# web2 - 172.16.100.21
#
#Command to be run:
# grep -c "Order Payment Status" /opt/ct-live/Crown/root/log/tc-start.log 
#
#
#
################################################################################################################################################################

#Function and API imports#

from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm


"""#######################Define remote server settings######################"""

#Select the user that will be used for the SSH connection:
#user = ''

#Able to
env.hosts = ['test_server']

"""##########################################################################"""


def orderSum():
    logDirectory = '/opt/ct-live/Crown/root/log/'
    command = '
    with cd(logDirectory):
        local(g')
