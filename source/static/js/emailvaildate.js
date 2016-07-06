/**
 * Created by DaiLinchuan on 2016/5/19.
 */
 $('#clickbtn').click(function () {

        var secs=30;
         $('#45').css("display", "block");
         $('#clickbtn').css("display", "none");
        for (i = 1; i <= secs; i++) {
            window.setTimeout("update(" + i + ")", i * 1000);
        }
    });
    function update(num) {
         var secs=30;
        if (num == secs) {
             var type1=$('#type1').val();
             if(type1==1){
                window.location.href='http://127.0.0.1:8000/users/setacemail'
             }else{
                window.location.href='http://127.0.0.1:8000/users/acuser'
               }

            $('#senceds').css("display", "none");
            $('#45').css("display", "none");
            $('#clickbtn').css("display", "block");
        }
        else {
            var printnr = secs - num;
            $('#senceds').html('(' + printnr + ')');
            $('#senceds').css("display", "block");
        }
    }