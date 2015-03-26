function cf_openCont(URL)
{
  var l = (window.screen.width-634)/2;
  var t = (window.screen.height-400)/2;
  open(URL,'','menubar=no,toolbar=no,location=no,directories=no,status=no,resizable=no,scrollbars=yes,width=634,height=400,top='+t+',left='+l);
}

function cf_ColAdvWinScroll(url,w,h)
{
open(url,'','menubar=no,toolbar=no,location=no,directories=no,status=no,resizable=yes,scrollbars=yes,width='+w+',height='+h+',top=50,left=50');
}


function cf_CmbSearch(sSearchWord,sfromweb)
{
   if (sSearchWord == '' ||sSearchWord==null || sSearchWord.trim()==""  )
   {
     alert("关键词不能为空");
     return false
   }
           else if(sSearchWord.length>50)
           {
       		alert("您输入的检索词超过最大长度50！");
       		return false;
       	   }
          else
          {
               var searchwordwhere=sSearchWord.trim().trssearch().replaceteshustr();
               if(searchwordwhere=="" || searchwordwhere==null)
        	{
        	     alert("抱歉，您输入的内容不在查询范围内！");
        		return false;
        	}
                else if(null != sfromweb && "" != sfromweb)
                {
                window.open('http://search.cmbchina.com/cmb/jsp/portalsearch/doclist_of_search.jsp?fromweb=' + sfromweb + '&SearchWord='+ encodeURI(searchwordwhere));
                }
                else
                {
        	      window.open('http://search.cmbchina.com/cmb/jsp/portalsearch/doclist_of_search.jsp?SearchWord='+ encodeURI(searchwordwhere));
                }
        	   
           }          
     
}
    
String.prototype.trim = function()
{
    return this.replace(/(^[\s]*)|([\s]*$)/g, "");
}
String.prototype.trssearch = function()
{
    return this.replace(/\s+/g, "+");
}

String.prototype.replaceteshustr = function()
{
    return this.replace(/[@#\$%\^&\*!~'(（\-\/%.。，,?+]+/g, "");
}



function cf_GetToMonth()   //获得今天的日期 格式：
{
	var today=new Date();
	var nowYear=today.getYear();
	var nowMonth=today.getMonth();
	nowMonth++;
   return nowYear+"-"+nowMonth;
}



//判断身份证是否合格，并且校验是否正确
function cf_CheckIDcard(idcard)            
{
        idcard=cf_AllTrim(idcard);
	var Errors=new Array(
	"ok",
	"身份证号码位数不对！",
	"身份证号码出生日期超出范围或含有非法字符！",
	"身份证号码校验错误！"
	);

	var idcard,Y,JYM;
	var S,M;
	var idcard_array = new Array();
	idcard_array = idcard.split("");
	//身份号码位数及格式检验
	switch(idcard.length)
	{

	case 15:
		if ((parseInt(idcard.substr(6,2))+1900) % 4 == 0 || ((parseInt(idcard.substr(6,2))+1900) % 100 == 0 && (parseInt(idcard.substr(6,2))+1900) % 4 == 0 ))
			{
			ereg=/^[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$/;//测试出生日期的合法性
			}
		else
		{ 
			ereg=/^[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$/;//测试出生日期的合法性
		}
		if(ereg.test(idcard)) return Errors[0];
		else   return Errors[2];
		break;

	case 18:
	//18位身份号码检测
	//出生日期的合法性检查 
	//闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
	//平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
	    if ((parseInt(idcard.substr(6,4)) % 400 == 0) || ((parseInt(idcard.substr(6,4)) % 100 != 0) && (parseInt(idcard.substr(6,4)) % 4 == 0)))
		{
			ereg=/^[1-9][0-9]{5}[1-9][0-9]{3}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$/;//闰年出生日期的合法性正则表达式
		}
		else
		{
			ereg=/^[1-9][0-9]{5}[1-9][0-9]{3}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$/;//平年出生日期的合法性正则表达式
		}
		if(ereg.test(idcard))
		{//测试出生日期的合法性
			//计算校验位
			S = (parseInt(idcard_array[0]) + parseInt(idcard_array[10])) * 7
			+ (parseInt(idcard_array[1]) + parseInt(idcard_array[11])) * 9
			+ (parseInt(idcard_array[2]) + parseInt(idcard_array[12])) * 10
			+ (parseInt(idcard_array[3]) + parseInt(idcard_array[13])) * 5
			+ (parseInt(idcard_array[4]) + parseInt(idcard_array[14])) * 8
			+ (parseInt(idcard_array[5]) + parseInt(idcard_array[15])) * 4
			+ (parseInt(idcard_array[6]) + parseInt(idcard_array[16])) * 2
			+ parseInt(idcard_array[7]) * 1 
			+ parseInt(idcard_array[8]) * 6
			+ parseInt(idcard_array[9]) * 3 ;
			Y = S % 11;
			M = "F";
			JYM = "10X98765432";
			M = JYM.substr(Y,1);//判断校验位
			
			if(M == idcard_array[17]) return Errors[0]; //检测ID的校验位
			else return Errors[3];
		}
		else return Errors[2];
		break;
		default:
		return Errors[1];
		break;
		}

}

/// 检查姓名是否符合要求，并且无特殊字符
function cf_CheckName(Name) {
    var ErrStr;
    var ErrChar;
    var ArryErrStr;
    ErrChar = "!@#$%^&*()_+|-=\~`;'[]{}\"':;,.<>?～！@#￥％^&×（）……＋|－＝、〔〕｛｝：“；‘《》？，。、1234567890";
    ErrStr = "虚拟,傻冒,先生,小姐,代订";
    ArryErrStr = ErrStr.split(",");
    //是否含有非法字符
    for (var k = 0; k < Name.length; k++) {
        if (ErrChar.indexOf(Name.charAt(k)) > -1) {
            return false;
        }
    }
    //是否含有非法字符串
    for (k = 0; k < ArryErrStr.length; k++) {
        if (Name.indexOf(ArryErrStr[k]) > -1) {
            return false;
        }
    }
    return true;
}


////比较日期 Start date 和 End date 
////参数 2010/11/11
function cf_CompareDate(sdate,edate)
{		
    sdate = cf_ConvertDate(sdate,'A');
    edate = cf_ConvertDate(edate,'A');
    var sDate = Date.parse(sdate);
    var eDate = Date.parse(edate);
    var result = sDate - eDate;   
    var NDAY = 60*60*24; //一天
    if(result == 0)
    {
       return 0;
    }
    else if(result > NDAY)
    {
       return 1;    //sdate 大于 edate
    }
    else
    {
       return -1;    // sdate 小于 edate
    }
}


function cf_IsNumber(s)   //检查输入字符串是否符合正整数格式
{
        s=cf_AllTrim(s);
	var regu = "^[0-9]+$";
	var re = new RegExp(regu);
	if (s.search(re) != -1) 
	{
	 return true;
	}
	else
	{
	 return false;
	}

}
//type = A转换日期至标准格式 2010/11/12
//type = B转换日期至常用格式 2010-11-12
function cf_ConvertDate(strDate,type)
{  
   if("A" == type)
       return strDate.toString().replace(/-/g,"/");   
   return strDate.toString().replace("/","-").replace("/","-");
}


/*********************************************************************
* 判断字符串strDate是否为一个正确的日期格式：
* yyyy-M-d或yyyy-MM-dd

* *******************************************************************/
function cf_IsDate(strDate)
{
    // 先判断格式上是否正确
    var regDate = /^(\d{4})-(\d{1,2})-(\d{1,2})$/;
    if (!regDate.test(strDate))
    {
        return false;
    }
    // 将年、月、日的值取到数组arr中，其中arr[0]为整个字符串，arr[1]-arr[3]为年、月、日
    var arr = regDate.exec(strDate);
    
    // 判断年、月、日的取值范围是否正确
    return cf_IsDateCorrect(arr[1], arr[2], arr[3]);
}

// 判断年、月、日的取值范围是否正确
// 注意JavaScript的月份范围为1-12
//日范围在1-31
function cf_IsDateCorrect(nYear, nMonth, nDay)
{
    if (nMonth > 12 || nMonth <= 0)
        return false;
    if (nDay > 31 || nDay <= 0)
        return false;
    switch(nMonth)
    {
        case "1":
        case "01":
        case "3":
        case "03":
        case "5":
        case "05":
        case "7":
        case "07":
        case "8":
        case "08":
        case "10":
        case "12":
            return true;    // 大月，由于已判断过nDay的范围在1-31内，因此直接返回true
        case "4":
        case "04":
        case "6":
        case "06":
        case "9":
        case "09":
        case "11":
            return nDay <= 30;    // 小月，如果小于等于30日返回true
        case "2":
        case "02":
             break;
    }
    
    if (nDay <= 28)
        return true;
    if (cf_IsLeapYear(nYear))
        return true;
    return false;
}

// 是否为闰年，规则：四年一闰，百年不闰，四百年再闰
function cf_IsLeapYear(nYear)
{
    if (nYear % 4 != 0)
        return false;
    if (nYear % 100 != 0)
        return true;
    return (nYear % 400 == 0);
}

//地址
function cf_IsAddress(handle){
    var pattern = /^[a-zA-Z0-9\u4E00-\u9FA5\-\—\#\＃\－]{2,200}$/;
    if (!pattern.exec(handle)) return false;
    return true;
}

function cf_IsPostCode(handle)
{
  var pattern =	/^\d{6}?$/;
  if (!pattern.exec(handle)) return false;
    return true;
}    


//判断电话号码是否正确
function cf_IsPhone(strPhone)
{
        strPhone=cf_AllTrim(strPhone);
	var phoneRegWithArea = /^[0][1-9]{1}[0-9]{9,10}$/;                 //判断座机
	var phoneRegfenji = /^[0][1-9]{1}[0-9]{9,10}[-－][0-9]{1,8}$/;  //判断分机
	var regMobile =/^[1][0-9]{10}$/;                                       //判断手机
	var prompt = "您输入的电话号码格式不正确或位数不够，格式应如下：\n手机：13888888888或15988888888\n座机：075588888888\n分机：075588888888-8888\n建议输入您的手机号码！"
	if(strPhone.length > 9) 
	{
		if(phoneRegWithArea.test(strPhone) || regMobile.test(strPhone) || phoneRegfenji.test(strPhone))
		{			
			return true;
		}			
		else
		{
			alert(prompt);
			return false;
		}
	}
	else
	{
	    alert('忘了输入区号？');
	    return false;
	}
}

//除去前后空格
function cf_Trim(str)
{
   return str.replace(/(^\s+)|(\s+$)/g,""); 
}

//除去所有空格
function cf_AllTrim(str)
{
   return str.replace(/\s+/g,""); 
}