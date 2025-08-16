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

function _u_d(e) {
        for (var t = "", n = 0, r = 0, o = 0, i = 0; n < e.length; )
            (r = e.charCodeAt(n)) < 128 ? (t += String.fromCharCode(r),
            n++) : r > 191 && r < 224 ? (o = e.charCodeAt(n + 1),
            t += String.fromCharCode((31 & r) << 6 | 63 & o),
            n += 2) : (o = e.charCodeAt(n + 1),
            i = e.charCodeAt(n + 2),
            t += String.fromCharCode((15 & r) << 12 | (63 & o) << 6 | 63 & i),
            n += 3);
        return t
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

// 生成加密 payload
function encryptPayload(payloadObj) {
    const jsonStr = JSON.stringify(payloadObj); // JSON字符串
    const xorEncrypted = xorEncrypt(jsonStr);   // 异或加密
    return base64Encode(xorEncrypted);          // Base64 编码
}

// 生成签名
function getSig(f) {
    return CryptoJS.MD5(f + _p).toString().toUpperCase();
}

// 封装成一个函数，直接返回 {payload, sig}
function generatePayloadAndSig(payloadObj) {
    const f = encryptPayload(payloadObj);
    const sig = getSig(f);
    return { payload: f, sig };
}

// === 示例调用 ===
const payload = {
    sort: 1,
    start: 20,
    limit: 20
};



function d2(e) {
                for (var t = "", n = 0; n < e.length; n++) {
                    var r = _p.charCodeAt(n % _p.length);
                    t += String.fromCharCode(e.charCodeAt(n) ^ r)
                }
                return t = _u_d(t)
            }



function d1(e) {
                var t, n, r, o, i, a, u = "", c = 0;
                for (e = e.replace(/[^A-Za-z0-9\+\/\=]/g, ""); c < e.length; )
                    t = _keyStr.indexOf(e.charAt(c++)) << 2 | (o = _keyStr.indexOf(e.charAt(c++))) >> 4,
                    n = (15 & o) << 4 | (i = _keyStr.indexOf(e.charAt(c++))) >> 2,
                    r = (3 & i) << 6 | (a = _keyStr.indexOf(e.charAt(c++))),
                    u += String.fromCharCode(t),
                    64 != i && (u += String.fromCharCode(n)),
                    64 != a && (u += String.fromCharCode(r));
                return u
            }


            function decryptPayload(f_val) {
    // Base64 解码
    function base64Decode(e) {
        let t = "";
        let i = 0;
        e = e.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        while (i < e.length) {
            let o = _keyStr.indexOf(e.charAt(i++));
            let a = _keyStr.indexOf(e.charAt(i++));
            let r = _keyStr.indexOf(e.charAt(i++));
            let n = _keyStr.indexOf(e.charAt(i++));
            let s = o << 2 | a >> 4;
            let u = (a & 15) << 4 | r >> 2;
            let c = (r & 3) << 6 | n;
            t += String.fromCharCode(s);
            if (r !== 64) t += String.fromCharCode(u);
            if (n !== 64) t += String.fromCharCode(c);
        }
        return t;
    }

    // 异或解密
    function xorDecrypt(data) {
        let t = "";
        for (let n = 0; n < data.length; n++) {
            let r = _p.charCodeAt(n % _p.length);
            t += String.fromCharCode(data.charCodeAt(n) ^ r);
        }
        return t;
    }

    return JSON.parse(xorDecrypt(base64Decode(f_val)));
}

/**
 * 响应数据解密
 * @param data
 * @returns {any}
 */
function decrypt_data(data) {
    data =  d2(d1(data))
    return JSON.parse(data)
}

/**
 * 载荷加密
 * @param f
 * @returns {{sig, payload: string}}
 */
function get_params(f) {
    let f_payload = encryptPayload(payload);
    let p = getSig(f_payload);
    return { payload: f_payload, sig: p };
}

console.log(get_params(payload));


