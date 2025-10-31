const cryptoJs = require("crypto-js");

function callsign() {
    let e = "nw3b089qrgw9m7b7i"
        t = Number(Date.now().toString().slice(0, 10))
    console.log( t)
    n = "".concat(t, ",").concat(e)
    sign = "".concat(cryptoJs.MD5(n).toString(), ",").concat(t)
    return sign
}

console.log(callsign());

