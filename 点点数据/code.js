
e = {
    "market_id": 2,
    "genre_id": 0,
    "country_id": 75,
    "device_id": 0,
    "page": 1,
    "time": 1758816000,
    "rank_type": 1,
    "brand_id": 201,
    "sub_brand_id": 0
}

path = "/v1/rank"

n = {
    "s": "0d2c95947e15e60e9264b3ac68930dc8",
    "k": "13a026a8b1af5cc3",
    "l": "a2896c2c89a5d290",
    "d": 4,
    "sort": "dd",
    "num": 10
}
r = "get"

function v(e, path, n, r) {
    var s = n.s
      , d = n.k
      , m = n.l
      , f = n.d
      , v = n.sort
      , l = n.num
      , k = function(content, t, e) {
        for (var a = Array.from(content), n = Array.from(t), r = a.length, o = n.length, d = String.fromCodePoint, i = 0; i < r; i++)
            a[i] = d(a[i].codePointAt(0) ^ n[(i + e) % o].codePointAt(0));
        return a.join("")
    }(function(s, t, path, e) {
        return [s, t, e, path].join("(&&)")
    }(function(t, e) {
        var n = c()(t);
        if (!h()(n)) {
            var r = [];
            for (var d in n)
                _()(n[d]) && "get" === e && (n[d] = n[d].join("")),
                "post" === e && (_()(n[d]) || o()(n[d])) && (n[d] = JSON.stringify(n[d])),
                r.push(n[d]);
            return r.sort(),
            r.join("")
        }
    }(e, r), parseInt((new Date).getTime() / 1e3) - 655876800 - f, path, v), Object(y.b)(s, d, m), l);
    return t.from(k).toString("base64")
}

console.log(v(e, path, n, r))


