const CryptoJS = require("crypto-js");

// -------------------- 参数 --------------------
const a = 3;                        // 页码
const c = "symmetry_challenge";     // challenge 类型
const s = Date.now();                // 时间戳
const i = `${a}_${c}_${s}`;          // 基础明文
const u = "abcdefghijklmnop";        // IV

// -------------------- 生成 p (aes_sign) --------------------
const aesKey = CryptoJS.enc.Utf8.parse("12345678901234567890123456789012");
const aesIv  = CryptoJS.enc.Utf8.parse(u);

const p = CryptoJS.AES.encrypt(CryptoJS.enc.Utf8.parse(i), aesKey, {
    iv: aesIv,
    mode: CryptoJS.mode.OFB,
    padding: CryptoJS.pad.NoPadding
}).toString();

// -------------------- 生成 f (des_sign) --------------------
function l(e) {
    const key = CryptoJS.enc.Utf8.parse("6f726c64");
    const iv  = CryptoJS.enc.Utf8.parse("01234567");
    const encrypted = CryptoJS.DES.encrypt(CryptoJS.enc.Utf8.parse(e), key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString();
}

const f = l(i + "_param");

// -------------------- 输出 --------------------
console.log("明文 i:", i);
console.log("p (aes_sign):", p);
console.log("f (des_sign):", f);
console.log("时间戳 t:", s);
