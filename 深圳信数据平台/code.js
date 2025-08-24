const _0x27ca2a = require("crypto-js");

localStorage = {
    "isLogin": "false",
    "G_access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjQ0LCJleHBpcmVzX2F0IjoxNzU1OTgzNzM0NzMwLCJkZXZpY2VfaWQiOiJrbGluZUFsbDIuaHRtbGdzZm5iZDlsLnIyMWk3MHloLmdhbGt0IiwidXNlcl9pZCI6IjQ3MTU2ODEyNzM5MDc2NTAxOSIsImRldmljZV90eXBlIjoiMjAxIiwiaXNDTklwIjpudWxsLCJjbGllbnRfaWQiOiJTWlhTSlpYXzQ1IiwiaG9zdF9pZGVudGlmaWVyIjoiNDc1YjFkOWIwMjhiNTVkMzk2ZDkyZWM2YWU4ZWVhMTMiLCJqdGkiOiJmMTAwYjcwOC1hYjAxLTQ1MDUtOGE4OS04YTQ2ZDNmYTg0OGYifQ.5zddOzMsJkxAPrHFBsAHUjB-Yu8cGntU_PvA1pQTNU0",
    "slider": "slider-80f5798e-33db-4deb-8455-6acf9ef3394e",
    "device_id_internal": "ed1cc45b-1ffe-439e-88c1-601eae327761",
    "accept-cookie": "1",
    "G_localHttp": "https://gzdatasdk.mktdata.cn/application/",
    "uniqueId": "gsfnbd9l.r21i70yh.galkt",
    "G_userid": "471568127390765019",
    "point": "point-80f5798e-33db-4deb-8455-6acf9ef3394e",
    "tempenc": "1234567887654321",
    getItem: function (){}
}
function getResCode() {
    var _0x40a3a2 = _0x27ca2a.AES.encrypt(_0x27ca2a.enc.Utf8.parse(Math.floor(new Date().getTime() / 1000)), _0x27ca2a.enc.Utf8.parse(localStorage.getItem("tempenc") || "1234567887654321"), {
      iv: _0x27ca2a.enc.Utf8.parse("1234567887654321"),
      mode: _0x27ca2a.mode.CBC,
      padding: _0x27ca2a.pad.Pkcs7
    });
    return _0x27ca2a.enc.Base64.stringify(_0x40a3a2.ciphertext);
}

console.log(getResCode())

