const cryptoJs = require('crypto-js');

function getToken(){
    var time = (new Date).getTime()
    n = "Uu0KfOB8iUP69d3c:".concat(time);
    token = cryptoJs.MD5(n).toString()
    return {
        token: token,
        time: time
    }
}

console.log(getToken())


