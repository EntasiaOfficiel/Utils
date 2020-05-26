#!/usr/bin/env python3.8

from functions import *

def sendmsg(msg):
	execute_cmd_mc(Server("BungeeCord"), "alert "+msg)

if len(sys.argv) == 2:
	if sys.argv[1] == "M-32":
		sendmsg("&6Les serveurs vont redémarrer dans &330 minutes&6 ! &3( 2h30 )")
	elif sys.argv[1] == "M-7":
		sendmsg("&c&lATTENTION : &6Les serveurs vont redémarrer dans &35 minutes&6 ! &3( 2h30 )")
	elif sys.argv[1] == "M-2":
		sendmsg("&c&lATTENTION : Arret des serveurs MAINTENANT")
		for i in servers:
			stop_server(Server(i))
	elif sys.argv[1] == "M":
		os.system("/sbin/reboot")
	else:
		print("INCORECT ARGUMENT")

else:
	print("INCORRECT SYNTAX")
