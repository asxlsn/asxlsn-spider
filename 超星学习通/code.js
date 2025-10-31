const CryptoJS = require("crypto-js");
function encryptByAES(message, key) {
    let CBCOptions = {
        iv: CryptoJS.enc.Utf8.parse(key),
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    };
    let aeskey = CryptoJS.enc.Utf8.parse(key);
    let secretData = CryptoJS.enc.Utf8.parse(message);
    let encrypted = CryptoJS.AES.encrypt(
        secretData,
        aeskey,
        CBCOptions
    );
    return CryptoJS.enc.Base64.stringify(encrypted.ciphertext);
}

function login(phone, pwd){
   let transferKey = "u2oh6Vu^HWe4_AES";
    pwd = encryptByAES(pwd, transferKey);
    phone = encryptByAES(phone, transferKey);
    return {
        "phone": phone,
        "pwd": pwd
    }
}



