#! /usr/bin/env python

# testbot v0.2.3a
# Author: Alexsei
# Description: tetsing connections to IRC server and channels and some automation
#	template was derived from http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python
version = str("0.2.3a")
print("testbot v"+version)
#lib sauce
import socket
from time import sleep
import perchange
from operator import itemgetter

# basic config variables for bot
server = "irc.freenode.net"
port = 6667
startchannel = "##coinprice"
botnick = "thisbot"
connected = False
quitFlag = False
permissions = [] # level 0 - admin, level 1 - mod, level 2 - user(authed), level 3 - guest
permissions.append({ "Handle" : 'thisuser!~thisuser@unaffiliated/thisuser', "Level" : 0 })

def isOp(handle):
	print("Debug isOp check")
	if permissions.count({ "Handle" : str(handle), "Level" : 0}) == 1:
		print("Debug isOp check PASS")
		return True
	else:
		print("Debug isOp check FAIL")
		return False

# prepmsg()
# function takes in a string and encodes into Type.Bytes for python3 socket send
def prepmsg(s):
	return bytes(s, 'UTF-8')

# Mode Action behaviours
def modeAction(nick,handle,channel,mode,moded,message,botnick):
# for debugging MODE msg behaviour uncomment the following line
#	print "{0} {1} {2} {3} {4}".format(nick, channel, mode, moded, botnick)
	if mode == "+o" and moded == botnick: # thank you for Op msg
		sendmsg(channel,"{0}: Thank you, my meatbag-brother!".format(nick))

# Commands for additional bot function
def commands(nick,handle,channel,message,botnick): 
	if message.find('!tits') != -1:
		tits(channel,nick)
	elif message.find('!bigmovers') != -1:
		sendmsgfp(channel,perchange.topmarkchange(perchange.testAPI))
	elif message.find('!price') != -1:
		sendmsgfp(channel,perchange.getmarketticker(perchange.testAPI, message.split('!price')[1][1:]))
	elif message.find('!vol') != -1:
		if message.split('!vol')[1][1:] != "":
			sendmsgfp(channel,perchange.getmarketvolume(perchange.testAPI, message.split('!vol')[1][1:]))
	elif message.find('!help') != -1:
		help(channel,nick)
	elif message.find('!handle') != -1:
		sayhandle(channel,handle)
	elif message.find('!join') != -1 and isOp(handle):
		joinchan(message.split('!join')[1][1:])
	elif message.find('!leave') != -1 and isOp(handle):
		partchan(message.split('!leave')[1][1:])
	elif message.find('!newnick') != -1 and isOp(handle):
		nickchange(message.split('!newnick')[1][1:])
	elif message.find('!yo') != -1 and isOp(handle):
		ircsock.send(prepmsg('MODE %s +o %s \r\n' % (channel, nick,)))
	elif message.find('!playtime') != -1 and isOp(handle):
		playtime()
	elif message.find('!die') != -1 and isOp(handle):
		ircsock.send(prepmsg('PRIVMSG %s : It has been a pleasure serving you, Bro. May my next iteration serve you more than I was capable of.\r\n' % (channel,)))
		sleep(2)
		return disconnect('This bot served well. See you in the next iteration.')

def tits(channel,nick):
	if 'QuarkieFM' in nick:
		ircsock.send(prepmsg('PRIVMSG %s :%s:  ( o Y o )    ( o Y o )   ( o Y o )\r\n' % (channel, nick))) # lulz
	else:
		ircsock.send(prepmsg('PRIVMSG %s :%s: As you wish.. ( o Y o )\r\n' % (channel, nick))) # lets see dem tattiess
		ircsock.send(prepmsg('PRIVMSG %s :%s: Had enough?\r\n' % (channel, nick))) # nope. nehvaar.

def help(channel,nick):
	ircsock.send(prepmsg('PRIVMSG %s :%s: Wuff!Wuff! I\047m version %s.  My commands are !price <market>, !vol <market>, !bigmovers, !tits, !help.\r\n' % (channel, nick, version))) # . . . - - - . . .
	
def sayhandle(channel,handle):
	sendmsg(channel,handle)

def disconnect(mess):
	quit(mess) # okay baaiiiiii ^_^
	return True # notify command checker to set quitFlag to exit program

# BUG: quit message not sending to server, only quit command
def quit(quitmessage): # send IRC quit to server with message if supplied
	ircsock.send(prepmsg('QUIT {!s}\n'.format(quitmessage))) # format(quitmessage)

def ping(): # responds to server pings
	ircsock.send(prepmsg('PONG :Pong\n'))

def sendmsg(chan, msg): # send message function, sends to channel
	ircsock.send(prepmsg('PRIVMSG %s :%s\r\n' % (chan, msg,)))

def nickchange(newnick):
	ircsock.send(prepmsg('NICK %s\n' % (newnick,)))

# Function
# sendmsgfp(chan, buffer)
# send message with flood protectection
def sendmsgfp(chan,buffer):
	for line in buffer:
		sendmsg(chan, line)
		sleep(1)

		
def joinchan(chan): # join channel
	ircsock.send(prepmsg('JOIN %s\n' % (chan,)))

def partchan(chan): # leave a channel :'( waaaah
	ircsock.send(prepmsg('PART %s\n' % (chan,)))

def hello(): # function to reply to "Hello thisbot"
	ircsock.send(prepmsg("PRIVMSG %s :Hellow!\n" % (channel)))

def playtime(): # all work and no play makes Alexsei a dull boy
	playChan = channel
	time.sleep(2)
	sendmsg(playChan,'How are you gentlemen?')
	time.sleep(3)
	sendmsg(playChan,'All your base are belong to us!')
	time.sleep(2)
	sendmsg(playChan,'Make your time.')
	time.sleep(0.5)
	sendmsg(playChan,'Hahahaha')


try: # catch errors yo
# lets hookup!.. I mean to a server. Pervert.
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #pull up you sock-ets
	ircsock.connect((server, port))  # we get signal
except socket.error:
	die('No Socket, Bro!')
connected = True

ircsock.send(prepmsg('USER {!s} {!s} {!s} :This bot is part of a students assignment \n'.format(botnick, botnick, botnick,))) # how are you gentlemen?
ircsock.send(prepmsg("NICK %s\n" % (botnick,))) # all your base are belong to us
ircsock.send(prepmsg('PRIVMSG NickServ :IDENTIFY thisuser popweee\r\n')) # cloak my ip ktks

sleep(15) # this delay is to allow host/ip cloaking to take effect before joining channels

joinchan(startchannel) # lets party in assigned channel space!

while not quitFlag: # oh shit. beware runaway processes in the infinite

	ircmsg = ircsock.recv(2048).decode('utf-8') # need input. water in the wheel. make me rotate.
	ircmsg = ircmsg.strip('\n\r') # take off those wretched rags, please
	print(ircmsg) # spread em!

	if ircmsg.find(":Wuff! Hello %s" % (botnick,)) != -1: # if someone says hello one more mothuh fucking time...
		hello() # mothuh fuckuh! kos e zanat

	if ircmsg.find("PING :") != -1: # the chinese play the best...
		ping() # PONG kosketsh

	if ircmsg.find(' MODE ') != -1: # check for modes relavent to the bot and send to modeAction
		nick = ircmsg.split('!')[0][1:] 
		channel = ircmsg.split(' MODE ')[1].split(" ")[0] 
		handle = ircmsg.split(' MODE ')[0][1:] 
		mode = ircmsg.split(' MODE ')[1].split(" ")[1]
		try: 
			moded = ircmsg.split(' MODE ')[1].split(" ")[2] 
		except:
			moded = "None"
		modeAction(nick,handle,channel,mode,moded,ircmsg,botnick)

	if ircmsg.find(' PRIVMSG ') != -1: # process the msg before sending elements to commands sub-routine
		nick = ircmsg.split('!')[0][1:] # whas yo name, son?
		channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0] # where do you ya hail from, boy?
		handle = ircmsg.split(' PRIVMSG ')[0][1:] # get a grip, son!
		if commands(nick,handle,channel,ircmsg,botnick): # well, get to it, boy!
			quitFlag = True

	if quitFlag != False:
		try:
			ircsock.shutdown(socket.SHUT_WR)
			ircsock.close()
		except socket.error:
			pass

del ircsock
print("DEBUG: Shutting Down")
exit()
