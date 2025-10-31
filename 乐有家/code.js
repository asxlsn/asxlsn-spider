
const CryptoJS = require("crypto-js");


const DEFAULT_KEY = "ODcyYTUxNGM1N2M2";

// AES-ECB-PKCS7 加密
function aesEncrypt(plainText, key = DEFAULT_KEY) {
    const keyBytes = CryptoJS.enc.Utf8.parse(key);
    const textBytes = CryptoJS.enc.Utf8.parse(plainText);
    const encrypted = CryptoJS.AES.encrypt(textBytes, keyBytes, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString(); // Base64
}

 // AES-ECB-PKCS7 解密
 function aesDecrypt(cipherText, key = DEFAULT_KEY) {
    const keyBytes = CryptoJS.enc.Utf8.parse(key);
    const decrypted = CryptoJS.AES.decrypt(cipherText, keyBytes, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return decrypted.toString(CryptoJS.enc.Utf8);
}

// 生成加密的查询参数
function getQueryParamsEncrypt(obj) {
    let queryStr = "";
    for (let k in obj) {
        if (typeof obj[k] !== "string" && obj[k]) {
            queryStr += `${k}=${JSON.stringify(obj[k])}&`;
        } else if (obj[k]) {
            queryStr += `${k}=${obj[k]}&`;
        }
    }
    queryStr = queryStr.substring(0, queryStr.length - 1); // 去掉最后的 &
    return encodeURIComponent(aesEncrypt(queryStr)); // AES 加密 + URL 编码
}

// 你的 e 对象
const e = {
    "eId": "click",
    "obj": {
        "pId": "pages/esfList/esfList",
        "target": "#changeArea",
        "gray": "",
        "index": 0
    },
    "bd": "microsoft",
    "osv": "10",
    "scs": "1024x768",
    "osl": "zh_CN",
    "dpi": 1.25,
    "bat": 100,
    "uid": 8215939,
    "unionId": "on1pG1ejwdcumZ6WxvJLHGuW8cEI",
    "ref": "pages/index/index"
};

// // 输出加密结果
// const encryptedParams = getQueryParamsEncrypt(e);
// console.log("加密后的 e 参数：", encryptedParams);

// const decrypt_data = aesDecrypt(str);
// const jsonData = JSON.parse(decrypt_data);
// console.log(JSON.stringify(jsonData, null, 2)); // 格式化输出 JSON 数据
// str = 'tVV6Z/sU1+o/p1TRyFwShfWiAIPN2VRKps/ZvoMec8UzOsOmv/lTjzXzwwKuQaHVipPZmN9Akx48I/shIx/hjlA9qsDwtJ1H/XA0IF4RPkewrIoOTpFNzv889/8iq8eFg01tGn5k9Y3xc8aeovZg8lBW3BqVMUz0PUm8IVPlZeDfOPD3mvs9VbD5mjp6lPaklfGuhHNNOguYL7X1+/Pg2on+wrfIVZgcgyx2WUU5Ei7kVPkYmidgGgwvWfj79Ms1'
// console.log(aesDecrypt(str));;


// 模拟 e.data
const data = {
    "cityCode": "000002",
    "includeFrontImage": 1,
    "listQuery": 1,
    "rstype": 2,
    "pageNo": 1,
    "pageSize": 20,
    "starHouseQuery": 1,
    "tgLocationKey": "min_esf_list",
    "uuid": "oVs0Z0eheUCSdhVZI1yNeH8i3mGE"
}

// AES 密钥
const key = "ODcyYTUxNGM1N2M2";

// AES 加密函数
function AesEncrypt(text, key) {
    const keyUtf8 = CryptoJS.enc.Utf8.parse(key);
    const encrypted = CryptoJS.AES.encrypt(text, keyUtf8, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString(); // 默认是 Base64
}

// 生成 key
function generateKey(data, useEncrypt = true, l = false) {
    let m = null;
    if (data && Object.keys(data).length > 0) {
        if (useEncrypt) {
            if (l) {
                m = AesEncrypt(JSON.stringify(data), key);
            } else {
                m = {
                    key: AesEncrypt(JSON.stringify(data), key)
                        .replace(/[\s\u00A0\u200B]+/g, e => '+'.repeat(e.length))
                };
            }
        } else {
            m = data;
        }
    }
    return m;
}

function getKey(){
    return generateKey(data, true, false);
}

// // 示例调用
// const result1 = generateKey(data, true, true);  // 直接 AES 字符串
// const result2 = generateKey(data, true, false); // 对空格+零宽字符替换后返回对象


