function coverNum(num, len) {
    num = Math.round(num).toString();
    while (num.length < len) {
        num = '0' + num;
    }
    return num;
}

function dealMapArr(points) {
    var res = '';
    for (var i=0; i<points.length; i++) {
        res += coverNum(points[i][0], 3);
        res += coverNum(points[i][1], 3);
    }
    return res;
}
