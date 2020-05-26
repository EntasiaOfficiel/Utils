var pToN = [] // Port -> nom
var clients = [] // Nom -> données

var responses = []

var logined = []
var vanishs = []

for(i=0;i<10;i++)console.log("\n")

function nameorport(s){
	if(pToN[s.remotePort])return pToN[s.remotePort]
	else return "port:"+s.remotePort

}

function getId(){return Math.ceil(Math.random()*900)+99}

require('net').createServer(function (socket) {
	
	console.log("nouveau client sur le port "+socket.remotePort)

	socket.on('data', async function (data) {
		let m = data.toString()
		if(m.charCodeAt(m.length-2) == 13)m = m.substring(0, m.length-2) // AU CAS OU , NORMALEMENT INUTILE
		else m=m.substring(0, m.length-1) // LUI IL EST UTILE
		let s = m.substring(0,3)
		if(!Number(s)||m.length<4){
			console.log("Paquet invalide recu de "+pToN[socket.remotePort])
			console.log("Paquet : "+m)
			return
		}

		if(responses[s]){ // requête réponse demandée par le socket
			responses[s](m) // on envoi aussi l'ID dans la fonction !!
			delete responses[s]
		}else{
			let arg = m.substring(3).split(" ")
			
			let ret = handleRequest(socket, s, arg)
			if(typeof ret != 'undefined'){
				if(ret=="_x")console.log("Le client "+nameorport(socket)+" a envoyé un paquet inexistant.\nPaquet : "+m)
				else socket.write(s+ret+"\n")
			}
		}
	})
	

	socket.on('end', function (){
		console.log("Client "+nameorport(socket)+" déconnecté")
		disconnect(socket)
	})
	

	socket.on('error', function (e) {
		console.log("Client "+nameorport(socket)+" déconnecté par erreur : "+e.message)
		disconnect(socket)
	})



}).listen(23461, "127.0.0.1", () => {
	console.log('Serveur lancé')
})




function disconnect(socket){
	if(pToN[socket.remotePort] == "BungeeCord")logined = []
	delete clients[pToN[socket.remotePort]]
	delete pToN[socket.remotePort]
}




// async function getData(a){
// 	let client = a.shift()
// 	a = a.join(' ')
// 	clsocket = clients[client]
// 	return new Promise(async resolve => {
// 		let i = getId()
// 		clsocket.write(i+a+"\n")
// 		var fonction = (data) => {
// 			let m = data.toString()
// 			if(m.charCodeAt(m.length-2) == 13)m = m.substring(0, m.length-2)
// 			else m = m.substring(0, m.length-1)
// 			let s = m.substring(0,3)
// 			if(!Number(s)){
// 				console.log("paquet invalide en provenance du client "+nameorport(clsocket)+" recu. Contenu du paquet : "+m)
// 			}else if (s==i) {
// 				resolve(m.substring(7))
// 				let index = clsocket._events.data.indexOf(fonction)
// 				clsocket._events.data.splice(index, 1)
// 			}
// 		}
// 		if(typeof clsocket._events.data == "function"){
// 			clsocket._events.data = [clsocket._events.data]
// 		}
// 		clsocket._events.data.push(fonction)
// 	})
// }


function handleRequest(socket, id, arg){
    switch(arg[0]){
		case "BungeeCord":case "Skyblock":case "EntaGames":case "Hub":
			let cl = arg.shift()
			clients[cl].write(id+arg.join(' ')+"\n")
			responses[id] = (rep)=>{
				socket.write(rep)
			}
			return
		case "onlines":
			clients["Hub"].write(id+"onlines "+pToN[socket.remotePort]+" "+arg[1]+"\n")
			return
		case "log":
			if(clients[arg[1]]){
				console.log("**Duplicate de connexion recue pour le client "+arg[1]+" !**")
				console.log("L'ancienne connexion à été fermée pour être remplacée par la première")
				delete pToN[clients[arg[1]].remotePort]
				clients[arg[1]].end()
			}else console.log("Client sur le port "+socket.remotePort+" connecté en tant que "+arg[1])
			clients[arg[1]] = socket
			pToN[socket.remotePort] = arg[1]
			return
        case "login":
			if(logined[arg[1]])console.log("Duplicate de login recu pour le joueur "+arg[1])
			else{
				logined[arg[1]]=true
				clients["BungeeCord"].write(id+"login "+arg[1]+"\n")
			}
			return
		case "logout":
			delete logined[arg[1]]
			return
		case "islogin":
			if(logined[arg[1]])return 1
			else return 0

        case "vanish":
			broadcast(id+"vanish "+arg[1]+" "+arg[2], socket.remotePort)
			if(arg[1]=='1')vanishs[arg[2]] = true
			else delete vanishs[arg[2]]
			return
		case "vanishs":
			let b = ''
			for(let i in vanishs){
				b+=';'+i
			}
			return b.substring(1)
		case "isvanish":
			if(vanishs[arg[1]])return 1
			else return 0
		default:
			return "_x"
    }
}

function broadcast(request, exclude){
	for(let i in clients){
		if(clients[i].remotePort!=exclude) clients[i].write(request+"\n")
	}
}