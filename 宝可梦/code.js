const CryptoJS = require("crypto-js");

r = {
  params: {},
  timeout: 398,
  userToken:
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uSWQiOiI1RDRFNzI2MkExMUM0QUEwQjdEMzUxQTc0REMwNkU2QyIsIm9wZXJhdG9ySWQiOiIxNDA0ODExIn0.iDnwz6lTWkhLgFqrBkJFdBTsmpSCsRZ_41O1wpHwMOA",
  encryptionEnable: true,
};

function n(e, r, t) {
  var n = new Array(),
    a = 0;
  for (var i in e) (n[a] = i), a++;
  var o = n.sort(),
    u = {};
  for (var s in o) u[o[s]] = e[o[s]];
  if (Array.isArray(e)) {
    if (r) return JSON.parse(JSON.stringify(e));
    u = {
      str: JSON.stringify(e),
    };
  }
  return JSON.parse(
    JSON.stringify(u, function (e, r) {
      if (e) {
        if (null == r || null == r) return;
        return r instanceof Object ? (t ? r : JSON.stringify(r)) : "" + r;
      }
      return r;
    })
  );
}

/**
 * AES 解密
 * @param url_data
 * @Description
 * decodeURIComponent(url_data) → 还原 Base64 密文
 * aesDecrypt(decoded_url) → 得到原始明文
 * @returns {string}
 */
function aesDecryptFromUrlParam(url_data) {
  // 1. URL 解码
  let decoded_url = decodeURIComponent(url_data);
  return aesDecrypt(decoded_url);
}

/**
 * js对象类型
 * 加密参数并返回URL参数
 * @param params
 * @returns {string}
 */
function encryptParamsForUrl(params) {
  // 将参数对象转换为JSON字符串
  const paramsString = JSON.stringify(params);

  // AES加密并进行URL编码
  // param_url_encoded = aesEncryptFromUrlParam(paramsString);
  return aesEncryptFromUrlParam(paramsString);
}

/**
 * AES 加密
 * @Description
 * 明文 url_data
 *
 * aesEncrypt(url_data) → 得到 Base64 密文
 * encodeURIComponent() → 变成 URL 安全格式
 *
 * @param url_data
 * @returns {string}
 */
function aesEncryptFromUrlParam(url_data) {
  let encrypt = aesEncrypt(url_data);
  return encodeURIComponent(encrypt);
}
/**
 * AES加密函数
 * @param {string} text 要加密的文本
 * @returns {string} 加密后的文本
 */
function aesEncrypt(text) {
  var key = CryptoJS.enc.Utf8.parse("Njda*7^%1<.)0=+u&%hkfs;k");
  return CryptoJS.AES.encrypt(text, key, {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7,
    keySize: 6,
  }).toString();
}

/**
 * AES解密函数
 * @param {string} encryptedText 加密的文本
 * @returns {object} 解密后的对象
 */
function aesDecrypt(encryptedText) {
  var key = CryptoJS.enc.Utf8.parse("Njda*7^%1<.)0=+u&%hkfs;k");
  var decrypted = CryptoJS.AES.decrypt(encryptedText, key, {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7,
    keySize: 6,
  });
  return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
}

/**
 * 解密数据并格式化数据
 * @param encryptedData
 * @returns {any|null}
 */
function decryptAndFormat(encryptedData) {
  try {
    // 解密数据
    const decryptedData = aesDecrypt(encryptedData);
    // 格式化输出
    console.log(JSON.stringify(decryptedData, null, 2));
    // 返回解密后的数据供进一步使用
    return decryptedData;
  } catch (error) {
    console.error("解密或格式化失败:", error.message);
    return null;
  }
}
/**
 * 签名函数
 * @param {object} r 配置对象
 * @returns {object} 签名结果
 */
function Sign(r) {
  var t = r.timeout,
    a = r.userToken,
    i = r.params,
    o = r.encryptionEnable,
    u = (Date.now() + t).toString(),
    s = Math.round(1e6 * Math.random()),
    f = JSON.stringify(n(i, !1, o)),
    d = JSON.stringify(n(i, !0, o));

  // 拼接待签名字符串
  const toSign = a + f + s + u + "fWS21MVyxkYwEoCIAHieg7Tqn0jPl3GzQvRsDJcb";

  // 计算MD5，转小写
  const signature = CryptoJS.MD5(toSign).toString().toLowerCase();

  return {
    timestamp: u,
    nonce: s,
    signature: signature,
    secretJsonParams: d,
  };
}

function get_signature() {
  return Sign(r);
}

// 示例
var str_params = "7QkQL6Sa9TN4zR3ZetrrwA%3D%3D";
var url_text = '{"id":"4204"}';
console.log(aesDecryptFromUrlParam(str_params));
console.log(aesEncryptFromUrlParam(url_text));
