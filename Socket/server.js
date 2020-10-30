const security = require('./security')
const infos = require("entasia/pass").socket

function tconvert(x){
	if(x.toString().length==1)return "0"+x
	else return x
}
function gettime(x){
	let d = new Date()
	return `[${tconvert(d.getHours())}:${tconvert(d.getMinutes())}:${tconvert(d.getSeconds())}]`
}
function logger(msg, socket, content){
	console.log(gettime()+" "+msg)
	if(socket){
		console.log("Client : "+nameorport(socket.remotePort)+". Contenu : "+content)
	}	
}

var sockData = []

function softGetByName(name){
	let a = getByName(name)
	if(a)return a
	else{
		a = new Object()
		a.sendData = ()=>{}
		return a
	}
}

function getByName(name){
	for(let i in sockData){
		if(sockData[i].name==name)return sockData[i]
	}
}

function nameorport(s){
	if(sockData[s])return sockData[s].name
	else return "port:"+s
}


require('net').createServer(function (socket) {
	
	logger("New client on port "+socket.remotePort)

	socket.sendData = (str)=>{
		let signature = security.signMsg(str)
		let final = signature+" "+str+"\n"
		socket.write(final)
	}

	socket.on('data', function (data) {
		let m = data.toString()
		if(m.charCodeAt(m.length-2) == 13)m = m.substring(0, m.length-2)
		else if(m.charCodeAt(m.length-1) == 10) m=m.substring(0, m.length-1)
		for(let i of m.split("\n")){
			socket.emit('line', i)
		}
	
	})

	socket.on('line', function (msg) {
		let args = msg.split(" ")
		let signature = args.shift()
		logger("Paquet de "+nameorport(socket.remotePort)+" : "+msg)
		if(!security.verifyMsg(args.join(" "), signature)){
			logger("Signature invalide provenant du dernier packet !")
			socket.end()
			return
		}
		
		let type = args.shift()
		if(type=="log"){
			let t = getByName(args[0])
			if(t){
				logger("**Connection dupliquée pour "+args[0]+" !** L'ancienne connection à été terminée")
				delete sockData[t.remotePort]
				t.end()
			}
			logger("Client sur le port "+socket.remotePort+" connecté en tant que "+args[0])
			socket.name = args[0]
			sockData[socket.remotePort] = socket
		}else if(socket.name==undefined)logger("Paquet recu pour un serveur non authentifié !", socket, msg)
		else{
			let t = getByName(type)
			if(t)t.sendData(args.join(' '))
			else{
				switch(type){
					case "onlines":{
						sendOnlineRequest("onlines "+socket.name+" "+args[0])
						return
					}
					case "players":{
						sendOnlineRequest("players "+args.join(" "))
						return
					}
					case "broadcast":{
						return broadcast(args.join(' '), socket.remotePort)
					}
					default:{
						logger("Packet non reconnu (type "+type+")", socket, msg)
						return
					}
				}
			}
		}
	})
	

	socket.on('end', function (){
		logger("Client "+nameorport(socket.remotePort)+" déconnecté")
		socket.emit("off")
	})
	

	socket.on('error', function (e) {
		logger("Client "+nameorport(socket.remotePort)+" déconnecté avec erreur : "+e.message)
		socket.emit("off")
	})
	

	socket.on('off', () => {
		delete sockData[socket.remotePort]
		sendOnlineRequest("onlines "+socket.name+" 0")
	})



}).listen(infos.port, "127.0.0.1", () => {
	logger('Serveur lancé')
})

function sendOnlineRequest(r){
	for(let i of ["Hub", "EBH", "Public"]){
		softGetByName(i).sendData(r)
	}
}

function broadcast(request, exclude){
	logger("Broadcasting "+request)
	for(let i in sockData){
		if(sockData[i].remotePort!=exclude){
			sockData[i].sendData(request)
			logger("broadcasting to "+nameorport(sockData[i].remotePort))
		}
	}
}
