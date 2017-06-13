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

	return jsonify({'Port': subprocess_sean.get_ports(bridge).splitlines()})	

@cs.route('/add/port/<bridge>', methods=['POST'])
@auth.login_required
def add_port(bridge):
      
	#check if bridge already exists
	if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
		abort(404)

	if not request.json:
		abort(400)

	if not 'port' in request.json or type(request.json['port']) != unicode:
		abort(400)
	
	port = request.json['port']

        #check if interface already exists on pc
        if len(str(subprocess_sean.int_pc(port))) == 0:
                abort(404)

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

	return jsonify({'Result': True})

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
			'Action': action})

#-------------------------------Bridge-----------------------------------------

@cs.route('/read/bridge/<bridge>', methods=['GET'])
@auth.login_required
def get_bridge(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        return jsonify({'Bridge': subprocess_sean.get_bridge(bridge).splitlines()})

@cs.route('/add/bridge/<bridge>', methods=['POST'])
@auth.login_required
def add_bridge(bridge):

        #check if bridge already exists
        if len(str(subprocess_sean.bridge_pc(bridge))) != 0:
                abort(404)

        subprocess_sean.add_bridge(bridge)
        return jsonify({'Bridge': bridge}), 201

@cs.route('/delete/bridge/<bridge>', methods=['DELETE'])
@auth.login_required
def del_bridge(bridge):

        #check if bridge exists
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        subprocess_sean.del_bridge(bridge)
        return jsonify({'Result': True})

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
			'Options': options})


#----------------------------------Port mirror---------------------------------

@cs.route('/read/mirror/<mirror>', methods=['GET'])
@auth.login_required
def get_mirror(mirror):
	
	#check if mirror exists
	if len(str(subprocess_sean.check_mirror(mirror))) == 0:
		abort(404)

        return jsonify({'Mirror': subprocess_sean.get_mirror(mirror).splitlines()})
	
@cs.route('/add/mirror/<bridge>', methods=['POST'])
@auth.login_required
def add_mirror(bridge):

        #check if bridge already exists
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(400)
	
        if not request.json or not 'port1' in request.json:
                abort(400)

        if not request.json or not 'port2' in request.json:
                abort(400)
      
	if not request.json or not 'port3' in request.json:
                abort(400)

        if not request.json or not 'port4' in request.json:
                abort(400)

        if not request.json or not 'name' in request.json:
                abort(400)

        if not request.json or not 'dest' in request.json:
                abort(400)

        if not request.json or not 'source' in request.json:
                abort(400)

        if not request.json or not 'output' in request.json:
                abort(400)
	
        port1 = request.json['port1']
	port2 = request.json['port2']
	port3 = request.json['port3']
        port4 = request.json['port4']
        name = request.json['name']
        dest = request.json['dest']
        source = request.json['source']
        output = request.json['output']

        #check if port already exists
        if len(str(subprocess_sean.int_pc(port2))) == 0:
                abort(404)

        if len(str(subprocess_sean.int_pc(port4))) == 0:
                abort(404)

        #check if port exist on bridge
        if len(str(subprocess_sean.port_bridge(bridge, port2))) == 0:
                abort(404)

        if len(str(subprocess_sean.port_bridge(bridge, port4))) == 0:
                abort(404)
	
        if port2 == port4:
                abort(400)

        #check if mirror with same name already exists
        if len(str(subprocess_sean.check_mirror(name))) != 0:
                abort(400)

        subprocess_sean.add_mirror(bridge, port1, port2, port3, port4, name, dest, source, output)

        #check if mirror was added successfully
        if len(str(subprocess_sean.check_mirror(mirror))) == 0:
                abort(400)

        return jsonify({'Bridge': bridge,
			'Name': name,
			'Destination': dest,
			'Source': source,
			'Output': output}), 201


@cs.route('/update/mirror/<bridge>', methods=['PUT'])
@auth.login_required
def update_mirror(bridge):

        #check if bridge already exists
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        if not request.json or not 'port1' in request.json:
                abort(400)

        if not request.json or not 'port2' in request.json:
                abort(400)

        if not request.json or not 'port3' in request.json:
                abort(400)

        if not request.json or not 'port4' in request.json:
                abort(400)

        if not request.json or not 'name' in request.json:
                abort(400)

        if not request.json or not 'dest' in request.json:
                abort(400)

        if not request.json or not 'source' in request.json:
                abort(400)

        if not request.json or not 'output' in request.json:
                abort(400)

        port1 = request.json['port1']
        port2 = request.json['port2']
        port3 = request.json['port3']
        port4 = request.json['port4']
        name = request.json['name']
        dest = request.json['dest']
        source = request.json['source']
        output = request.json['output']

        #check if port already exists
        if len(str(subprocess_sean.int_pc(port2))) == 0:
                abort(404)

        if len(str(subprocess_sean.int_pc(port4))) == 0:
                abort(404)

        #check if port exist on bridge
        if len(str(subprocess_sean.port_bridge(bridge, port2))) == 0:
                abort(404)

        if len(str(subprocess_sean.port_bridge(bridge, port4))) == 0:
                abort(404)

        if port2 == port4:
                abort(400)

        subprocess_sean.add_mirror(bridge, port1, port2, port3, port4, name, dest, source, output)

        return jsonify({'Bridge': bridge,
                        'Name': name,
                        'Destination': dest,
                        'Source': source,
                        'Output': output})


@cs.route('/delete/mirror/<bridge>/<mirror>', methods=['DELETE'])
@auth.login_required
def del_mirror(bridge, mirror):

        #check if bridge exists
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        #check if mirror exists
        if len(str(subprocess_sean.check_mirror(mirror))) == 0:
                abort(404)

        subprocess_sean.del_mirror(bridge, mirror)

        #check if mirror gets deleted successfully
        if len(str(subprocess_sean.check_mirror(mirror))) != 0:
                abort(400)

        return jsonify({'Result': True})

#-------------------------NetFlow----------------------------------------------

@cs.route('/read/netflow/<bridge>', methods=['GET'])
@auth.login_required
def get_netflow(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        return jsonify({'Bridge': bridge,
                        'Netflow': subprocess_sean.get_netflow(bridge).splitlines()})


@cs.route('/update/netflow/<bridge>', methods=['PUT'])
@auth.login_required
def update_netflow(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

	if not request.json or not 'options' in request.json:
		abort(400)

        options = request.json['options']

        subprocess_sean.update_netflow(bridge,options)

        return jsonify({'Bridge': bridge,
                        'Options': options})


@cs.route('/add/netflow/<bridge>', methods=['POST'])
@auth.login_required
def add_netflow(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        if not request.json or not 'target' in request.json:
                abort(400)
        if not request.json or not 'timeout' in request.json:
                abort(400)
	
	target = request.json['target']
        timeout = request.json['timeout']

        subprocess_sean.add_netflow(bridge, target, timeout)

        return jsonify({'Bridge': bridge,
                        'Target': target,
			'Timeout': timeout})


@cs.route('/delete/netflow/<bridge>', methods=['DELETE'])
@auth.login_required
def del_netflow(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_sean.bridge_pc(bridge))) == 0:
                abort(404)

        subprocess_sean.del_netflow(bridge)

        return jsonify({'Result': True})


if __name__ == '__main__':
	cs.run(debug=True)
