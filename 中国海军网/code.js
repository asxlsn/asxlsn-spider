const CryptoJS = require("crypto-js");

function encryptBy3DES(t) {
    const key = "WfJTKO9S4eLkrPz2JKrAnzdb"; // 24字节Key
    const iv  = "D076D35C";                 // 8字节IV

    // 转成 CryptoJS 格式
    const keyHex = CryptoJS.enc.Utf8.parse(key);
    const ivHex  = CryptoJS.enc.Utf8.parse(iv);

    // 3DES CBC PKCS7
    const encrypted = CryptoJS.TripleDES.encrypt(t, keyHex, {
        iv: ivHex,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });

    return encrypted.toString(); // Base64
}

console.log(encryptBy3DES("111111")); // KGSsr+SFSt4=
