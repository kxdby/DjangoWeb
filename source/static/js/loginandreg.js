/**
 * Created by DaiLinchuan on 2016/5/5.
 */
 <!-- js端 验证账号密码格式-->
    function IsEmpty(usdate,padate,loginerroe) {
        var regMail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
        if ( usdate== '' || usdate == undefined || usdate == null) {
           loginerroe.css("display", "block");
           loginerroe.html("账号不可为空");
            return false;
        } else if (!usdate.match(regMail)){
           loginerroe.css("display", "block");
            loginerroe.html("账号格式错误");
             return false;
        }
        else{
                     loginerroe.css("display", "block");
                     if (padate == '' || padate == undefined || padate == null) {

                       loginerroe.html("密码不可为空");

                          return false;
                    } else if (padate.length<6 || padate.length>10){

                       loginerroe.html("密码必须在6-10位");
                          return false;
                    }
            }
        return true;
    }


<!-- aja服务端登录验证 用户 是否可以登录 -->
   function autoComplete(usdate,padate,logi){
                $('#source_url').val();
                $.post(logi,{'email':usdate,'password':padate},function(data){
               if(data.code=="success"){
                           window.location.reload();
                             }else if(data.code=="notemail") {
                                window.location.href='http://127.0.0.1:8000/users/acuser'
                           }else{
                                $('.tips-error').css("display", "block");
                                $('.tips-error').html(data.message);
               }
                });
   }

<!-- 验证码-->
   function  IsCapt(capt,reg_error){
       if ( capt== '' || capt == undefined || capt == null){
            reg_error.css("display", "block");
            reg_error.html("验证码不可为空");
            return false;
       }else{
           return true;
       }
   }

<!-- aja服务端注册验证 用户 是否可以登录 -->
   function autocapt(usdate,padate,capt,login){
                $('#source_url').val();
                $.post(login,{'email':usdate,'password':padate,'capt':capt},function(data){
               if(data.code=="success"){
                           window.location.href='http://127.0.0.1:8000/users/acuser'
                             }else{
                                $('.tips-error').css("display", "block");
                                $('.tips-error').html(data.message);
                           }
                });
   }

function IsEmail(email,forgeterroe){

    var regMail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
    if(!email.match(regMail)){
     forgeterroe.css("display", "block");
     forgeterroe.html('账号格式错误');
      return false;
    }else{
         forgeterroe.css("display", "none");
        return true;
    }


}

<!-- aja服务端注册验证 用户 是否可以登录 -->
function  forgetemail(email,forgeterroe,forget){
     $.post(forget,{'email':email},function(data){
               forgeterroe.css("display", "block");
               if(data.code=="success"){
                          <!-- 提示邮件   改-->
                    window.location.href='http://127.0.0.1:8000/users/setacemail'

                           setTimeout(function(){
                              window.location.reload();},8000
                             );
                             }
                   else if(data.code=="notemail"){

                        window.location.href='http://127.0.0.1:8000/users/acuser'
               }
               else{
                           forgeterroe.html('账号不存在');
                           }
                });
}
