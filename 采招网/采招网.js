const CryptoJS = require('crypto-js');
variate = {
    "key": {
        "words": [
            863652730,
            2036741733,
            1164342596,
            1782662963
        ],
        "sigBytes": 16
    },
    "aceIV": {
        "words": [
            1719227713,
            1314533489,
            1397643880,
            1749959510
        ],
        "sigBytes": 16
    },
    "xgGjcArray": [],
    "xgGjcIndex": 0,
    "isPageLoad": true
}
AESDecrypt = function (str) {
    var nContent = CryptoJS.AES.decrypt(str, variate.key, {
        iv: variate.aceIV,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.ZeroPadding
    })
    if (nContent && nContent != null) {
        try {
            var constr = CryptoJS.enc.Utf8.stringify(nContent)
            if (constr != "") {
                var data = JSON.parse(constr);
                return data;
            } else
                return null;
        } catch (err) {
            return null;
        }

    } else
        return null;
}

