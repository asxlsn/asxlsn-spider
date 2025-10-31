// 引入 JSEncrypt 库
const JSEncrypt = require('node-jsencrypt');

// 公钥字符串
const publicKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCMFPpXdR/mA3FOyB2L6HaxKRMBDWAPWA2j3qjBdDCu4lTiJ+ip9PwJW3XtaBonyeBdo22AYhMkLjAzfJnoFOFtbOf+oF4Ht4pgR3csXQqJsgvMSPInzexdayTD5Vg/quIgLlWVBLn670O2YOHd9/Ojc2GidoJnUO4D8YlfSd/sEwIDAQAB";

// 创建 JSEncrypt 对象
const encryptStr = new JSEncrypt();
encryptStr.setPublicKey(publicKey);

// 封装加密时间戳的方法
function encryptTimestamp(timestamp) {
    return encryptStr.encrypt(timestamp);
}

// 示例调用
const timestamp = new Date().getTime();
const encryptedTimestamp = encryptTimestamp(timestamp);

// 打印加密结果
console.log(encryptedTimestamp);
