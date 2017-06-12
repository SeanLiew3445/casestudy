import subprocess_sean, json
from flask import Flask, jsonify, request, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth

cs = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'sean':
		return 'liew'
	return None

@auth.error_handler
def unauthorised():
	return make_response(jsonify( { 'error': 'Unauthorised access' } ), 403)

@cs.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@cs.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

@cs.route('/read/<bridge>', methods=['GET'])
@auth.login_required
def get_read(bridge):
	#check if bridge exists on pc
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)

	return str(subprocess_sean.get_ports(bridge))	

@cs.route('/add', methods=['POST'])
@auth.login_required
def add_port():
	bridge = request.json['bridge']
        port = request.json['port']

	#check if bridge already exists
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)

	#check if interface already exists on pc
	#if len(str(subprocess_sean.int_pc(interface))) == 0:
	#	abort(404)

	if not request.json:
		abort(400)
	if not 'bridge' in request.json and type(request.json['bridge']) != unicode:
		abort(400)
	if not 'port' in request.json and type(request.json['port']) != unicode:
		abort(400)

	subprocess_sean.add_ports(bridge, port)
	return jsonify({'Bridge': bridge,
			'Port': port}), 201

@cs.route('/delete/<bridge>', methods=['DELETE'])
@auth.login_required
def del_port(bridge):
	
	#check if bridge exists
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)

	if not request.json or not 'port' in request.json:
		abort(400)

	port = request.json['port']

	#check if port exists on bridge
	if len(str(subprocess_sean.port_bridge(port))) == 0:
		abort(404)		

	subprocess_sean.del_ports(bridge, port)
	return jsonify({'result': True})

@cs.route('/update/<bridge>/<port>', methods=['PUT'])
@auth.login_required
def update_port(bridge, port):

	#check if bridge exist
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)
	
	#check if port exist on bridge
	if len(str(subprocess_sean.port_bridge(port))) == 0:
		abort(404)

	if not request.json or not 'action' in request.json:
		abort(400)

	action = request.json['action']
	subprocess_sean.update_ports(bridge, port, action)
	return str(subprocess_sean.get_ports(bridge))

if __name__ == '__main__':
	cs.run(debug=True)
