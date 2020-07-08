#!/usr/bin/env python3.8

from functions import *

if len(sys.argv) == 1: 
	print("Met un nom de serveur")
else:
	serv = find_server(sys.argv[1])
	if serv != None:
		if len(sys.argv) == 2: 
			print("Met un argument !")
		else:
			if check_access(serv) == True:
				sys.argv[2] = sys.argv[2].lower()
				if sys.argv[2] == "start":
					start_server(serv)
					
				elif sys.argv[2] == "stop":
					stop_server(serv)

				elif sys.argv[2] == "kill":
					proc = get_proc(serv, True)
					if proc != None:
						proc.children()[0].kill()
						proc.kill()
						print("Serveur `"+serv.name+"` tué ! (pas bien ca)")

				elif sys.argv[2] == "cmd":
					if len(sys.argv) < 4:
						print("Met une commande !")
					else:
						if get_proc(serv, True) != None:
							targs = sys.argv
							del sys.argv[0:3]
							targs = " ".join(targs)
							if execute_cmd_mc(serv, targs):
								print("Commande `"+targs+"` executée sur "+serv.name)
				elif sys.argv[2] == "stats":
						proc = get_proc(serv, True)
						if proc != None:
							print_info(serv, proc)

				elif sys.argv[2] == "save":
					save_server(serv)
						
				else:
					print("Commande inconnue !")
