"""###################################################################################################################

The purpose of this script is to use Fabric as a "management" console for the wallboards, it's currently being
used as a front end but this will be the middle section to a GUI interface that I will eventually create

Goals:
1) Have the script insert
############################################
Current Wallboard Configuration:
Wallboard1 - 192.168.1.131
Wallboard2 - 192.168.1.132
Wallboard3 - 192.168.1.133
Wallboard4 - 192.168.1.134

############################################
Dependencies:
- Mac CSV.csv
- Artists.csv
############################################
Change log:


##################################################################################################################"""

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
    env.hosts = []
    macFile = open("Mac CSV.csv", 'r')
    totalList = macFile.readlines()
    for i in range(len(totalList)):
        totalList[i] = totalList[i].rstrip()
    for x in totalList:
        env.hosts.append(x.split(",",1)[1])

@task
def artHosts():
    env.hosts = []
    mFile = open("Artists.csv", 'r')
    totalList = mFile.readlines()
    for i in range(len(totalList)):
        totalList[i] = totalList[i].rstrip()
    for x in totalList:
        env.hosts.append(x.split(",",1)[1])

@task
def testHosts(): #testing purposes only 
    env.hosts = ['192.168.1.160', '192.168.1.151', '192.168.1.163']

@task
def singleHost():
    env.hosts = ['192.168.1.206']


"""##########################################################################"""

@task
def custom():
    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'xadmin'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")

    #Variable declarations:
    commands = 'sudo defaults write /Library/Preferences/com.apple.RemoteManagement VNCAlwaysStartOnConsole -bool true'
    with hide('output', 'running'), settings(warn_only=False, timeout=1, colorize_errors=True, connection_attempts=2):
        return sudo(commands)

@task
def deployScript():

    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'xadmin'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this
    
    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")
    
    #Variable declarations:
    commands = 'chmod 777 /Users/Shared/logouthook;' \
              'defaults write com.apple.loginwindow LogoutHook /Users/Shared/logouthook'
    #commands = scp -v xadmin@192.168.1.111:/Users/xadmin/Desktop/logoutScript/logouthook /Users/Shared/;
    #commands = 'mkdir ~/Desktop/COOOOOOOOOOOOOOOOOOOOL'
    put("/home/jquintanilla/Documents/Fabric Scripts/MacDeployments/logouthook", "/Users/Shared/")
    with hide('output', 'running'), settings(warn_only=False, timeout=1, colorize_errors=True, connection_attempts=2):
    #with settings(warn_only=True, timeout=1, colorize_errors=True, connection_attempts=2): #for testing purposes
        return sudo(commands)

@task
def franchiseDeploy():

    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'xadmin'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")

    #Variable declarations:
    commands = 'installer -pkg /Users/Shared/bizhub_C554_C364_109.pkg -target /;' \
              '/usr/sbin/lpadmin -p Franchise_KM -E -v lpd://192.168.0.220 -P ' \
               '/Library/Printers/PPDs/Contents/Resources/KONICAMINOLTAC364e.gz ' \
               '-D \'Franchise KM\''
    #commands = scp -v xadmin@192.168.1.111:/Users/xadmin/Desktop/logoutScript/logouthook /Users/Shared/;
    #commands = 'mkdir ~/Desktop/COOOOOOOOOOOOOOOOOOOOL'
    put("/home/jquintanilla/Documents/Fabric Scripts/MacDeployments/bizhub_C554_C364_109.pkg", "/Users/Shared/")
    with hide('output', 'running'), settings(warn_only=False, timeout=1, colorize_errors=True, connection_attempts=2):
    #with settings(warn_only=True, timeout=1, colorize_errors=True, connection_attempts=2): #for testing purposes
        return sudo(commands)

@task
def printerDeploy():

    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'xadmin'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")

    #Variable declarations:
    commands = 'installer -pkg /Users/Shared/Xerox\ Print\ Driver\ 3.64.0.pkg -target /;' \
              '/usr/sbin/lpadmin -p Art_WorkCentre -E -v lpd://192.168.0.244 -P ' \
               '/Library/Printers/PPDs/Contents/Resources/Xerox\ ColorQube\ 8700S.gz ' \
               '-D \'Art Xerox\''
    #commands = scp -v xadmin@192.168.1.111:/Users/xadmin/Desktop/logoutScript/logouthook /Users/Shared/;
    #commands = 'mkdir ~/Desktop/COOOOOOOOOOOOOOOOOOOOL'
    with hide('output', 'running'), settings(warn_only=False, timeout=1, colorize_errors=True, connection_attempts=2):
    #with settings(warn_only=True, timeout=1, colorize_errors=True, connection_attempts=2): #for testing purposes
        return sudo(commands)

@task
def fieryDeploy():

    env.user = 'xadmin'

    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")

    #Variable declarations:
    commands = 'installer -pkg /Users/Shared/Fiery\ Printer\ Driver.pkg -target /;' \
              '/usr/sbin/lpadmin -p ArtFiery -E -v lpd://192.168.0.76 -P ' \
               '/Library/Printers/PPDs/Contents/Resources/en.lproj/Xerox\ WC\ 7800-7970Series\ EFI ' \
               '-D \'Art Fiery\''
    with hide('output', 'running'), settings(warn_only=False, timeout=1, colorize_errors=True, connection_attempts=2):
        return sudo(commands)

@task
def info():

    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'xadmin'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")

    #Variable declarations:
    commands = 'dsconfigad -show'
    with hide('output', 'running'), settings(warn_only=False, timeout=1, colorize_errors=True, connection_attempts=2):
        return sudo(commands)

@task
def file_get():
    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'xadmin'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")
    get("/Library/Preferences/com.microsoft.office.licensing.plist", "/home/jquintanilla/Documents/temp"+"."+env.host)

@task
def main_message():
    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'xadmin'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")

    #Variable declarations:
    commands = 'osascript -e' 'display notification "Lorem ipsum dolor sit amet" with title "Title"'
    with hide('output', 'running'), settings(warn_only=False, timeout=1, colorize_errors=True, connection_attempts=2):
        return sudo(commands)

@task
def grab():
    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'xadmin'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Script processing commencing")

    #commands = "system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'"
    #commands = "ls -a /Users/"
    commands = "hostname"
    with hide('output', 'running'), settings(warn_only=False, timeout=1, colorize_errors=True, connection_attempts=2):
        return sudo(commands)

@task
def move():
    env.user = 'xadmin'
    env.skip_bad_hosts = True
    put("/home/jquintanilla/Documents/Fabric Scripts/MacDeployments/Xerox Print Driver 3.64.0.pkg", "/Users/Shared/")

@task
def moveFiery():
    env.user = 'xadmin'
    env.skip_bad_hosts = True
    put("/home/jquintanilla/Documents/Fabric Scripts/MacDeployments/Fiery Printer Driver.pkg", "/Users/Shared/")

@task
def moveCustom():
    env.user = 'xadmin'
    env.skip_bad_hosts = True
    put("/home/jquintanilla/Documents/Fabric Scripts/MacDeployments/Fiery Printer Driver.pkg", "/Users/Shared/")


@task
@runs_once
def send():
    results = execute(deployScript)
    print yellow("Executions completed without error")
    print yellow("Here are results from send call for results: %s") % (results)

@task
@runs_once
def fire():
    results = execute(fieryDeploy)
    print yellow("Executions completed")
    print yellow("Here are results from send call for results: %s") % (results)

@task
@runs_once
def copy():
    results = execute(moveFiery)
    print yellow("Executions completed")
    print yellow("Here are results from send call for results: %s") % (results)

@task
@runs_once
def probe():
    results = execute(info)
    print yellow("Executions completed")
    print yellow("Here are results from send call for results: %s") % (results)

@task
@runs_once
def key():
    results = execute(file_get)
    print yellow("Executions completed")
    print yellow("Here are results from send call for results: %s") % (results)

@task
@runs_once
def message():
    results = execute(main_message)
    print yellow("Executions completed")
    print yellow("Here are results from send call for results: %s") % (results)

@task
@runs_once
def franchise():
    results = execute(franchiseDeploy)
    print yellow("Executions completed")
    print yellow("Here are results from send call for results: %s") % (results)

@task
@runs_once
def demosh():
    #Use this one for custom codes
    results = execute(custom)
    print yellow("Executions completed")
    print yellow("Here are results from send call for results: %s") % (results)

@task
@runs_once
def serial():
    results = execute(grab)
    print yellow("Executions are complete")
    #print green(results)
    for j,k in results.iteritems():
        print green("{} -> {} ".format(j,k))

