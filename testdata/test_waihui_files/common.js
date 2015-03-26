var fx = jQuery.noConflict();

function showSubmenu(smid) {
    var submenu = fx("div[id^='submenu_" + smid + "']");

    if (null != submenu && typeof submenu != "undefined") {
        fx("div[id^='submenu_']").attr("class", "hide");
        submenu[0].className = "";
    }
}

function hideSubmenu(smid) {
    var submenu = fx("div[id^='submenu_" + smid + "']");
    
    if (null != submenu && typeof submenu != "undefined") {
        fx("div[id^='submenu_']").attr("class", "hide");
        submenu[0].className = "hide";
        fx("div[id*='_cur']")[0].className = "";
    }
}

function adjustHeight(leftid, rightid) {
    var left = document.getElementById(leftid);
    var right = document.getElementById(rightid);
    
    if (left != null && right != null) {
        if (left.clientHeight < right.clientHeight) {
            left.style.minHeight = right.clientHeight + "px";
            
            if (window.ActiveXObject) {
                var browser = navigator.appName ;
                var version = navigator.appVersion.split(";"); 
                version = version[1].replace(/[ ]/g,""); 
                
                if (browser == "Microsoft Internet Explorer" && version == "MSIE6.0") {
                    left.style.height = right.clientHeight + "px";
                }
            }
        } else {
            right.style.height = left.clientHeight + "px";
        }
    }
}

function openHq() {
    var branch = document.getElementById("branch").value;
    
    if (null != branch && "" != branch) {      
	
        window.location.href = "/Hq/CmbQuote.aspx?branch=" + branch;
    }
}