import subprocess_sean, json
from flask import Flask, jsonify, request, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth

cs = Flask(__name__)
auth = HTTPBasicAuth()


#---------------------------------Error handling-------------------------------

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


#--------------------------------------Port------------------------------------

@cs.route('/read/port/<bridge>', methods=['GET'])
@auth.login_required
def get_port(bridge):
	#check if bridge exists on pc
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)

	return subprocess_sean.get_ports(bridge)	

@cs.route('/add/port/<bridge>', methods=['POST'])
@auth.login_required
def add_port(bridge):
      
	#check if bridge already exists
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)

	#check if interface already exists on pc
	#if len(str(subprocess_sean.int_pc(interface))) == 0:
	#	abort(404)

	if not request.json:
		abort(400)

	if not 'port' in request.json or type(request.json['port']) != unicode:
		abort(400)
	
	port = request.json['port']
	subprocess_sean.add_ports(bridge, port)
	return jsonify({'Bridge': bridge,
			'Port': port}), 201

@cs.route('/delete/port/<bridge>', methods=['DELETE'])
@auth.login_required
def del_port(bridge):
	
	#check if bridge exists
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)

	if not request.json or not 'port' in request.json:
		abort(400)

	port = request.json['port']

	#check if port exists on bridge
	if len(str(subprocess_sean.port_bridge(bridge, port))) == 0:
		abort(404)		

	subprocess_sean.del_ports(bridge, port)
	
	#check if delete was successful
	if len(str(subprocess_sean.port_bridge(bridge, port))) != 0:
		abort(404)	

	return jsonify({'Result': True}), 201

@cs.route('/update/port/<bridge>/<port>', methods=['PUT'])
@auth.login_required
def update_port(bridge, port):

	#check if bridge exist
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)
	
	#check if port exist on bridge
	if len(str(subprocess_sean.port_bridge(bridge, port))) == 0:
		abort(404)

	if not request.json or not 'action' in request.json:
		abort(400)

	action = request.json['action']
	subprocess_sean.update_ports(bridge, port, action)
	return jsonify({'Bridge': bridge,
			'Port': port,
			'Action': action}), 201

#-------------------------------Bridge-----------------------------------------

@cs.route('/read/bridge/<bridge>', methods=['GET'])
@auth.login_required
def get_bridge(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        return subprocess_sean.get_bridge(bridge)

@cs.route('/add/bridge/<bridge>', methods=['POST'])
@auth.login_required
def add_bridge(bridge):

        #check if bridge already exists
        if len(str(subprocess_sean.bridge_pc(bridge))) != 0:
                abort(400)

        subprocess_sean.add_bridge(bridge)
        return jsonify({'Bridge': bridge}), 201

@cs.route('/delete/bridge/<bridge>', methods=['DELETE'])
@auth.login_required
def del_bridge(bridge):

        #check if bridge exists
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        subprocess_sean.del_bridge(bridge)
        return jsonify({'Result': True}), 201

@cs.route('/update/bridge/<bridge>', methods=['PUT'])
@auth.login_required
def update_bridge(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        if not request.json or not 'options' in request.json:
                abort(400)

        options = request.json['options']
        subprocess_sean.update_bridge(bridge,options)

	return jsonify({'Bridge': bridge,
			'Options': options}), 201


#----------------------------------Port mirror---------------------------------

@cs.route('/read/mirror/<bridge>', methods=['GET'])
@auth.login_required
def get_mirror(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        return subprocess_sean.get_bridge(bridge)

@cs.route('/add/mirror/<bridge>', methods=['POST'])
@auth.login_required
def add_mirror(bridge):

        #check if bridge already exists
        if len(str(subprocess_sean.bridge_pc(bridge))) != 0:
                abort(400)

        subprocess_sean.add_bridge(bridge)
        return jsonify({'Bridge': bridge}), 201

@cs.route('/delete/mirror/<bridge>', methods=['DELETE'])
@auth.login_required
def del_mirror(mirror):

        #check if bridge exists
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        subprocess_sean.del_bridge(bridge)
        return jsonify({'Result': True}), 201




if __name__ == '__main__':
	cs.run(debug=True)
