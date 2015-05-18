
//validate username and password
//username: email address
//password: at least 8 digits, only containing numbers and digits
function validate(type)
{	// validate user name and password
	// validate username
	if(type == "user")
	{
		var value = document.getElementById('user').value;
		// var reg = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
		var reg = /^\w{2,10}\W{0,1}\w{2,10}$/;
       	var result =  reg.test(value);
		if(!result)
		{
			my_alert("Invalid user name");
			return false;
		}
		var first_second = document.getElementById('pwd_1')['style']['cssText'];
		if (first_second.length != 14) {
			var existed = user_existed(value);
			if (existed != -200) {
				my_alert("user name almost existed, please use another one.");
				return false;
			};
		};
		return true;
	}
	// second validate password
	else if(type=="pwd")
	{
		var value = document.getElementById('pwd').value;
		var reg = /^\w{8,16}$/;
		var result = reg.test(value);
		if(!result){
			my_alert("Invalid password, password should have a length from 8 to 16");
			return false;
		}
		return true;
	}
	else
		return;
}

//post username and password to server
function user_existed(user)
{
	var xmlhttp;
	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function()
  	{
  		if (xmlhttp.readyState==4 && xmlhttp.status==200)
    	{
    		var res = xmlhttp.responseText;
    		var res_dict = eval("(" + res + ")");
    		if(res_dict["code"] == 200)
    		{
    			my_alert(res_dict["data"]);
    			return res_dict['code'];
    		}
    		else if(res_dict["code"] == -200)
    		{
    			my_alert(res_dict["data"]);
    			return res_dict['code'];
    		}
    		else 
    			return res_dict['code'];
    	}
  	}
	// xmlhttp.open("POST", tmp, true);
	xmlhttp.open("POST", server+"/validate", true);
	xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	content = "user="+user;
	xmlhttp.send(content);
}

//valite whether the repeated passwords are the same or not.
//It's the show time when new user come to register.
function repeat_judge()
{
	pwd = document.getElementById('pwd').value;
	pwd_1 = document.getElementById('pwd_1').value;
	if (pwd_1 != pwd) {
		my_alert("password not agree");
		document.getElementById('pwd_1').value = "";
	};
}

//for new user come to register
function register()
{
	var first_second = document.getElementById('pwd_1')['style']['cssText'];
	document.getElementById('login').disabled = true;
	if (first_second.length == 14) {
		document.getElementById('pwd_1')['style']['cssText'] = "display:";
		document.getElementById('user').value = "";
		document.getElementById('pwd').value = "";
	}else{
		var post_data = {};
		post_data["user"] = document.getElementById('user').value;
		post_data["pwd"] = document.getElementById('pwd').value;
		var xmlhttp;
		if (window.XMLHttpRequest) {
			xmlhttp = new XMLHttpRequest();
		}else{
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		}

		xmlhttp.onreadystatechange = function(){
			if (xmlhttp.readyState==4 && xmlhttp.status==200) {
				// my_alert("success");
				var res = xmlhttp.responseText;
				var res_dict = eval("(" + res + ")");
				my_alert(res_dict['data']);
				document.getElementById('login').disabled = false;
				document.getElementById('pwd_1')['style']['cssText'] = "display:none";
			};
		}
		xmlhttp.open("POST", server+"/register", true);
		xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
		xmlhttp.send(JSON.stringify(post_data));
	}
}

function my_alert(msg){
	scrollBy(0, -1000);
	$("#error").fadeIn(3000);
	document.getElementById("error_msg").innerText = msg;
	$("#error").fadeOut(3000);
}

function login_success(){
	var error = document.getElementById("error_msg").innerText;
	if (error=="") {
		return;
	}else{
		my_alert(error);
	}
}