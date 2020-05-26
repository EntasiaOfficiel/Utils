#!/usr/bin/env python3.8

import sys, os, json, tarfile
import psutil
import pwd
import subprocess
import shlex
import threading
import time
import collections
import grp

users = {}

def getUser(name):
	if name in users:
		return users[name]
	else:
		a = User(name)
		users[name] = a
		return a

class User:

	def __init__(self, n):
		self.name = n
		pw = pwd.getpwnam(n)
		self.uid = pw[2]
		self.gid = pw[3]
		self.groups = [self.gid]
		for i in [g.gr_gid for g in grp.getgrall() if n in g.gr_mem]:
			self.groups.append(i)

class Server:

	def __init__(self, n):
		if n in servers:
			self.name = n
			self.data = get_data(n)
			self.owner=getUser(self.data["owner"])
		else:
			print("INTERNAL : Serveur non existant demandé ! "+n)
			sys.exit(1)

mcpath = "/Entasia/minecraft"

servers = []
noacess = []
for i in os.listdir(mcpath+"/servers"):
	if os.path.exists(f"{mcpath}/servers/{i}/server.json"):
		servers.append(i)
	else:
		noacess.append(i)


def check_access(serv):
	euid = os.geteuid()
	if euid != os.getuid():
		print("Accès non autorisé : euid/uid différents")
		return False
	elif euid == 0:
		return True
	elif euid == serv.owner.uid and os.getgroups() == serv.owner.groups:
		return True
	else:
		print("Accès non autorisé avec `"+os.getlogin()+"` !")
		return False

def find_server(name):
	name = name.lower()
	t = None
	for i in servers+noacess:
		if i.lower() == name:
			return Server(i)
		elif i.lower().startswith(name):
			if t == None:
				t = i
			else:
				t = "_"
	if t == None:
		print("Serveur `"+name+"` non trouvé !")
	elif t == "_":
		print("Plus d'un serveur correspond à `"+name+"` !")
	elif t in noacess:
		print("Tu n'as pas accès au serveur `"+t+"` !")
	else:
		return Server(t)
	return None


def get_data(serv):
	return json.load(open(f"{mcpath}/servers/{serv}/server.json", "r"))

def update(serv):
	clear_logs(serv)
	set_perms(serv)

def clear_logs(serv):
	if os.path.exists(mcpath+"/servers/"+serv.name+"/logs"):
		for file in os.listdir(mcpath+"/servers/"+serv.name+"/logs"):
			if file.endswith(".log.gz"):
				l = time.time() - os.path.getmtime(mcpath+"/servers/"+serv.name+"/logs/"+file)
				if l > 604800: # 60*60*24*7 = 604800
					os.remove(mcpath+"/servers/"+serv.name+"/logs/"+file)

def set_perms(serv):
	if os.getuid() == 0:
		os.chdir(mcpath+"/servers")
		os.system(f"chmod -R 770 {serv.name}")
		os.system(f"chown -R {serv.data['owner']}:{serv.data['owner']} {serv.name}")

def start_server(serv):
	if get_proc(serv, False) == None:
		update(serv)
		os.chdir(mcpath+"/servers/"+serv.name)
		execute_cmd_term(serv.owner, f"screen -dmS {serv.name} java -Xms{serv.data['ram_default']}m -Xmx{serv.data['ram_max']}m -jar {mcpath}/jars/{serv.data['profile']}.jar")
		print("Serveur "+serv.name+" démarré")
	else:
		print("Le serveur "+serv.name+" est déja démarré !")

def stop_server(serv):
	if get_proc(serv, False) == None:
		print("Le serveur "+serv.name+" est déja éteint !")
	else:
		if "bungee" in serv.data and serv.data['bungee'] == True:
			execute_cmd_mc(serv, "end")
		else:
			execute_cmd_mc(serv, "stop")

		print("Serveur "+serv.name+" éteint")

def save_server(serv):
	if not os.path.isdir(f"{mcpath}/saves"):
		os.mkdir(f"{mcpath}/saves")
	if not os.path.isdir(f"{mcpath}/saves/{serv.name}"):
		os.mkdir(f"{mcpath}/saves/{serv.name}")
	t = time.strftime("%Y-%m-%d_%H-%M-%S")+"-"+serv.name+".tar.gz"
	print("Sauvegarde du serveur `"+serv.name+"`, en cours, enregistrement sous "+t)
	proc = get_proc(serv, False)
	if proc != None:
		execute_cmd_mc(serv, "save-off")
	os.chdir(mcpath+"/servers")
	file = tarfile.open(f"{mcpath}/saves/{serv.name}/{t}", "w:gz")
	file.add(serv.name)
	file.close()
	if proc != None:
		execute_cmd_mc(serv, "save-on")
		execute_cmd_mc(serv, "save-all")
	print("Fin de sauvegarde du serveur `"+serv.name+"`, enregistré sous "+t)

def execute_cmd_mc(serv, cmd):
	if "'" in cmd or '"' in cmd:
		print("Les caractères \" et ' ne sont pas supportés dans les commandes !")
		return False
	else:
		execute_cmd_term(serv.owner, f"""screen -S {serv.name} -p 0 -X eval 'stuff "{cmd}\n" '""")
		# execute_cmd_term(serv.owner, "id")
		return True

def _demote(owner):
	def _dem():
		if os.getuid() == 0:
			os.setgroups(owner.groups)
		os.setgid(owner.gid)
		os.setuid(owner.uid)
	return _dem

def execute_cmd_term(owner, cmd):
	subprocess.check_call(shlex.split(cmd), preexec_fn=_demote(owner))
	return True

def get_proc(serv, msg):
	for proc in psutil.process_iter():
		a = proc.cmdline()
		if(len(a)>2) and (proc.username() == serv.owner.name) and (a[0].lower() == "screen") and (a[2] == serv.name):
				return proc
	if msg:
		print("Le serveur "+serv.name+" est éteint !")
	return None

def print_info(serv, proc):
	child = proc.children()[0]
	print("Serveur : "+serv.name)
	print("Owner : "+proc.username())
	print("PID screen : "+str(proc.pid))
	print("PID java : "+str(child.pid))
	b = child.memory_full_info()
	print("RAM config : "+str(serv.data["ram_default"])+"Mo default | "+str(serv.data["ram_max"])+"Mo max")
	print("RAM (Mo) : "+str(round(b.uss/1000000, 1))+" USS | "+str(round(b.rss/1000000, 1))+" RSS")
	print("RAM percent (RSS) : "+str(round(child.memory_percent(memtype="rss"), 1))+"% total | "+
	str(round(b.rss/(serv.data["ram_default"]*10000), 1))+"% default | "+str(round(b.rss/(serv.data["ram_max"]*10000), 1))+"% max")
