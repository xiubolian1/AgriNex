  //登录js开始
var linkUrl=window.location.href;
         var jump="";
         var name="SHJSSH";
         var ly="";
         var defaultLoginType="";
       
var info;
var total=0;
$(function(){    
    userinfo();
   var mbxdh ="";
   mbxdh = $("#mbxdh").children().text();
   if(mbxdh=="")
   {
     $("li[id='nav01']").attr("class","active");
	 $("a[id='znwd']").attr("href","https://zwdtuser.sh.gov.cn/uc/naturalUser/jumpSendTo.do?redirect_uri=https%3A%2F%2Fzwdt.sh.gov.cn%2Fsmzy%2Fshspace%2Floginsso%2Fin%3Ftype%3Dbsgrfr%26callback%3Dhttps%253A%252F%252Fzwdt.sh.gov.cn%252Fsmzy%252Fqa%252Ftourist%252Fguide%252Fqa%253Ffrom%253Dsy");
   }
   else if(mbxdh.indexOf("要闻动态")>0)
   {
     $("li[id='nav02']").attr("class","active");
	 $("a[id='znwd']").attr("href","https://zwdtuser.sh.gov.cn/uc/naturalUser/jumpSendTo.do?redirect_uri=https%3A%2F%2Fzwdt.sh.gov.cn%2Fsmzy%2Fshspace%2Floginsso%2Fin%3Ftype%3Dbsgrfr%26callback%3Dhttps%253A%252F%252Fzwdt.sh.gov.cn%252Fsmzy%252Fqa%252Ftourist%252Fguide%252Fqa%253Ffrom%253Dywdt");
   }
   else if(mbxdh.indexOf("政务公开")>0)
   {
     $("li[id='nav03']").attr("class","active");
	 $("a[id='znwd']").attr("href","https://zwdtuser.sh.gov.cn/uc/naturalUser/jumpSendTo.do?redirect_uri=https%3A%2F%2Fzwdt.sh.gov.cn%2Fsmzy%2Fshspace%2Floginsso%2Fin%3Ftype%3Dbsgrfr%26callback%3Dhttps%253A%252F%252Fzwdt.sh.gov.cn%252Fsmzy%252Fqa%252Ftourist%252Fguide%252Fqa%253Ffrom%253Dzwgk");
   }
   else if(mbxdh.indexOf("政民互动")>0)
   {
     $("li[id='nav04']").attr("class","active");
	 $("a[id='znwd']").attr("href","https://zwdtuser.sh.gov.cn/uc/naturalUser/jumpSendTo.do?redirect_uri=https%3A%2F%2Fzwdt.sh.gov.cn%2Fsmzy%2Fshspace%2Floginsso%2Fin%3Ftype%3Dbsgrfr%26callback%3Dhttps%253A%252F%252Fzwdt.sh.gov.cn%252Fsmzy%252Fqa%252Ftourist%252Fguide%252Fqa%253Ffrom%253Dzmhd");
   }
   else if(mbxdh.indexOf("走进上海")>0)
   {
     $("li[id='nav05']").attr("class","active");
	 $("a[id='znwd']").attr("href","https://zwdtuser.sh.gov.cn/uc/naturalUser/jumpSendTo.do?redirect_uri=https%3A%2F%2Fzwdt.sh.gov.cn%2Fsmzy%2Fshspace%2Floginsso%2Fin%3Ftype%3Dbsgrfr%26callback%3Dhttps%253A%252F%252Fzwdt.sh.gov.cn%252Fsmzy%252Fqa%252Ftourist%252Fguide%252Fqa%253Ffrom%253Dzjsh");
   }
   else if(mbxdh.indexOf("专题")>0)
   {
     $("li[id='nav03']").attr("class","active");
	 $("a[id='znwd']").attr("href","https://zwdtuser.sh.gov.cn/uc/naturalUser/jumpSendTo.do?redirect_uri=https%3A%2F%2Fzwdt.sh.gov.cn%2Fsmzy%2Fshspace%2Floginsso%2Fin%3Ftype%3Dbsgrfr%26callback%3Dhttps%253A%252F%252Fzwdt.sh.gov.cn%252Fsmzy%252Fqa%252Ftourist%252Fguide%252Fqa%253Ffrom%253Dsy");
   }



});
function userinfo () {
    $.ajax({
        url : "https://zwdtuser.sh.gov.cn/uc/usercenter/userinfo.jsp",
        type : "GET",
        contentType : "application/json; charset=utf-8",
        dataType : "jsonp",
        jsonp: "callback",
        jsonpCallback:"showData",
        async:false,
        success : function(data) {
        }
    })
}

$("#enldyc").load("/enldyc/index.html");
$("#yc").load("/zwgkyc/index.html");
$("#ywdtyc").load("/ywdtyc/index.html",function(){
jQuery.getScript("https://service.shanghai.gov.cn/zqhtml/rdgzxw.js")
}
);
//登录js结束
//document.writeln("<script type=\"text/javascript\" src=\"https://www.shanghai.gov.cn/assets2020/js/jhelper_config.js\"></script>");
 document.writeln("<script type=\"text/javascript\" src=\"https://jhelper.shanghai.gov.cn/publicJS/3100000044.js\"> </script>");
 document.writeln("<script  type=\"text/javascript\" src=\"https://service.shanghai.gov.cn/JianSuo/js/sh_search_service.js\"></script>");
 document.writeln("<script  type=\"text/javascript\" src=\"https://service.shanghai.gov.cn/ywtbdl/js/sh_ywtb.js\"></script>");
 //document.writeln("<script src=\"//gov.govwza.cn/dist/aria.js?appid=be30ca125d0f542b56e3f2cd45359459\" charset=\"utf-8\"></script>");
//关怀版
        var $slb= $('#slb');
        $slb.click(function () {
      schubert.use("trout", function(){
        schubert.trout.doModeInit();
        schubert.trout.doElder('elder');
        document.getElementById("wzagjt").style.display="none";
        document.getElementById("ghb").style.display="none";
        //document.getElementById("wzazzb").style.display="none";
        document.getElementById("zzb").style.display="inline";
      })    
                      });
//无障碍
        //jQuery(document).ready(function () {
            //getToolbarMod();
             //});
//侧边栏js

function testfunc() {
  if(dingyueForm.email.value=="") {
    alert("邮件地址不能为空");
    return false;
  }else if(dingyueForm.email.value.indexOf(" ")!=-1){
    alert("邮件地址Error");
    return false;
  }
  return true;
  }
$(function(){
	$(".share1 ul li").mouseenter(function(){
		$(".share-show").hide();
		$(this).find(".share-show").show();

	});
	$(".share-show").mouseenter(function(e){
		$(this).show();
	});
	$(".share-show").mouseleave(function(e){
		console.log("******",e);
		if(e.relatedTarget == null){
		   e.preventDefault();
		   return;
		}
		$(this).hide();
	});
});

$(function () {
            $(".dropdown ").each(function () {
                if ($(this).find(".dropdown-menu").length > 0)
                    Tabtarget.bind($(this), $(this).find(".dropdown-menu"));
            });
        });
 $(function () {
            $(".sidebar ").each(function () {
                if ($(this).find(".share-show").length > 0)
                    Tabtarget.bind($(this), $(this).find(".share-show"));
            });
        });
//语音js
document.writeln("<script src=\'https://www.shanghai.gov.cn/voice/js/voice-main.js\'></script>");
document.writeln("<script src=\'https://www.shanghai.gov.cn/voice/js/voice-recorder.js\'></script>");



        function voiceHandle(obj){
          if($(obj).hasClass("voice-microphone")){
            var sessionId = $("#sessionId").val();
            var userId="search";
            startRecording(sessionId,userId);
          }
      }
$("#voice-status").on("click", function(){
                voiceHandle(this);
            });
