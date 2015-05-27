/*
获取用户主页数据：
1. 评分排名数据
2. 人脉关系图
*/
function load_data(){
	// my_alert("load done!");
	get_rank();
	var post_data = {};
	// document.getElementById('tag_text').defaultValue = "Please use comma to seperate your tag";
	post_data["name"] = document.getElementById('nickname').innerText.trim();
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
			// my_alert(res);
			is_first_time(res_dict);
			load_option_front(res_dict);
		};
	}
	xmlhttp.open("POST", server+"/classinfo", true);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}

/*
获取用户评分数据
*/
function get_rank(){
	var options = document.getElementById("rank");
	var value = document.getElementById("rank").value;
	var rank_way = options[value].text
	var user = document.getElementById("nickname").innerText.trim();
	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			document.getElementById("rank_res").innerText = res_dict['data'][0] + '/' + res_dict['data'][1];
		};
	}
	xmlhttp.open("GET", [server,"/ranking/",rank_way,"/",user].join(""), false);
	xmlhttp.send();
}


/*
判断用户是否第一次登陆
*/
function is_first_time(res_dict){
	var first_time = res_dict["data"]["first_time"];
	if (!first_time) {
		var tmp_css = document.getElementById('first_time');
		tmp_css.classList.remove('first_time');
		tmp_css.innerHTML = tmp_css.innerHTML.replace('first_time', '');
	}
}

//discover function
// step 1. get the post data, as json type
// step 2. post filter criteria to server
// step 3. get the server's response
// step 4. render the response 
function discover(){
	// step 1
	var criteria = {};
	criteria['me'] = document.getElementById("user").innerText.trim();
	criteria['location'] = document.getElementById('location').value;
	var age = document.getElementById('age').value;
	if(age == "unlimited"){
		criteria['age'] = 'unlimited';
	}else{
		age = parseInt(age);
		criteria['age'] = []
		for (var i = 6; i >= 0; i--) {
			criteria['age'].push(age+i);
		};
	}
	criteria['gender'] = document.getElementById('gender').value;
	criteria['degree'] = document.getElementById('degree').value;
	criteria['field'] = document.getElementById('field').value;
	criteria['skill'] = document.getElementById('skill').value;
	criteria['hobby'] = document.getElementById('hobby').value;
	criteria['school'] = document.getElementById('school').value;

	// 
	var temp = ['location', 'age', 'gender', 'degree',
				'field', 'skill', 'hobby', 'school'];
	var flag = true;
	for (var i = temp.length - 1; i >= 0; i--) {
		if (criteria[ temp[i] ] != "unlimited") {
			flag = false;
		};
	};

	if(flag){
		my_alert("To find people who are similar to you, you need to choose at least one filter criteria");
		return ;
	}
	// step 2
	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			discover_interactive(res_dict['data']);
		};
	}
	xmlhttp.open("POST", server+"/similar", true);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(criteria));
}

// discover interactive
function discover_interactive(data){
	$('.theme-popover-mask').fadeIn(100);
	$('#discover_form').slideDown(200);
	var name = data['name'];
	var distance = data['distance'];
	for (var i = distance.length - 1; i >= 0; i--) {
		distance[i] = distance[i]*100;
	};
	for (var i = name.length - 1; i >= 0; i=i-2) {
		name[i] = "\n" + name[i];
	};
	discover_model(name, distance);
	// document.getElementById('line').innerHTML = res
}

//
function discover_model(name, distance){
	// 路径配置
	require.config({
	paths:{ 
		'echarts' : '../static/js/echarts',
		'echarts/chart/force' : '../static/js/echarts'
	}
	});
	// 使用
	require(
	[
		'echarts',
		'echarts/chart/bar' 
	],
	function (ec) {
		var myChart = ec.init(document.getElementById('bar')); 
		option = {
	    title : {
	        text: 'The first 10 people similar to you',
	        subtext: 'Get a target?'
	    },
	    tooltip : {
	        trigger: 'axis'
	    },
	    legend: {
	        data:['people']
	    },
	    toolbox: {
	        show : true,
	        feature : {
	            mark : {show: true},
	            dataView : {show: true, readOnly: false},
	            magicType : {show: true, type: ['line', 'bar']},
	            restore : {show: true},
	            saveAsImage : {show: true}
	        }
	    },
	    calculable : true,
	    xAxis : [
	        {
	            type : 'category',
	            'axisLabel':{'interval': 0},
	            data: name
	            // data : ['1','2','3','4','5','6','7','8','9','10','11','12']
	        }
	    ],
	    yAxis : [
	        {
	            type : 'value'
	        }
	    ],
	    series : [
	        {
	            name:'people',
	            type:'bar',
	            data: distance
	            // data:[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
	        }	       
	    ]
	};
		var ecConfig = require('echarts/config');
		function focus(param) {
			var data = param.data;
			var links = option.series[0].links;
			var nodes = option.series[0].nodes;
			if (data.source !== undefined && data.target !== undefined) { //点击的是边
				var sourceNode = nodes[data.source];
				var targetNode = nodes[data.target];
				console.log("选中了边 " + sourceNode.name + ' -> ' + targetNode.name + ' (' + data.weight + ')');
			} else { 
				console.log("选中了" + data.name + '(' + data.value + ')');
			}
			console.log(param);
		}
		myChart.on(ecConfig.EVENT.CLICK, focus)
				myChart.setOption(option); 
		}
	);
}

// get detail information
function details(){
	var user = document.getElementById("user").innerText.trim();
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
			var data = res_dict["data"];
			details_interactive(data);
		};
	}
	xmlhttp.open("POST", server+"/details", false);
	xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	content = "user="+user;
	xmlhttp.send(content);
}

// details interactive
function details_interactive(data){
	$('.theme-popover-mask').fadeIn(100);
	$('#detail_form').slideDown(200);
	var x_data = data['x_data'];
	var world_data = data['world_data'];
	var friend_data = data['friend_data'];
	for (var i = friend_data.length - 1; i >= 0; i--) {
		friend_data[i] = -friend_data[i];
	}
	var mark = data['mark']; 
	var max = data['max'];
	max = Math.max(max, 5);
	details_model(x_data, world_data, friend_data, mark, max);
	// document.getElementById('line').innerHTML = res
}

function details_model(x_data, world_data, friend_data, mark, max){
	// 路径配置
	require.config({
	paths:{ 
		'echarts' : '../static/js/echarts',
		'echarts/chart/force' : '../static/js/echarts'
	}
	});
	// 使用
	require(
	[
		'echarts',
		'echarts/chart/line' 
	],
	function (ec) {
		var myChart = ec.init(document.getElementById('line')); 
		option = {
			title : {
				text: 'Rank Detail',
				subtext: 'Keep going, don\'t settle',
				x: 'center'
			},
			tooltip : {
				trigger: 'axis',
				formatter: function(v) {
	            return v[0][1] + '<br/>'
	                   + v[0][0] + ' : ' + v[0][2] + '<br/>'
	                   + v[1][0] + ' : ' + -v[1][2] + '';}
			},
			legend: {
				data:['world','relation'],
				x: 'left'
			},
			toolbox: {
				show : true,
				feature : {
					mark : {
						show : true,
						lineStyle : {width: 1, color: '#1e90ff', type: 'dashed'
						}
					},
					magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
					restore : {show: true},
					saveAsImage : {show: true},
					dataZoom : {show : true, realtime: true},
				},
			},
			dataZoom : {
		        show : true,
		        realtime : true,
		        start : 0,
		        end : 100
	    	},
			xAxis : [
					{
						type : 'category',
						boundaryGap : false,
						axisLine: {onZero: true},
						data : x_data
					}
			],
			yAxis : [
					{
						name : 'world',
						type : 'value',
						max : max
					},
					{
						name : 'relation',
						type : 'value',
					    // max : 0,
					    min : -10,
					    axisLabel : {formatter: function(v){
							if(v<0)
								return -v;
							else
								return v;}}
					}
			],
			series : [
					{
						name:'world',
						type:'line',
						itemStyle: {normal: {areaStyle: {type: 'default'}}},
						data: world_data,
						markPoint : {
							data: [{name: 'your rank in the world', value: "^_^", xAxis: mark['world'][0].toString(), yAxis: mark['world'][1].toString()}]
						}
					},
					{
						name:'relation',
						type:'line',
						yAxisIndex:1,
						itemStyle: {normal: {areaStyle: {type: 'default'}}},
						data: friend_data,
						markPoint : {data : [{name: 'your rank in the first level relationship', value: "^_^", xAxis: mark['friend'][0].toString(), yAxis: (-mark['friend'][1]).toString()}]}
					}
			]
		};
		var ecConfig = require('echarts/config');
		function focus(param) {
			var data = param.data;
			var links = option.series[0].links;
			var nodes = option.series[0].nodes;
			if (data.source !== undefined && data.target !== undefined) { //点击的是边
				var sourceNode = nodes[data.source];
				var targetNode = nodes[data.target];
				console.log("选中了边 " + sourceNode.name + ' -> ' + targetNode.name + ' (' + data.weight + ')');
			} else { 
				console.log("选中了" + data.name + '(' + data.value + ')');
			}
			console.log(param);
		}
		myChart.on(ecConfig.EVENT.CLICK, focus)
				myChart.setOption(option); 
		}
	);
}

//
function stat(){
	var user = document.getElementById('user').innerText.trim();
	var content = {};
	content["user"] = user;
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
			var available = res_dict["data"]["available"];
			if(available){
				var data = res_dict["data"]["data"];
				stat_interactive(data);
			}else{
				my_alert("Access permission: please contact Admin!");
				return ;
			}
			
		};
	}
	xmlhttp.open("POST", server+"/statistics", false);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(content));
}

//
function stat_interactive(data){
	$('.theme-popover-mask').fadeIn(100);
	$('#stat_form').slideDown(200);
	var name = data[0];
	var scores = data[1];
	for (var i = name.length - 1; i >= 0; i=i-2) {
		name[i] = "\n" + name[i];
	};
	stat_model(name, scores);
}

//
function stat_model(name, scores){
	// 路径配置
	require.config({
	paths:{ 
		'echarts' : '../static/js/echarts',
		'echarts/chart/force' : '../static/js/echarts'
	}
	});
	// 使用
	require(
	[
		'echarts',
		'echarts/chart/bar' 
	],
	function (ec) {
		var myChart = ec.init(document.getElementById('stat'));
		option = {
	    title : {
	        text: 'The first 20 people in your company'
	    },
	    tooltip : {
	        trigger: 'axis'
	    },
	    legend: {
	        data:['score']
	    },
	    toolbox: {
	        show : true,
	        feature : {
	            mark : {show: true},
	            dataView : {show: true, readOnly: false},
	            magicType : {show: true, type: ['line', 'bar']},
	            restore : {show: true},
	            saveAsImage : {show: true}
	        }
	    },
	    calculable : true,
	    xAxis : [
	        {
	            type : 'category',
	            axisLabel:{'interval':0},
	       		data: name
	             // data : ['1','2','3','4','5','6','7','8','9','10','11','12']
	        }
	    ],
	    yAxis : [
	        {
	            type : 'value'
	        }
	    ],
	    series : [
	        {
	            name:'score',
	            type:'bar',
	            data: scores
	            // data:[2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
	        }	       
	    ]
	};
		var ecConfig = require('echarts/config');
		function focus(param) {
			var data = param.data;
			var links = option.series[0].links;
			var nodes = option.series[0].nodes;
			if (data.source !== undefined && data.target !== undefined) { //点击的是边
				var sourceNode = nodes[data.source];
				var targetNode = nodes[data.target];
				console.log("选中了边 " + sourceNode.name + ' -> ' + targetNode.name + ' (' + data.weight + ')');
			} else { 
				console.log("选中了" + data.name + '(' + data.value + ')');
			}
			console.log(param);
		}
		myChart.on(ecConfig.EVENT.CLICK, focus)
				myChart.setOption(option); 
		}
	);
}

// when people click the vote button, this func will be activated
function vote(){
	var user = document.getElementById('user').innerText.trim();
	var content = {};
	content["user"] = user;
	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			var available = res_dict["data"]["available"];
			var admin = res_dict["data"]["admin"]
			// if there is no vote event
			if(available == 0){
				var data = res_dict["data"]["data"];
				my_alert(data);
				vote_interactive(available, data, admin);
			}
			// if there is a current vote event
			// return the current and other votes' information
			else if(available == 1){
				var data = res_dict["data"]["data"];
				// my_alert(data);
				vote_interactive(available, data, admin);
				return ;
			}else{
				return ;
			}
		};
	}
	xmlhttp.open("POST", server+"/vote", false);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(content));
}

//
function vote_interactive(available, data, admin){
	$('.theme-popover-mask').fadeIn(100);
	if(admin){
		$('#vote_form').slideDown(200);
		vote_model(available, data, user="")
	}else{
		$('#vote_form_other').slideDown(200);
		vote_model(available, data, user="_other")
	}
}

//
function vote_model(available, data, user){
	// there is no vote event right here
	if (available == 0) {
		document.getElementById('current_vote'+user).innerText = data;
		document.getElementById('del_vote_button'+user).disabled = true;
	}
	// if there are vote information, stored in data, 
	// we then fill the vote box will these data
	else{
		var current = data["current"];
		var history = data["history"];
		// set the current vote name
		document.getElementById('current_vote'+user).innerHTML = current["name"];
		history.push(current["name"]);
		// set the vote history and make the current vote selected
		var tmp_string = "";
		for (var i = history.length - 1; i >= 0; i--) {
			tmp_string += "<option value='" + history[i] + "'>" + history[i] + "</option>";
		};
		document.getElementById('vote_history'+user).innerHTML = tmp_string;
		var index = history.indexOf(current["name"]);
		document.getElementById('vote_history'+user).options[index].selected = true;
		// set the candidate and its current score and your score and details info
		var candidate_name = current["candidate_name"];
		if (candidate_name.length) {
			var tmp_string = "";
			for (var i = candidate_name.length - 1; i >= 0; i--) {
				var tmp_name = candidate_name[i].replace("-", ".");
				tmp_string += "<option value='" + tmp_name + "'>" + tmp_name + "</option>";
			};
			document.getElementById('candidate_name'+user).innerHTML = tmp_string;
			document.getElementById('candidate_name'+user).options[candidate_name.length - 1].selected = true;
			// set the current candidate's info: scores and detailed information
			var candidate = current["candidate"];
			var me = document.getElementById('user').innerText.trim();
			document.getElementById("current_score"+user).innerText = "Total: " + candidate[candidate_name[0]]["total"];
			if (me in candidate[candidate_name[0]]["score"]) {
				document.getElementById("given_score"+user).placeholder = "Given: " + candidate[candidate_name[0]]["score"][me];
			}
			document.getElementById("candidate_desp_text"+user).innerText = candidate[candidate_name[0]]["desp"];
			var tmp_string = "";
			var winner = current["winner"];
			var num = winner.length;
			for (var i = num - 1; i >= 0; i--) {
				tmp_string += "<tr><td>"+(num-i)+"</td><td>"+winner[i][0]+"</td><td>"+winner[i][1]+"</td></tr>";
			};
			document.getElementById("winner_list"+user).innerHTML = tmp_string;
			// return ;
		};
	}
}

//
function add_vote(){
	if (!document.getElementById('add_vote_box') || !document.getElementById("add_vote_box").value) {
		document.getElementById('current_vote').innerHTML = "<input id='add_vote_box' style='width: 354px;'>"
		document.getElementById('add_vote_box').placeholder = "Create a vote, input the vote name"
	}else{
		var content = {};
		content["vote_name"] = document.getElementById('add_vote_box').value;
		content["add_new_vote"] = 1;
		var xmlhttp;
		if (window.XMLHttpRequest) {
			xmlhttp = new XMLHttpRequest();
		}else{
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		}
		xmlhttp.onreadystatechange = function(){
			if (xmlhttp.readyState==4 && xmlhttp.status==200) {
				var res = xmlhttp.responseText;
				var res_dict = eval("(" + res + ")");
				my_alert(res_dict["data"]);
				return ;
			};
		}
		xmlhttp.open("POST", server+"/create_vote", false);
		xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
		xmlhttp.send(JSON.stringify(content));
	}
}

//
function del_candidate () {
	var post_data = {};
	post_data["candidate_name"] = document.getElementById('candidate_name').value;
	post_data["vote"] = document.getElementById("current_vote").innerText;
	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			my_alert(res_dict["data"]);
			return ;
		};
	}
	xmlhttp.open("POST", server+"/del_candidate", false);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}

//
function score_candidate(){
	var post_data = {};
	post_data["candidate"] = document.getElementById('candidate_name').value.replace('.', '-');
	post_data["vote"] = document.getElementById("current_vote").innerText;
	post_data["name"] = document.getElementById("user").innerText.trim().replace('.', '-');
	post_data["score"] = document.getElementById("given_score").value;

	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			my_alert(res_dict["data"]);
			return ;
		};
	}
	xmlhttp.open("POST", server+"/score_candidate", false);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}

//
function add_candidate(){
	if (!document.getElementById('add_candidate_box') || !document.getElementById("add_candidate_box").value) {
		document.getElementById('current_score').innerHTML = "<input id='add_candidate_box' style='width: 180px;'>"
		document.getElementById('add_candidate_box').placeholder = "input the candidate's name"
		document.getElementById('candidate_desp_text').disabled = false;
		document.getElementById('candidate_desp_text').value = "";
		document.getElementById('candidate_desp_text').placeholder = "Please add the candidate's detail information to help him/her ask votes for support";
	}else{
		var content = {};
		content["vote_name"] = document.getElementById('current_vote').innerHTML;
		content["candidate_name"] = document.getElementById('add_candidate_box').value;
		content["add_new_vote"] = 0;
		var desp = document.getElementById('candidate_desp_text').value;
		if (desp.length<10) {
			my_alert("Detailed descrption for the candidate should at least contains 10 characters");
			return;
		}
		content["candidate_description"] = desp;
		var xmlhttp;
		if (window.XMLHttpRequest) {
			xmlhttp = new XMLHttpRequest();
		}else{
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		}
		xmlhttp.onreadystatechange = function(){
			if (xmlhttp.readyState==4 && xmlhttp.status==200) {
				var res = xmlhttp.responseText;
				var res_dict = eval("(" + res + ")");
				my_alert(res_dict["data"]);
				return ;
			};
		}
		xmlhttp.open("POST", server+"/create_vote", false);
		xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
		xmlhttp.send(JSON.stringify(content));
	}
}

//
function get_candidate(){
	var post_data = {};
	post_data["name"] = document.getElementById("user").innerText.trim();
	post_data["user"] = document.getElementById("candidate_name").value;
	post_data["vote"] = document.getElementById("current_vote").innerText;
	// my_alert(post_data);
	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			// my_alert(res_dict["data"]);
			// res_dict: total, desp, mine
			res_dict = res_dict["data"];
			document.getElementById("current_score").innerText = "Total: " + res_dict["total"];
			document.getElementById("given_score").placeholder = "Given: " + res_dict["mine"];
			document.getElementById("candidate_desp_text").innerText = res_dict["desp"];
			return ;
		};
	}
	xmlhttp.open("POST", server+"/get_candidate", false);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}



//
function load_option_front(res_dict){
	var class_info = res_dict['data'];

	//set field name
	var field_name = class_info['field_name'];
	var tmp_string = "<option value='unlimited'>unlimited</option>";
	for (var i = field_name.length - 1; i >= 0; i--) {
		tmp_string += "<option value='" + field_name[i] + "'>" + field_name[i] + "</option>";
	};
	// tmp_string += "<option value='unlimited'>unlimited</option>";
	document.getElementById('field').innerHTML = tmp_string;

	//set skill, according to field name
	var skill;
	tmp_string = "<option value='unlimited'>unlimited</option>";
	for (var i = field_name.length - 1; i >= 0; i--) {
		skill = class_info['field'][field_name[i]];
		tmp_string += "<option value='" + field_name[i] + "'>" + field_name[i] + "</option>";
		for (var j = skill.length - 1; j >= 0; j--) {
			tmp_string += "<option value='" + skill[j] + "'>" + skill[j] + "</option>";
		};
	};
	// tmp_string += "<option value='unlimited'>unlimited</option>";
	document.getElementById('skill').innerHTML = tmp_string;

	//set hobby
	tmp_string = "<option value='unlimited'>unlimited</option>";
	var hobby = class_info['hobby'];
	for (var i = hobby.length - 1; i >= 0; i--) {
		tmp_string += "<option value='" + hobby[i] + "'>" + hobby[i] + "</option>";
	};
	// tmp_string += "<option value='unlimited'>unlimited</option>";
	document.getElementById('hobby').innerHTML = tmp_string;

	//set school
	tmp_string = "<option value='unlimited'>unlimited</option>";
	var school = class_info['school'];
	for (var i = school.length - 1; i >= 0; i--) {
		tmp_string += "<option value='" + school[i] + "'>" + school[i] + "</option>";
	};
	// tmp_string += "<option value='unlimited'>unlimited</option>";
	document.getElementById('school').innerHTML = tmp_string;
	make_graph(class_info["nodes"], class_info["links"]);
}

//
function make_graph(my_nodes, my_links){
	// 路径配置
	require.config({
		paths:{ 
			'echarts' : '../static/js/echarts',
			'echarts/chart/force' : '../static/js/echarts'
		}
	});
	// 使用
	require(
		[
			'echarts',
			'echarts/chart/force' 
		],
		function (ec) {
			var myChart = ec.init(document.getElementById('main')); 
			option = {
				title : {
					text: 'Magnet Human Relation',
					subtext: 'You are just one node in the boundless human relation net',
					x:'right',
					y:'bottom'
				},
				tooltip : {
					trigger: 'item',
					formatter: '{a} : {b}',
					borderWidth: 1,
					axisPointer: {
									type : 'line',
									lineStyle : {color: '#48b', width: 2, type: 'solid'}
					}
				},
				toolbox: {
					show : true,
					feature : {
						restore : {show: true, title: 'reset'},
						saveAsImage : {show: true, title: 'save as image'},
					}
				},
				legend: {x: 'left', data:[]},
				series : [
				{
					type:'force',
					name : "People",
					categories : [
						{name: 'level 1'},
						{name: 'level 2'},
						{name: 'level 3'},
						{name: 'level 4'},
						{name: 'level 5'}
					],
					itemStyle: {
						normal: {
							label: {
								show: true,
								textStyle: {color: '#800080'}
							},
							nodeStyle : {
								brushType : 'both',
								strokeColor : 'rgba(255,215,0,0.4)',
								lineWidth : 1
							}
						},
						emphasis: {
							label: {show: true},
							nodeStyle : {},
							linkStyle : {}
						}
					},
					minRadius : 15,
					maxRadius : 25,
					density : 0.1,
					attractiveness: 1,
					linkSymbol: 'arrow',
					draggable: true,
					nodes:my_nodes,
					links:my_links
				}
				]
			};

			var ecConfig = require('echarts/config');
			function focus(param) {
				var data = param.data;
				var links = option.series[0].links;
				var nodes = option.series[0].nodes;
				if (data.source !== undefined && data.target !== undefined) { //点击的是边
					var sourceNode = nodes[data.source];
					var targetNode = nodes[data.target];
					console.log("选中了边 " + sourceNode.name + ' -> ' + targetNode.name + ' (' + data.weight + ')');
				} else { 
					console.log("选中了" + data.name + '(' + data.value + ')');
				}
				console.log(param);
			}
			myChart.on(ecConfig.EVENT.CLICK, focus)
					myChart.setOption(option); 
			}
		);	
}

//
function unify(){
	var skill = document.getElementById('skill');
	var field = document.getElementById('field').value;
	for (var i = skill.length - 1; i >= 0; i--) {
		if(skill[i].value == field){
			skill.options[i].selected = true;
			return;
		}
	};
}

//user interactive
function user(){
	$('.theme-popover-mask').fadeIn(100);
	$('#user_form').slideDown(200);
	load_user_info();
}

function load_user_info(){
	var post_data = {};
	// document.getElementById('tag_text').defaultValue = "Please use comma to seperate your tag";
	post_data["name"] = document.getElementById('user').innerText.trim();
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
			var basic = res_dict['data']['basic'];
			document.getElementById('i_pwd').value = basic['pwd'][basic['pwd'].length-1];
			document.getElementById('i_degree').value = basic['degree'];
			document.getElementById('i_age').value = basic['age'];
			document.getElementById('i_field').value = basic['field'];
			document.getElementById('i_gender').value = basic['gender'];
			document.getElementById('i_school').value = basic['school'];
			document.getElementById('i_skill').value = basic['skill'];
			document.getElementById('i_hobby').value = basic['hobby'];
			document.getElementById('i_location').value = basic['location'];
			
			var friend = res_dict['data']['friend'];
			var tmp_string = "<option></option>";
			for (var i = friend.length - 1; i >= 0; i--) {
				tmp_string += "<option value='" + friend[i] + "'>" + friend[i] + "</option>";
			};
			document.getElementById('score_name').innerHTML = tmp_string;
			// get_friend_score();
			// my_alert(res);
			// load_option_front(res_dict);
		};
	}
	xmlhttp.open("POST", server+"/user_info", true);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}

function update_info(){
	// first get the updated information in the user UI
	var post_data = {};
	post_data["name"] = document.getElementById('user').innerText.trim();
	post_data["pwd"] = document.getElementById("i_pwd").value;
	post_data["age"] = document.getElementById("i_age").value;
	post_data["field"] = document.getElementById("i_field").value;
	post_data["gender"] = document.getElementById("i_gender").value;
	post_data["school"] = document.getElementById("i_school").value;
	post_data["location"] = document.getElementById("i_location").value;
	post_data["degree"] = document.getElementById("i_degree").value;
	post_data["skill"] = document.getElementById("i_skill").value;
	post_data["hobby"] = document.getElementById("i_hobby").value;

	// then post it to the server	
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
			// load_option_front(res_dict);
		};
	}
	xmlhttp.open("POST", server+"/update", true);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}

function get_friend_score(){
	//get friend score given by me
	if(document.getElementById('score_name').value.length == 0){
		document.getElementById('friend_score').value = "";
		document.getElementById('friend_score').disabled = true;
		document.getElementById('tag_text').disabled = true;
		document.getElementById('tag_button').disabled = true;
		return;
	}
	document.getElementById('friend_score').disabled = false;
	document.getElementById('tag_text').disabled = false;
	document.getElementById('tag_button').disabled = false;
	var post_data = {};
	post_data["me"] = document.getElementById('user').innerText.trim();
	post_data["friend"] = document.getElementById('score_name').value;
	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			document.getElementById("friend_score").value = res_dict["data"];
		};
	}
	xmlhttp.open("POST", server+"/friend_score", true);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}

//
function score_friend(){
	// pre-process the data
	
	var post_data = {};
	if(document.getElementById('friend_score').disabled){
		try{
			var tmp = document.getElementById('u_score').value.split("+");
			var name = tmp[0].trim();
			var score = parseFloat(tmp[1].trim());
		}catch(err){
			my_alert("Format is invalid, please use USERNAME+SCORE");
			return;
		}
		if (isNaN(score) || score<0 || score>10) {
			my_alert("score can only be digit, and between 0-10, thanks!");
			return;
		};
		post_data["tag"] = [];
	}
	else{
		var name = document.getElementById("score_name").value;
		var score = document.getElementById("friend_score").value;
		var tag = document.getElementById("tag_text").value;
		var reg = /^[A-Za-z,\s\n]*$/;
		if (tag.length<1 || !reg.test(tag)) {
			my_alert("your tag is invalid, please use comma to seperate tags");
			return;
		}
		tag = tag.split(",");
		for (var i = tag.length - 1; i >= 0; i--) {
			tag[i] = tag[i].trim();
		}
		post_data["tag"] = tag;
	}
	// send to server and interactive with the user UI
	post_data["my"] = document.getElementById("user").innerText.trim();
	post_data["friend"] = name;
	post_data["score"] = score;

	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			my_alert(res_dict['data']);
		};
	}
	xmlhttp.open("POST", server+"/score_friend", true);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}

//
function add_delete_friend(add_or_del){
	my_alert("add_or_del friend");
	var post_data = {};
	post_data['me'] = document.getElementById("user").innerText.trim();
	if (add_or_del=="add") {
		post_data['friend'] = document.getElementById("add_name").value;
		post_data['method'] = "add";
	}else{
		post_data['friend'] = document.getElementById("delete_name").value;
		post_data['method'] = "del";
	}

	var xmlhttp;
	if (window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			var res = xmlhttp.responseText;
			var res_dict = eval("(" + res + ")");
			my_alert(res_dict['data']);
			update_after_add_del(add_or_del);
		};
	}
	xmlhttp.open("POST", server+"/manage_friend", true);
	xmlhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xmlhttp.send(JSON.stringify(post_data));
}

function update_after_add_del(add_or_del){
	var tmp = document.getElementById('number_2').innerText.split(' ')[2];
	if (add_or_del=="add") {
		tmp = parseInt(tmp)+1;
	}else{
		tmp = parseInt(tmp)-1;
	}
	document.getElementById('number_2').innerText = "There are " + tmp.toString() + " relationships";
}

//
function my_alert(msg){
	scrollBy(0, -1000);
	$("#error").fadeIn(3000);
	document.getElementById("error_msg").innerText = msg;
	$("#error").fadeOut(3000);
}