const net = require('net')
var socket
function connect(){
	socket = net.createConnection({ port: 5000, host: 'localhost' })
	socket.on('error', e => {
		if(e.message == "read ECONNRESET"){
			console.log("déconnecté du serveur !")
		}else if(e.message == "connect ECONNREFUSED 127.0.0.1:5000"){
			console.log("Connexion au serveur refusée !")
		}else throw e
		console.log("Tentative de reconnexion dans 5 secondes ..\n")
		setTimeout(() => {
			console.log("Tentative de reconnexion")
			connect()

		}, 10)
	})

	socket.on('end', () => {
		console.log("Le serveur nous à kické !")
		throw new Error("Server kicked us")
	})

	socket.on('connect', () => {
		console.log("Connecté au serveur !")
		socket.write(getId()+"socket log BungeeCord\n")
	})
	socket.on('data', data => {
		let m = data.toString()
		if(m.charCodeAt(m.length-2) == 13)m = m.substring(0, m.length-2)
		else m = m.substring(0, m.length-1)
		let s = m.substring(0,3)
		if(!Number(s)){
			console.log("paquet invalide en provenance du serveur recu. Contenu du paquet : "+m)
		}
		let arg = m.substring(3).split(" ")
		if(arg[0] == "rep")return
		switch(arg[0]){
			case "onlineplayers":
				socket.write(s+"rep iTrooz_, Stargeyt et Shame\n")
				break

		}
	})

	
}

connect()

function getId(){return Math.ceil(Math.random()*900)+99}

function sendData(a){
	return new Promise(resolve => {
		let i = getId()
		socket.write(i+a+"\n")
		
		// socket.on('data', data =>{
		var fonction = (data) => {
			let m = data.toString()
			if(m.charCodeAt(m.length-2) == 13)m = m.substring(0, m.length-2)
			else m = m.substring(0, m.length-1)
			let s = m.substring(0,3)
			if(!Number(s)){
				console.log("paquet invalide en provenance du serveur recu. Contenu du paquet : "+m)
			}else if (s==i) {
				resolve(m.substring(7))
				let index = socket._events.data.indexOf(fonction)
				socket._events.data.splice(index, 1)
			}
		}
		if(typeof socket._events.data == "function"){
			socket._events.data = [socket._events.data]
		}
		socket._events.data.push(fonction)
		// console.log(typeof socket._events.data)

	})
}


// setInterval(async function(){
// 	// console.log("demande de données")
// 	let d = Date.now()
// 	var a = await sendData("BungeeCord onlineplayers")
// 	// console.log("RESULTAT : "+a)
// 	console.log(Date.now() - d)
// },500)
