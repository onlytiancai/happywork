$(function(){
    var getCookie = function(c_name) {
        var i,x,y,ARRcookies=document.cookie.split(";");
        for (i=0;i<ARRcookies.length;i++) {
            x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
            y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
            x=x.replace(/^\s+|\s+$/g,"");
            if (x==c_name) {
                return decodeURI(y);
            }
        }
    }
    
    if (getCookie("sessionid") == undefined){
        $('.navbar .nav-pills').append("<li><a href='/login/index.html'>登录</a></li>");
    }else {
        $('.navbar .nav-pills').append("<li><a href='/login/index.html'>"+getCookie("nickname")+"</a></li>");
    }
});
