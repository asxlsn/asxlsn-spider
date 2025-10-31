const CryptoJS = require('crypto-js')

headers = {}
// window.navigator.appCodeName 没有定义?
// 取属性逻辑 扣对象
// 调式-> 值可以固定
n = "".concat('Mozilla', "_").concat(function () {
    for (var e = [], t = 0; t < 32; t++)
        e[t] = "0123456789abcdef".substr(Math.floor(16 * Math.random()), 1);
    return e.join("")
}())
// get 获取
t = 0
a = (new Date).getTime() + t

var r = function (e) {
    var i = n[0]
        , s = "ojts"
        , o = "CipherKey5"
        , l = n[1]
        , u = {}
        ,
        c = ["12345678901234567890123456789012", "qwefqwefqwefqwefqwefqwefqwefqwef", "QWDSQWDSQWDSQWDSQWDSQWDSQWDSQWDS", "12345678901234567890123456789012", "qwefqwefqwefqwefqwefqwefqwefqwef", "QWDSQWDSQWDSQWDSQWDSQWDSQWDSQWDS"]
        , d = "".concat(i, "_").concat(c[e])
        , p = CryptoJS.MD5("".concat(s).concat(o)).toString().substring(8, 24)
        , m = CryptoJS.enc.Utf8.parse(CryptoJS.MD5("".concat(s).concat(o)).toString().substring(8, 24));
    u["Crypto-Chars"] = e <= 2 ? CryptoJS.AES.encrypt("".concat(d, "_").concat(l), m, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    }).toString() : CryptoJS.MD5("".concat(d, "_").concat(l, "_").concat(p)).toString();
    var f = CryptoJS.enc.Utf8.parse(CryptoJS.MD5(s).toString().substring(8, 24));
    return u["Crypto-Random"] = CryptoJS.AES.encrypt("".concat(d), f, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    }).ciphertext.toString(CryptoJS.enc.Base64),
        u
}(Math.abs(a % 6), a, n);

headers['Device-Id'] = n
headers['Crypto-Chars'] = r['Crypto-Chars']
headers['Crypto-Random'] = r['Crypto-Random']
console.log(headers)