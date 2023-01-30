
//集成测试提交执行模块
function vailForm() {
    var obj = document.getElementsByName("iname");
    var check_val = [];
    var xhttp = new XMLHttpRequest();

    for(k in obj){
        if(obj[k].checked){
            check_val.push(obj[k].value);
        }
    }
    if (check_val == "") {
        alert("请选择要执行的模块");
        return false;
    }
    else{
        alert("已执行所选模块，等待执行结果");
    }
    xhttp.open("POST","/integrate",true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(check_val);
}

//返回列表
function fun(){
    obj = document.getElementsByName("iname");
    check_val = [];
    for(k in obj){
        if(obj[k].checked)
            check_val.push(obj[k].value);
    }
     return check_val;
}

//编辑待请求接口给选定的接口赋值
function testbut() {
//    var aa = document.querySelectorAll('#editinter');
//    var obj = document.getElementById("editinter");
    var obj2 = document.getElementsByName("editinter2");
    var res = event['target']['value'];
    console.log(event['target']['value']);
    var modifydata = JSON.stringify({"editId": res});
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/mytest", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("x-requested-with","XMLHttpRequest"); 
    xhttp.send(modifydata);
    //该属性每次变化时会触发
    xhttp.onreadystatechange = function(){
    //若响应完成且请求成功
    if(xhttp.readyState === 4 && xhttp.status === 200){
        console.log("testssss");
        //将字符串类型转为对象
        var result = JSON.parse(xhttp.responseText);
        console.log(result);
        //输出result的数据类型
        //alert(typeof(result));
        //将对象类型转为字符串
        //var result2 = JSON.stringify(result['data']);
        var result2 = result['data'];
        //对字符串进行分割
        //var result3 = result2.toString().split(",");
        document.getElementById("editinter").value=result2[0];
        document.getElementById("emode").value=result2[1];
        document.getElementById("eaddr").value=result2[2];
        document.getElementById("eheader").value=result2[3];
        document.getElementById("eparam").value=result2[4];
        document.getElementById("eoption").value=result2[5];
        document.getElementById("eauthor").value=result2[6];
        document.getElementById("edesc").value=result2[7];
        document.getElementById("eresult").value=result2[8];
        document.getElementById("euserpwd").value=result2[9];
        }
    }
}

//使用伪类实现title属性(未使用)
function onMouseHover(ev) {
        document.styleSheets[0].insertRule('#title::before { left: '+ ev.pageX +'px }', 0);
        document.styleSheets[0].insertRule('#title::after { left: '+ ev.pageX +'px }', 0);
        document.getElementById('title').style.zIndex=9999;
    }
 
    function onMouseOut() {
        document.styleSheets[0].deleteRule(0);
        document.styleSheets[0].deleteRule(0);
}

//文件转码为二进制
function fileBinary() {
    var xhttp = new XMLHttpRequest();
    var input = document.createElement("input");
    var action = "/encodefile"; //上传服务的接口地址
    var form = new FormData();
    input.type = "file";
    input.click();
    input.onchange = function(){
    var file = input.files[0];
    form.append("myf", file); //第一个参数是后台读取的请求key值
    form.append("fileName", file.name);
    form.append("type", "binary"); //实际业务的其他请求参数
    xhttp.open("POST", action);
    xhttp.send(form); //发送表单数据
    xhttp.onreadystatechange = function(){
      if(xhttp.readyState==4 && xhttp.status==200){
        //var resultObj = JSON.parse(xhttp.responseText);
        var resultObj = xhttp.responseText;
        document.getElementById('shade3').classList.remove('hide');
        document.getElementById('moda3').classList.remove('hide');
        document.getElementById('encodedesc').value=resultObj;
      }
       if(xhttp.readyState==4 && xhttp.status==500){alert('导入文件有误');}
    }
  }
}

//文件转码为base64
function fileBase() {
    var xhttp = new XMLHttpRequest();
    var input = document.createElement("input");
    var action = "/encodefile"; //上传服务的接口地址
    var form = new FormData();
    input.type = "file";
    input.click();
    input.onchange = function(){
    var file = input.files[0];
    form.append("myf", file); //第一个参数是后台读取的请求key值
    form.append("fileName", file.name);
    form.append("type", "base64"); //实际业务的其他请求参数
    xhttp.open("POST", action);
    xhttp.send(form); //发送表单数据
    xhttp.onreadystatechange = function(){
      if(xhttp.readyState==4 && xhttp.status==200){
        //var resultObj = JSON.parse(xhttp.responseText);
        var resultObj = xhttp.responseText;
        document.getElementById('shade3').classList.remove('hide');
        document.getElementById('moda3').classList.remove('hide');
        document.getElementById('encodedesc').value=resultObj;
      }
      if(xhttp.readyState==4 && xhttp.status==500){alert('导入文件有误');}
    }
  }
}

//文件转码为字符串,可作为接口参数传递
function fileStr() {
    var xhttp = new XMLHttpRequest();
    var input = document.createElement("input");
    var action = "/encodefile"; //上传服务的接口地址
    var form = new FormData();
    input.type = "file";
    input.click();
    input.onchange = function(){
    var file = input.files[0];
    form.append("myf", file); //第一个参数是后台读取的请求key值
    form.append("fileName", file.name);
    form.append("type", "filestr"); //实际业务的其他请求参数
    xhttp.open("POST", action);
    xhttp.send(form); //发送表单数据
    xhttp.onreadystatechange = function(){
      if(xhttp.readyState==4 && xhttp.status==200){
        //var resultObj = JSON.parse(xhttp.responseText);
        var resultObj = xhttp.responseText;
        document.getElementById('shade3').classList.remove('hide');
        document.getElementById('moda3').classList.remove('hide');
        document.getElementById('encodedesc').value=resultObj;
      }
      if(xhttp.readyState==4 && xhttp.status==500){alert('导入文件有误');}
    }
  }
}
