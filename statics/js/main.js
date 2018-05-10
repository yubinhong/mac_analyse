/**
 * Created by Administrator on 2017/9/15 0015.
 */

function confirmAct(){
        showMask();
        return manage();
}

function manage() {
    var formdata=new FormData($("#form1")[0]);
    $.ajax({
        url: '/',
        type: 'POST',
        data: formdata,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
        success:function (callback) {
            console.log(callback);
            hideMask();
            var advisor_list=JSON.parse(callback);
            var html_ele='';
            $.each(advisor_list,function (index,item) {
                html_ele +='<p>'+item+'</p>';
            });
            console.log(html_ele);
            $('#advisor').html(html_ele);
            $('#myModal').modal('show');
            $("#btn2").removeClass('hide');
        },

    });
}


//显示遮罩层
function showMask(){
    $("#mask").css("height",$(document).height());
    $("#mask").css("width",$(document).width());
    $("#mask").show();
}
//隐藏遮罩层
function hideMask(){

    $("#mask").hide();
}