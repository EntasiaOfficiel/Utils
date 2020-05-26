#!/usr/bin/env python3.8

from functions import *

if len(sys.argv) < 2: 
	print("Met un argument")
else:
	sys.argv[1] = sys.argv[1].lower()
	if sys.argv[1] == "update":
		for i in servers:
			update(Server(i))
		print("Serveurs mis à jour")

	elif sys.argv[1] == "list":
		print("Liste des serveurs :")
		for i in servers:
			print("- "+i)

	elif sys.argv[1] == "stats":
		print("Statistiques des serveurs :")
		L = []
		for proc in psutil.process_iter():
			a = proc.cmdline()
			if (len(a)>2):
				if (a[0].lower() == "screen") and (a[2] in servers):
					print("----------")
					print_info(Server(a[2]), proc)
					L.append(a[2])
		print("----------")
		for i in servers:
			if not i in L:
				print("Le serveur "+i+" est éteint")

	elif sys.argv[1] == "startall" or sys.argv[1] == "start":
		for i in servers:
			serv = Server(i)
			if serv.data["autorestart"] == True:
				start_server(serv)

	elif sys.argv[1] == "stopall" or sys.argv[1] == "stop":
		for i in servers:
			stop_server(Server(i))

	elif sys.argv[1] == "saveall" or sys.argv[1] == "save":
		for i in servers:
			serv = Server(i)
			if "autosave" in serv.data and serv.data["autosave"] == True:
				save_server(serv)
			else:
				print("Skip du serveur "+serv.name+" : option `autosave` non activée")
			print(" ")
	# elif sys.argv[1] == "autosave":
	# 	auto_save_servers()
	else:
		print("Commande inconnue !")
