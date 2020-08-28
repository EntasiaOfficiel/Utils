const JsSHA = require('jssha')
const crypto = require('crypto')
const pass = require("./pass")

function signMsg(msg, hexSalt){
    if(!hexSalt){
        hexSalt = crypto.randomBytes(16).toString('hex')
    }

    let digest = new JsSHA("SHA-256", "TEXT", { encoding: "UTF8" })

    digest.update(pass.secret)
    digest.update(hexSalt)
    digest.update(msg)
    
    let hash = digest.getHash("B64")
    return hash+";"+hexSalt
}

function verifyMsg(msg, signature){
    console.log("--")
    console.log("MSG="+msg)
    console.log("SIGNATURE="+signature)
    let list = signature.split(";")
    return signature==signMsg(msg, list[1])
}


// let msg = "log paper2"
// let signature = signMsg(msg)
// if(verifyMsg(msg, "Nbdf3X2qZb271kvHjBR/JKjN/rFS6hOyIZ+XoVDXvow=;60BA7BD825698697865C06FD940253E7")){
//     console.log("vérifié")
// }else console.log("invalidé")


module.exports = {signMsg, verifyMsg }