"""####################################################################################################################

The purpose of this code is to make an easier and faster way to search through the app server logs

The script will use search queries (ordernum/supportcode and date) and return the records found with the unique
session ID


Currently only developing support for support code, I will work on order number in the future

Servers:
app1 - 172.16.10.102
app2 - 172.16.10.103
app3 - 172.16.10.104
app4 - 172.16.10.105
app5 - 172.16.10.106
app6 - 172.16.10.107

Commands to be run:
grep -c *ordernumber* /opt/ct-live/Crown/root/log/tc-start.log (gets line where the session ID would be)



Change log:

#####################################################################################################################"""

#Function and API imports#
from __future__ import with_statement
from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import OrderedDict
import datetime

__author__ = "Jonathan Quintanilla"

"""#######################Define environment settings########################"""

#Define all the remote servers to run script:
@task
def prodHosts():
    env.hosts = ['172.16.10.102','172.16.10.103','172.16.10.104','172.16.10.105','172.16.10.106','172.16.10.107']

@task
def testHosts(): #testing purposes only 
    env.hosts = ['192.168.1.164']

"""##########################################################################"""

@task
def engraving(unique,startdate,enddate):


@task
def custom(supportcode2,date2):
    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'storefront'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")
    """
    if date2 == 000000:
        #Variable declarations:
        commands = 'cat /opt/ct-live/Crown/root/log/tc-start.log | grep \"%s\"' % supportcode2

        #with settings(warn_only=True, timeout=1, colorize_errors=True, connection_attempts=2): #for testing purposes
        with hide('output', 'running'), settings(warn_only=False, timeout=1,
                                                 colorize_errors=True, connection_attempts=2):
            return sudo(commands)
    """
    #Variable declarations:
    commands = 'grep {0} /opt/logbackup/tc-start.{1}'.format(supportcode2, date2)
    #with settings(warn_only=True, timeout=1, colorize_errors=True, connection_attempts=2): #for testing purposes
    with hide('output', 'running'), settings(warn_only=True, timeout=100, colorize_errors=True, connection_attempts=2):
        result = run(commands)

@task
@runs_once
def final(supportcode, date):
    results = execute(custom, supportcode, date)
    print yellow("Executions completed")
    print yellow("Here are results from send call for results: %s") % results

    for i in results.items():
        #tempList = i.value.replace("\r\n", "")
        print i.values()