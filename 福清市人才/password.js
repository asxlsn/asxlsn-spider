const CryptoJS = require("crypto-js");
const NodeRSA = require("node-rsa");

// 网站的公钥（Base64 格式）
const publicKeyBase64 = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDCeOxp3Zml2lo4ZuuphxpeB2kJbsTbSpYjOZ4eYqMDB9L5mG4uOaUtJ6ooznlKwB8dE8GvYBU7ROQHtjmolB7hIghFk2aCZMjb+kM733uhHnWNaiQ2ZbYcw+geZVB729Kd+GEbP+LvueMfTjEQQCjH956mEOsK96u5MuQniawxHwIDAQAB";

// 拼成 PEM 格式
const publicKeyPEM = `-----BEGIN PUBLIC KEY-----\n${publicKeyBase64}\n-----END PUBLIC KEY-----`;

// RSA 加密器（PKCS#1 v1.5）
const key = new NodeRSA(publicKeyPEM, 'pkcs8-public', {
    encryptionScheme: 'pkcs1'
});

// 要加密的密码
const password = "111111";

// 先 RSA 加密得到二进制
const encryptedBuffer = key.encrypt(password, 'buffer'); // buffer 格式

// 转成 hex
const encryptedHex = encryptedBuffer.toString('hex');

// hex -> Base64（CryptoJS 版本的 hex2b64）
function hex2b64(hexStr) {
    const words = CryptoJS.enc.Hex.parse(hexStr);
    return CryptoJS.enc.Base64.stringify(words);
}

const encryptedB64 = hex2b64(encryptedHex);

console.log("最终加密结果：", encryptedB64);
