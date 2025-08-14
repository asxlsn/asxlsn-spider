const CryptoJS = require("Crypto-JS");
function getSign(){
    let token = '052d1cb364e87691951c0d099af14eda'
    // let timestamp = Date.now();
    let timestamp = 1755101061446
    let data ='{"inputWords":"手机","searchReqFromPage":"xyPcHome","bucketId":30,"type":0}'
    var str = token + "&" + timestamp + "&" + '34839810' + "&" + data;
    return CryptoJS.MD5(str).toString();

}






console.log(getSign())