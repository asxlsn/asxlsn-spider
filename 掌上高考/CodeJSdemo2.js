const CryptoJs = require('crypto-js')


function w(t) {
    var {SIGN: t, str: n} = t
      , n = (n = decodeURI(n),
    // 消息摘要算法当中  带key
    CryptoJs.HmacSHA1(CryptoJs.enc.Utf8.parse(n), t));
    t = CryptoJs.enc.Base64.stringify(n).toString();
    return CryptoJs.MD5(t).toString();
}

function main123(d) {
    const g = "D23ABC@#56";
    // d = "https://api.zjzw.cn/web/api/?is_single=2&local_province_id=43&page=" + page + "&province_id=&request_type=1&size=10&special_id=4&top_school_id=1391&type=&uri=apidata/api/gk/special/school"
    O = w({
        SIGN: g,
        str: d.replace(/^\/|https?:\/\/\/?/, "")
    })
    return O
}