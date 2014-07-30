#! /usr/bin/env python

# testbot v0.1a
# Author: Alexsei
# Description: tetsing connections to IRC server and channels and some automation
#	template was derived from http://wiki.shellium.org/w/Writing_an_IRC_bot_in_Python

#lib sauce
import socket
import time

# basic config variables for bot
server = "irc.freenode.net"
port = 6667
channel = "#thisbot"
botnick = "thisbot"
connected = False
quitFlag = False
inCoinPrice = False

# Commands for additional bot function
def commands(nick,channel,message):
	if message.find('!tits') != -1:
		if 'QuarkieFM' in nick:
			ircsock.send('PRIVMSG %s :%s:  ( o Y o )    ( o Y o )   ( o Y o )\r\n' % (channel, nick)) # lulz
		else:
			ircsock.send('PRIVMSG %s :%s: As you wish.. ( o Y o )\r\n' % (channel, nick)) # lets see dem tattiess
			ircsock.send('PRIVMSG %s :%s: Had enough?\r\n' % (channel, nick)) # nope. nehvaar.

	elif message.find('!help') != -1:
		ircsock.send('PRIVMSG %s :%s: Hi, I\047m version 0.1a. One of my commands is !tits.\r\n' % (channel, nick)) # . . . - - - . . .
	elif message.find('!joinus') != -1 and 'thisuser' in nick:
		joinchan(str('\043\043coinprice'))
	elif message.find('!leaveus') != -1 and 'thisuser' in nick:
		partchan(str('\043\043coinprice'))
	elif message.find('!playtime') != -1 and 'thisuser' in nick:
			playtime()
	elif message.find(botnick+': !die') != -1 and 'thisuser' in nick:
			ircsock.send('PRIVMSG %s : It has been a pleasure serving you, Bro. May my next iteration serve you more than I was capable of.\r\n' % (channel,))
			disconnect('This bot served well. See you in the next iteration.')


def disconnect(mess):
#	if not connected:
#		return
	
#	connected = Flase
	
	quit(mess) # okay baaiiiiii ^_^
	
	quitFlag = True # get me outta here! -untrap flag

def quit(message): # send IRC quit to server with message if supplied
	ircsock.send('QUIT :%s\n' % (message,))

def ping(): # responds to server pings
	ircsock.send("PONG :Pong\n")

def sendmsg(chan, msg): # send message function, sends to channel
	ircsock.send("PRIVMSG %s :%s\r\n" % (chan, msg,))

def joinchan(chan): # join channel
	ircsock.send('JOIN %s\n' % (chan,))

def partchan(chan): # leave a channel :'( waaaah
	ircsock.send('PART %s\n' % (chan,))

def hello(): # function to reply to "Hello thisbot"
	ircsock.send("PRIVMSG %s :Hellow!\n" % (channel))

def playtime(): # all work and no play makes Alexsei a dull boy
	playChan = str('\043\043coinprice')
	if not inCoinPrice: # join if not already in there
		joinchan(playChan)
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

ircsock.send("USER %s %s %s :This bot is part of a students assignment \n" % (botnick, botnick, botnick,)) # how are you gentlemen?
ircsock.send("NICK %s\n" % (botnick,)) # all your base are belong to us
ircsock.send('PRIVMSG NickServ : IDENTIFY thisuser popweee\r\n') # cloak my ip ktks

time.sleep(5) # this delay is to allow host/ip cloaking to take effect before joining channels

joinchan(channel) # lets party in #thisbot

while 1: # oh shit. beware runaway processes in the infinite
	ircmsg = ircsock.recv(2048) # need input. water in the wheel. make me rotate.
	ircmsg = ircmsg.strip('\n\r') # take off those wretched rags, please
	print(ircmsg) # spread em!

	if ircmsg.find(' PRIVMSG ') != -1: # process the msg before sending elements to commands sub-routine
		nick = ircmsg.split('!')[0][1:] # whas yo name, son?
		channel = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0] # where do you ya hail from, boy?
		commands(nick,channel,ircmsg) # well, get to it, boy!

	if quitFlag != False:
		break

	if ircmsg.find(":Hello %s" % (botnick,)) != -1: # if someone says hello one more mothuh fucking time...
		hello() # mothuh fuckuh! kos e zanat

	if ircmsg.find("PING :") != -1: # the chinese play the best...
		ping() # PONG kosketsh

try:
	ircsock.shutdown(socket.SHUT_WR)
	ircsock.close()
except socket.error:
	pass
del ircsock

exit()
