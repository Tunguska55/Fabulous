"""#########################################################################################################################
#The goal of this code is to run a grep command on remote servers, tally the total order count and display or email it to an intended target. ------completed 06-02-15
#
#The script needs to be able to tally the total number of orders in an hour every hour from 5AM - 11PM, example: 
# Hour 1 (5AM - 6AM) - 1 order(s)
# Hour 2 (6AM - 7PM) - 3 order(s)
# etc
#
#Servers:
# app1 - 172.16.10.102
# app2 - 172.16.10.103
# app3 - 172.16.10.104
# app4 - 172.16.10.105
# web1 - 172.16.10.30
# web2 - 172.16.10.31
#
#Commands to be run:
# grep -c "Order Payment Status" /opt/ct-live/Crown/root/log/tc-start.log (gets the total number of web orders) 
# grep "Order Payment Status" /opt/ct-live/Crown/root/log/tc-start.log (gets the whole line including date) 
#
#
#
#
#
#
Change log:

06-02-15 - the web orders are tallied and sent to the declared recipients with proper HTML formatting
06-03-15 - added timestamp to email that is sent
06-04-15 - added the ability tally the sum of orders for every hour between every server

############################################################################################################################"""

#Function and API imports#
from __future__ import with_statement
from fabric.api import *
from fabric.colors import *
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
    env.hosts = ['172.16.10.102', '172.16.10.103', '172.16.10.104', '172.16.10.105', '172.16.10.106', '172.16.10.107']
    #env.hosts = ['172.16.10.102'] # for testing purposes
@task
def testHosts(): #testing purposes only 
    env.hosts = ['192.163.2.14', 'test_server2']


"""##########################################################################"""

#Code gets the numbers and stores it in a list variable to keep persistence in data#

@task
def orderSum():

    #Select the user that will be used for the SSH connection (default is current user):
    env.user = 'storefront'

    #Skips the hosts that timeout or fail to prevent code from stopping, to view problems go to send function#
    env.skip_bad_hosts = True # will eventually write exception handling to circumvent this
    
    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Total sum being collected")
    
    #Variable declarations:
    commands = 'grep -c \"Order Payment Status\" /opt/ct-live/Crown/root/log/tc-start.log'
    
    with hide('output', 'running'), settings(warn_only=True, timeout=1, colorize_errors=True, connection_attempts=2):
    #with settings(warn_only=True, timeout=1, colorize_errors=True, connection_attempts=2): #for testing purposes
        return run(commands)


@task
def hourlySum():

    #see orderSum for explanations on code#
    
    env.user = 'storefront'
    env.skip_bad_hosts = True
    commands = 'grep \"Order Payment Status\" /opt/ct-live/Crown/root/log/tc-start.log'

    print green("Executing on " + red("%s ") + green("as ") + blue("%s ")) % (env.host, env.user)
    print green("Hourly sum being collected")

    with settings(warn_only=True, timeout=1, colorize_errors=True, connection_attempts=2): #for testing purposes
        return run(commands)

@task
def convertTime(t): #converts the list into a formatted string
    a = int(t[0])
    if a > 12:
        b = "0" + str(int(t[0]) - 12) + ":" + t[1] + ":" + t[2] + " PM"
        return b
    else:
        b = t[0] + ":" + t[1] + ":" + t[2] + " AM"
        return b
        
@task
@runs_once
def send():
    hourly = execute(hourlySum)
    results = execute(orderSum)
    print yellow("Executions completed without error")
    print yellow("Here are results from send call for hourly: %s") % (hourly) # for testing purposes
    print yellow("Here are results from send call for results: %s") % (results.keys())  #for testing purposes

    
    #### Breakdown each hour and find the order total for every hour ####

    
    #VARIABLES#
    
    #hour = {"6AM-7AM": 0, "7AM-8AM" : 0, "8AM-9AM" : 0, "9AM-10AM" : 0, "10AM-11AM" : 0, "11AM-12PM" : 0, "12PM-1PM" : 0, "1PM-2PM" : 0, "2PM-3PM" : 0, "3PM-4PM" : 0, "4PM-5PM" : 0, "5PM-6PM" : 0, "6PM-7PM" : 0, "7PM-8PM" : 0, "8PM-9PM" : 0, "9PM-10PM" : 0, "10PM-11PM" : 0} #UNORDERED DICT

    IP = {}
    hour = OrderedDict([("6AM-7AM",0), ("7AM-8AM",0), ("8AM-9AM",0), ("9AM-10AM",0), ("10AM-11AM",0), ("11AM-12PM",0), ("12PM-1PM",0), ("1PM-2PM",0), ("2PM-3PM",0), ("3PM-4PM" ,0), ("4PM-5PM",0), ("5PM-6PM",0), ("6PM-7PM",0), ("7PM-8PM",0), ("8PM-9PM",0), ("9PM-10PM",0), ("10PM-11PM",0)]) #dictionary to hold the final value
    
    temp = ""
    currentDate = "" #will hold the current date in proper format
    d = "" #temp variable to hold unformatted date
    t1 = "" #temp variable to hold unformatted time (military time)
    time = "" #will hold formatted time

    for i in env.hosts:  # Main for loop to work with each individual server/ip
        temp = hourly[i]
        #print temp
        print red("value of i: %s" % (i))
        IP[i] = []
        tempList = temp.replace("\r\n", "").split(">") #seperates the strings from the list and removes carriage returns/new lines
        
        for z in range(len(tempList)-1):  ## this loop breaks down each individual line for processing and tallying
            #print "WHOA: %s" % (tempList[z]) #testing purposes
            d = tempList[z][0:10].split("-") #gets the current date
            currentDate = d[1] + "-" + d[2] + "-" + d[0] #formats the date
            t1 = tempList[z][11:19].split(":",3) #gets the current time
            
            for x in range(24):  ### this loop matches the time to add to the counter of how many times that name appeared

                if int(t1[0]) == x:
                    #print "Found a match! %s = %s" % (int(t1[0]), x)
                    
                    if int(t1[0]) > 12:
                        f = int(t1[0]) - 12
                        coolString = str(f) + "PM-" + str(f+1) + "PM"
                        hour[coolString] = hour[coolString] + 1

                    elif int(t1[0]) == 12:
                        f = int(t1[0])
                        coolString = str(f) + "PM-" + str(f-11) + "PM"
                        hour[coolString] = hour[coolString] + 1

                    else:
                        f = int(t1[0])
                        if f+1 == 12:
                            coolString = str(f) + "AM-" + str(f+1) + "PM"
                            hour[coolString] = hour[coolString] + 1
                        else:
                            coolString = str(f) + "AM-" + str(f+1) + "AM"
                            hour[coolString] = hour[coolString] + 1
        
           # print convertTime(t1) #converts the time list into a formatted string
           # print "Value of t1: %s" % (t1)
           # print currentDate
           # print z
        IP[i].append(hour.items())
        print blue("IP: %s ---- %s" % (i, IP[i][0]))
        hour = hour.fromkeys(hour,0) # clears the dictionary to prevent spilling of data into a different web server 
        
    print "Final count: %s" % (hour)
    
    #### Tally up all the web orders using the list that is pulled from results[] #####
    finalSum =[0]
    for i in env.hosts:
        #print results[i] # strictly for debugging purposes
        finalSum[0] = int(results[i]) + finalSum[0]
        #print finalSum[0] #for testing purposes
    
    #### Timestamp setup ####
    format = "%a %b %d %I:%M:%S %p %Y"
    today = datetime.datetime.today()
    t = today.strftime(format)
    
    #### Setting up mail settings ####
    s = "cas.crownawards.com"
    sender = 'crownit@crownawards.com'
    receivers = ['spetrina@crownawards.com', 'jquintanilla@crownawards.com']
    #receivers = ['jquintanilla@crownawards.com', 'jquintanilla@crownawards.com'] #for testing purposes
    subject = "Total web order count and average per server"
    text = "The total web order count is: %s" % (finalSum[0])
    text2 = "Command was run on %s" % (t)

    #### Constructing the HTML/plain-text message ####
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(receivers)
    tag = """
    <html>
    <head></head>
    <body>
    <p> %s </p>
    <p> %s </p>
    <br />
    """ % (text, text2) 
    ht = [""]
    print "VALUE OF: %s" % (env.hosts)
    for ii in env.hosts:
        print ii

        en = [0] #variabl to hold per web server total
        for x in IP[ii]: ##CALCULATES TOTAL PER WEB SERVER
            for z in x: ##
                en[0] = en[0] + z[1]##

        ht[0] = ht[0] + """
        <hr> %s -- Total = %s </hr>
        <br />
        """ % (ii, en[0])
        for x in IP[ii]:
            for z in x:
                ht[0] = ht[0] + """\
                <p> %s -- %s </p>
                """ % (z[0], z[1])
    print "VALUE OF HT[0]: %s" % (ht[0])
    last = """\
    </body>
    </html>
    """
    html = tag + ht[0] + last
    
    #html = """\
    #<html>
    #  <head></head>
    #  <body>
    #    <p> %s </p>
    #    <p> %s </p>
    #    <br />
    #    <hr> 
    #  </body>
    #</html>
    #""" % (text, text2)

    
    part1 = MIMEText(text + " " + text2, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    #### Send the email message with a generic exception ####
    try:
        server = smtplib.SMTP(s)
        server.sendmail(sender, receivers, msg.as_string())
        print yellow("Email successfully sent!")
    except Exception:
        ##Might need to add better exception handling##
        print "Error: unable to send"
        server.quit()
    
