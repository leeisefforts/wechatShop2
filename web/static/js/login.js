;
var user_login_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".logC .do-login").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var login_name = $(".lgD input[name=login_name]").val();
            var login_pwd = $(".lgD input[name=login_pwd]").val();

            if( login_name == undefined || login_name.length < 1){
                common_ops.alert( "请输入正确的登录用户名~~" );
                return;
            }
            if( login_pwd == undefined || login_pwd.length < 1){
                common_ops.alert( "请输入正确的密码~~" );
                return;
            }
            btn_target.addClass("disabled");

        } );
    }
};

$(document).ready( function(){
    user_login_ops.init();
} );