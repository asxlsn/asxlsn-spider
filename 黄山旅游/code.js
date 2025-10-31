const JSEncrypt = require('node-jsencrypt');

const pubKey = `-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDI5kmdW9rmxQlTraZ6Wx+C7kYR
DjL332N53dsqFsqqT+PX6mosaM5hW4MS4vUbQNtUblhmQgzmUD0KBJFH9YZMmSPL
dCC+G4r7d2PPFBrCy+9dFUMUNaT4PenyaVQJyAp3bhUJ7n93bRJT9jtxsdDwJ/Zl
12A/kO93fr7+waaepwIDAQAB
-----END PUBLIC KEY-----`;

function toRSAcode(text) {
    const encryptor = new JSEncrypt();
    encryptor.setPublicKey(pubKey);
    const resultText = encryptor.encrypt(text);
    return encodeURIComponent(resultText);
}
