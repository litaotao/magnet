

//定义全局loader
var scriptList = document.getElementsByTagName('script') || [];
for (var i = scriptList.length - 1; i >= 0; i--) {
	if (scriptList[i].src.search("loader.js") > 0) {
		window._config = scriptList[i].getAttribute('server');
	};
};

var server = window._config;
if (server[0]!="h") {
	server = "http://"+server;
};