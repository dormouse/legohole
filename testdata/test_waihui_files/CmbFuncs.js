//PDA掌上银行
function cf_PDA_Download() {
    open('http://www.cmbchina.com/PDAbank/PDADownload.htm', 'PDAWin', 'menubar=no,toolbar=no,location=no,directories=no,scrollbars=no,status=no,resizable=no,top=0,left=100,width=266,height=441');
}

//大众版登录
function cf_HBWindows() {
    open('https://pbsz.ebank.cmbchina.com/CmbBank_GenShell/UI/GenShellPC/Login/Login.aspx', 'newhb', 'menubar=no,toolbar=no,location=no,directories=no,scrollbars=yes,status=yes,resizable=yes');
}

//i理财登录
function cf_IFinWindows() {
    open('https://pbsz.ebank.cmbchina.com/CmbBank_GenShell/UI/GenShellPC/NetBankAcc/Login.aspx', 'newifin', 'menubar=no,toolbar=no,location=no,directories=no,scrollbars=yes,status=yes,resizable=yes');
}

//信用卡登录
function cf_CreditCardLogin() {
    open('https://pbsz.ebank.cmbchina.com/CmbBank_GenShell/UI/GenShellPC/Login/Login.aspx?LoginType=C', 'creditcard', 'menubar=no,toolbar=no,location=no,directories=no,scrollbars=yes,status=yes,resizable=yes');
}

//专业版
function cf_EWallet() {
    open('http://www.cmbchina.com/cmbpb/v36/pb.htm', 'EWallet', 'menubar=no,toolbar=no,location=no,directories=no,status=yes,resizable=no,scrollbars=no,width=600,height=400,top=60,left=100');
}

//财富账户
function cf_WMAzybInstall() {
    open('http://wma.cmbchina.com/cmbinvestcenter/wmazyb/wmzybinstall.htm', 'wmzybinstall', 'menubar=no,toolbar=no,location=no,directories=no,status=no,resizable=no,scrollbars=yes,width=590,height=400,top=60,left=80');
}


//商户登录
function cf_OpenFirm() {
    open('https://ebank.sz1.cmbchina.com/EB10/EBServer?Command=5001&ClientID=0&PRID=LOGINPREVIEW', 'NewWindow', 'menubar=no,toolbar=no,location=no,directories=no,status=yes,scrollbars=0,resizable=0');
}
 
//信用卡申请进度查询
function cf_ApplySchedule() {
    open('https://pbsz.ebank.cmbchina.com/CmbBank_CreditCard/UI/CreditCardPC/CreditCard/na_QuerySchedule.aspx', 'Schedule', 'menubar=no,toolbar=no,location=no,directories=no,scrollbars=yes,status=yes,resizable=yes');
}

//信用卡支付系统使用协议
function cf_EnforceCardProtocol() {
    open('https://pbsz.ebank.cmbchina.com/CmbBank_CreditCard/UI/CreditCardPC/CreditCard/cs_ProOfActivate.aspx', 'EnforceCardProtocol', 'menubar=no,toolbar=no,location=no,directories=no,scrollbars=yes,status=yes,resizable=yes');
}

//港股交易登陆
function cf_LoginTradeSystem()
{
        var pageURL = "https://etrade.hk.cmbintl.com";
        var mywin = window.open(pageURL,"loginSystem","fullscreen=1, toolbar= no, menubar=no, scrollbars=no, resizable=yes, alwaysRaised=yes, fullscreen=no, location=no, status=no,top=0,left=0,width="+(screen.availWidth - 10).toString() +",height="+(screen.availHeight-30).toString(),"");
		mywin.moveTo(0,0)
		mywin.resizeTo(screen.width,screen.height)
}


//ICS 在线客服
var icsWnd = null;
var switchWnd = null;
function cf_FLoginICS() {
    var nWinLeft = (screen.width - 600) / 2;
    var nWinTop = (screen.height - 400) / 2;
    if (icsWnd != null)
        icsWnd.close();
    icsWnd = window.open('https://forum.cmbchina.com/cmu/icslogin.aspx?from=B&logincmu=0', 'icslogin', 'width=600,height=400,status=yes,left=' + nWinLeft + ',top=' + nWinTop);
}

//专业版演示
function cf_PBDemo()
{
 	open('http://www.cmbchina.com/cmbpb/v36/gb/demo/PBDemo1.htm','PBDemo','menubar=no,toolbar=no,location=no,directories=no,status=yes,resizable=no,scrollbars=yes,width=760,height=480,top=20,left=20');
}

//友情链接
function cf_GoodLink()
{
  open('http://www.cmbchina.com/about/goodlink.html');
}

//隐私保密条款
function cf_PrivacyLink()
{
  open('http://www.cmbchina.com/about/privacy.html');
}
//网站地图
function cf_SiteMapLink()
{
  open('http://www.cmbchina.com/about/sitemap.htm');
}


//手机一网通
function cf_MobileSite()
{
  open('http://m.cmbchina.com/web/index.html');
}


//网站声明
function cf_WebNoticeLink()
{
  open('http://www.cmbchina.com/about/webnotice.html');
}


//网安
function cf_GoToWangan()
{
  open('http://www.cmbchina.com/cmb2005web/webpages/cmbsafe/index.htm');
}

//深圳网络警察
function cf_GoToWangJing()
{
  open('http://www.sznet110.gov.cn/netalarm/index.jsp');
}


