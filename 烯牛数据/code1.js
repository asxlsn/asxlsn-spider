const CryptoJS = require("crypto-js");
// 固定密钥
const _p = "W5D80NFZHAYB8EUI2T649RT2MNRMVE2O";
const _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";



// Base64 编码
function base64Encode(e) {
    let c = "";
    let o, i, a, u;
    let l = 0;

    while (l < e.length) {
        o = e.charCodeAt(l++) >> 2;
        i = (3 & e.charCodeAt(l - 1)) << 4 | (e.charCodeAt(l) >> 4);
        a = (15 & e.charCodeAt(l++)) << 2 | (e.charCodeAt(l) >> 6);
        u = 63 & e.charCodeAt(l++);
        if (isNaN(e.charCodeAt(l - 2))) {
            a = u = 64;
        } else if (isNaN(e.charCodeAt(l - 1))) {
            u = 64;
        }
        c += _keyStr.charAt(o) + _keyStr.charAt(i) + _keyStr.charAt(a) + _keyStr.charAt(u);
    }
    return c;
}

// 异或加密
function xorEncrypt(data) {
    let t = "";
    for (let n = 0; n < data.length; n++) {
        let r = _p.charCodeAt(n % _p.length);
        t += String.fromCharCode(data.charCodeAt(n) ^ r);
    }
    return t;
}

// 加密主函数
function encryptPayload(payloadObj) {
    const jsonStr = JSON.stringify(payloadObj); // JSON字符串
    const xorEncrypted = xorEncrypt(jsonStr);   // 异或加密
    return base64Encode(xorEncrypted);          // Base64 编码
}

function getSig(f) {
    return CryptoJS.MD5(f + _p).toString().toUpperCase();
}
// 示例
const payload = {
        "sort": 1,
        //todo start 数量变化
        "start": 20,
        "limit": 20
    }






function get_params(f) {
    let f_payload = encryptPayload(payload);
    let p = getSig(f_payload);
    return {
        payload: f_payload,
        sig: p
    };
}


// 签名函数


// 示例


console.log(get_params(payload));


