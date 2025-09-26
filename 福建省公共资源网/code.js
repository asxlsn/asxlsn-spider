const CryptoJS = require("crypto-js");


t = {
    "ts": new Date().getTime(),
    "pageNo": 1,
    "pageSize": 20,
    "total": 3268,
    "KIND": "GCJS",
    "GGTYPE": "1",
    "timeType": "6",
    "BeginTime": "2025-03-26 00:00:00",
    "EndTime": "2025-09-26 23:59:59"
}


function l(t, e) {
    return t.toString().toUpperCase() > e.toString().toUpperCase() ? 1 : t.toString().toUpperCase() == e.toString().toUpperCase() ? 0 : -1
}

function u(t) {
    for (var e = Object.keys(t).sort(l), n = "", a = 0; a < e.length; a++)
        if (void 0 !== t[e[a]])
            if (t[e[a]] && t[e[a]]instanceof Object || t[e[a]]instanceof Array) {
                var i = JSON.stringify(t[e[a]]);
                n += e[a] + i
            } else
                n += e[a] + t[e[a]];
    return n
}


function d(t) {
    for (var e in t)
        "" !== t[e] && void 0 !== t[e] || delete t[e];
    var n = 'B3978D054A72A7002063637CCDF6B2E5' + u(t);
    return CryptoJS.MD5(n).toString().toLowerCase()

}

function b(data) {
    var e = CryptoJS.enc.Utf8.parse('EB444973714E4A40876CE66BE45D5930')
      , n = CryptoJS.enc.Utf8.parse('B5A8904209931867')
      , a = CryptoJS.AES.decrypt(data, e, {
        iv: n,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return a.toString(CryptoJS.enc.Utf8)
}



console.log(d(t));
