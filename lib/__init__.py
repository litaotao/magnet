
### init flask app
from flask import Flask, request, send_file, Response, render_template
from flask.ext.restful import Api

app = Flask(__name__, static_url_path='/static', static_folder='static',)
app.secret_key = "wow, this girl send a ^_^ to me, what does that mean?"
api = Api(app)

### init config file
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read('../etc/magnet.conf')

server_addr = cf.get('server', 'server_addr')
server_port = int(cf.get('server', 'server_port'))

mongo_host = cf.get('mongo', 'host')
mongo_port = int(cf.get('mongo', 'port'))

debuglog = cf.get('debug', 'debuglog')

allow_user = cf.get('statistic', 'allow')

vote_admin = cf.get('voteAdmin', 'vote_admin')
###
if __name__ == '__main__':
	print allow_user
	print 'yalong.chen' in allow_user
	# app.run(host=server_addr, port=server_port, debug=True)
	# print mongo_host