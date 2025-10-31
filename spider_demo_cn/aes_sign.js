const CryptoJS = require("crypto-js");

// === l() 函数 ===
function l(e) {
    const key = CryptoJS.enc.Utf8.parse("6f726c64"); // 8字节 key
    const iv  = CryptoJS.enc.Utf8.parse("01234567"); // 8字节 IV
    const encrypted = CryptoJS.DES.encrypt(
        CryptoJS.enc.Utf8.parse(e),
        key,
        { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 }
    );
    return encrypted.toString(); // Base64 输出
}

// === 构造明文 ===
const a = 3;                        // 页码
const c = "symmetry_challenge";     // challenge 类型
const s = Date.now();                // 时间戳
const i = `${a}_${c}_${s}`;

// === 生成 f ===
const des_sign = l(i + "_param");

console.log("明文 i:", i);
console.log("des_sign:", des_sign);
