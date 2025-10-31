

function watch(obj, name) {
    const isProxyActive = Symbol("isProxyActive");
    return new Proxy(obj, {
        get: function (target, property, receiver) {
            try {
                const value = target[property];
                if (value === undefined && !receiver[isProxyActive]) {
                    const protoChainNeeded = !Object.getPrototypeOf(target).hasOwnProperty(property);
                    const descriptor = Object.getOwnPropertyDescriptor(target, property) || {};
                    const toStringDesc = descriptor.toString || (descriptor.get && descriptor.get.toString());
                    console.log(`${name}.${property} 读取: ${String(value)} (${typeof value}), 补原型链: ${protoChainNeeded}, toString: ${toStringDesc || '无'}`);
                }
            } catch (e) {}
            return target[property];
        },
        set: (target, property, newValue, receiver) => {
            try {
                if (!receiver[isProxyActive]) {
                    const displayValue = String(newValue);
                    if (displayValue.length <= 50) {
                        const protoChainNeeded = !Object.getPrototypeOf(target).hasOwnProperty(property);
                        const descriptor = Object.getOwnPropertyDescriptor(target, property) || {};
                        const toStringDesc = descriptor.toString || (descriptor.get && descriptor.get.toString());
                        console.log(`${name}.${property} 设置: ${displayValue} (${typeof newValue}), 补原型链: ${protoChainNeeded}, toString: ${toStringDesc || '无'}`);
                    }
                }
            } catch (e) {}
            return Reflect.set(target, property, newValue, receiver);
        }
    });
}









window = global
//做了什么事情，返回什么
//当前js代码执行之后所执的方法
window.requestAnimationFrame = function(args){
    console.log("requestAnimationFrame ====>:", args)
}
window.setInterval = {}
window.setTimeout = {}
window.innerWidth = 667
window.innerHeight = 703
window.outerWidth = 1536
window.outerHeight =824
window.screenX = 0
window.screenY = 0
window.pageYOffset = 0
window.pageXOffset = 0
window.Navigator = function(args){
    console.log("对象 => Navigator ====>:", args)
}

window.EventSource = function(args){
    console.log("对象 => EventSource ====>:", args)
}
window.screen = {
  "availHeight": 824,
  "availLeft": 0,
  "availTop": 0,
  "availWidth": 1536,
  "colorDepth": 24,
  "height": 864,
  "isExtended": false,
  "onchange": null,
  "orientation": {
    "angle": 0,
    "type": "landscape-primary",
    "onchange": null
  },
  "pixelDepth": 24,
  "width": 1536
}

window.onwheelx = {
    "_Ax": "0X21"
}
window.sessionStorage = {
    "__tea_session_id_24": "{\"sessionId\":\"b021df40-13aa-4f86-972e-289e4d812d3c\",\"timestamp\":1755412604883}",
    "tt_scid": "A322.YAsfxfxbojJO5Lng8-SKGmWBh86HfylcQUYGH-t1NrsRzazN8no.GK3KTZr9e47",
    "_tea_cache_duration": "{\"duration\":688433,\"page_title\":\"今日头条\"}",
    "_byted_param_sw": "7delTpqkrqvxvItbXfE=",
    "/": "1",
    "__tea_session_id_2018": "{\"sessionId\":\"217ee8d1-9f0c-4bb8-a1cd-4bd439c8646c\",\"timestamp\":1755411916014}"
}
window.localStorage = {
    "__tea_cache_first_2018": "1",
    "__pwa_push_show_count": "3",
    "__tea_cache_first_24": "1",
    "__tea_cache_tokens_2018": "{\"web_id\":\"7536483330960197129\",\"user_unique_id\":\"verify_me3xiw4c_vL0FhxX2_s278_4LmZ_9fyU_m0dyayVQayIL\",\"timestamp\":1755411916011,\"_type_\":\"default\"}",
    "xmst": "YUZ3Jcw5dy6VpYkaHv343FRWIU1CNamFsi62E6I0jY-0xRX62hGlKfpavuxH9X64-DDuaenhwNAjCgVUfaxHTyoiW4GxuMfQI2KJZ2S1NGYQ4TlaiNg-W-wwqMWbl4Zk4qw=",
    "__tea_cache_tokens_24": "{\"web_id\":\"7536483291210515994\",\"user_unique_id\":\"7536483291210515994\",\"timestamp\":1755412604637,\"_type_\":\"default\"}",
    "__pwa_push_show_time": "1755341072994",
    "__tea_cache_refer_24": "{\"refer_key\":\"\",\"refer_title\":\"今日头条\",\"refer_manual_key\":\"\",\"routeChange\":false}",
    "__is_visited_home": "1",
    "tt_scid": "A322.YAsfxfxbojJO5Lng8-SKGmWBh86HfylcQUYGH-t1NrsRzazN8no.GK3KTZr9e47",
    "_byted_param_sw": "7delTpqkrqvxvItbXfE=",
    "web_runtime_security_uid": "c57ade44-6515-41d2-a7ea-b6a58b20b732",
    "SLARDARtoutiao_web_pc": "JTdCJTIydXNlcklkJTIyOiUyMjc1MzY0ODMyOTEyMTA1MTU5OTQlMjIsJTIyZGV2aWNlSWQlMjI6JTIyNzUzNjQ4MzI5MTIxMDUxNTk5NCUyMiwlMjJleHBpcmVzJTIyOjE3NjMxODg2MDQ5NTUlN0Q=",
    "ttcid": "e695739eceb7464791b9cecf539e12e532"
}
window._sdkGlueVersionMap = {
    "sdkGlueVersion": "1.0.0.55",
    "bdmsVersion": "1.0.1.7",
    "captchaVersion": "4.0.2"
}

//套上深度代理
window = watch(window, "window")


span = {
    classList:[]
}


document = {}
document.body ={}
document.referrer = ''
document.cookie = 'ttcid=e695739eceb7464791b9cecf539e12e532; s_v_web_id=verify_me3xiw4c_vL0FhxX2_s278_4LmZ_9fyU_m0dyayVQayIL; local_city_cache=%E6%88%90%E9%83%BD; csrftoken=ac831339b921788847887b220f6fd0b9; _ga=GA1.1.1425957257.1754724272; gfkadpd=24,6457; tt_scid=A322.YAsfxfxbojJO5Lng8-SKGmWBh86HfylcQUYGH-t1NrsRzazN8no.GK3KTZr9e47; _ga_QEHZPBE5HH=GS2.1.s1755411915$o7$g1$t1755412604$j60$l0$h0'
document.createElement = function (args){
    console.log("对象 => document.createElement('" + args+ "')")
    if (args === "span"){
        return watch(span, "span")
    }
}
document.documentElement =  {}
document.documentElement = watch(document.documentElement, "document.documentElement")
document = watch(document, "document")
XMLHttpRequest = function (args){
    console.log("对象 => XMLHttpRequest ====>:", args)
}



require("./jdms.js")





arguments = [
    0,
    1,
    12,
    "offset=0&channel_id=94349549395&max_behot_time=0&category=pc_profile_channel&disable_raw_data=true&aid=24&app_name=toutiao_web&msToken=YUZ3Jcw5dy6VpYkaHv343FRWIU1CNamFsi62E6I0jY-0xRX62hGlKfpavuxH9X64-DDuaenhwNAjCgVUfaxHTyoiW4GxuMfQI2KJZ2S1NGYQ4TlaiNg-W-wwqMWbl4Zk4qw%3D&msToken=YUZ3Jcw5dy6VpYkaHv343FRWIU1CNamFsi62E6I0jY-0xRX62hGlKfpavuxH9X64-DDuaenhwNAjCgVUfaxHTyoiW4GxuMfQI2KJZ2S1NGYQ4TlaiNg-W-wwqMWbl4Zk4qw%3D",
    "",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
]
var r = window.uuuu._v;
a_bours = window.uuuu._u(r[0], arguments, r[1], r[2])
console.log(a_bours.length)





