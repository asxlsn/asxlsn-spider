// 固定密钥
const _p = "W5D80NFZHAYB8EUI2T649RT2MNRMVE2O";
const _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

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

// UTF-8 修复
function _u_d(e) {
    let t = "", n = 0, r = 0, o = 0, i = 0;
    while (n < e.length) {
        r = e.charCodeAt(n);
        if (r < 128) {
            t += String.fromCharCode(r);
            n++;
        } else if (r > 191 && r < 224) {
            o = e.charCodeAt(n + 1);
            t += String.fromCharCode((31 & r) << 6 | (63 & o));
            n += 2;
        } else {
            o = e.charCodeAt(n + 1);
            i = e.charCodeAt(n + 2);
            t += String.fromCharCode((15 & r) << 12 | (63 & o) << 6 | (63 & i));
            n += 3;
        }
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

// Base64 + 异或 + UTF-8 修复
function decryptParam(f_val) {
    const base64Decoded = base64Decode(f_val);
    const xorDecoded = xorDecrypt(base64Decoded);
    return JSON.parse(_u_d(xorDecoded));
}
params = 'LBctVlQ7NS46OAYrXDZ3cwNiAw0VcDBdICshOT8mEHUjRzFdHGwlNToxNjBZMTAWXjtVVU07O1wEKiFvbB5vY3VBJV9vICc3LTJ7eGNnst2HsaOy0Mni19ngcGF0o6fWv7f2Gm1iZDknMyktSiQhLG0mWUFXNicQdxUPYXQ2XT0jF34PBn52bGRjNjBcICdrCHkHGBshIFM/OnB3ZmkQIz5YLUwSdHdqNQ=='
console.log(decryptParam(params));
