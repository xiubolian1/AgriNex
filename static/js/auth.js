function checkpassword() {
    var password_init = document.getElementById('pwd_init').value;
    var password = document.getElementById("p1").value;
    var repassword = document.getElementById("p2").value;

    if (password_init == password) {
        layer.msg('新密码与初始密码相同！');
        document.getElementById('p1').value = "";
        document.getElementById('p2').value = "";
        document.getElementById('pwd_init').value = "";

    } else if (password != repassword) {
        layer.msg('密码与确认密码不匹配！');
        document.getElementById('p1').value = "";
        document.getElementById('p2').value = "";
        document.getElementById('pwd_init').value = "";
    }
}


var form = document.getElementById('change-form');
form.addEventListener('submit', function (event) {
    // 防止表单默认提交行为
    event.preventDefault();

    // 发送表单数据到后端进行登录操作
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/auth/change_pwd', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                layer.msg('修改成功');
                window.location.href = '/';
            } else {
                layer.msg(response.message);
                document.getElementById("new-captcha").click();
            }
        }
    };
    xhr.send( 'pwd_init=' + form.pwd_init.value + '&pwd_change=' + form.pwd_change.value + '&captcha=' + form.captcha.value);
});
