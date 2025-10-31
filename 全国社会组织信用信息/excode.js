const JSEncrypt = require('node-jsencrypt');

let h = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
function getRsaCode(t) {
    var e = new JSEncrypt;
    return e.setPublicKey("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCCsYUGHMhjSzdMqn9JzPfKs9JbxXTPtHofTv7reV0HrEz4brnE6ZJpNn5s934KO3L4QDF7ELHysIiounhhpF1bewW9jKdcpZA5M1CkGHKcwpLA2liaqOlt/0Mf3ui9jxR9AHxUMFVGfJ6Q4+cEmDBUAEOXlxqk4ZjGpubwGNk9XQIDAQAB"),
        e.encrypt(t.toString())
}


encodedata = function (t) {
    var a, i, e, s, n, l = "", c = "", o = "", r = 0;
    do {
        e = (a = t.charCodeAt(r++)) >> 2,
            s = (3 & a) << 4 | (i = t.charCodeAt(r++)) >> 4,
            n = (15 & i) << 2 | (c = t.charCodeAt(r++)) >> 6,
            o = 63 & c,
            isNaN(i) ? n = o = 64 : isNaN(c) && (o = 64),
            l = l + h.charAt(e) + h.charAt(s) + h.charAt(n) + h.charAt(o),
            a = i = c = "",
            e = s = n = o = ""
    } while (r < t.length);
    return l
}

getParams = function (avalve,bvblve,movex) {
    a= getRsaCode(parseInt(movex)+ "");
    i = {
        a : encodedata(avalve),
        b : encodedata(bvblve),
        c : encodedata(a)
    }
    return i;
}

console.log(getParams("1","2",56))