import subprocess, sys
from flask import Flask, jsonify

#------------------------------------Error Handling---------------------------

def bridge_pc(bridge):
	check = subprocess.Popen(('sudo ovs-vsctl list-br | grep -w ' + bridge), shell=True, stdout=subprocess.PIPE).communicate()[0]
	return check

def int_pc(interface):
        check = subprocess.Popen(('sudo ifconfig | grep -w ' + interface),shell=True, stdout=subprocess.PIPE).communicate()[0]
        return check

def port_bridge(bridge, port):
        check = subprocess.Popen(('sudo ovs-vsctl list-ports ' + bridge + ' | grep ' + port), shell=True, stdout=subprocess.PIPE).communicate()[0]
        return check

def check_mirror(mirror):
        check = subprocess.Popen(('sudo ovs-vsctl list mirror | grep ' + mirror), shell=True, stdout=subprocess.PIPE).communicate()[0]
        return check

#---------------------------PORT-----------------------------------------------

def get_ports(bridge):
	read = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-ports-desc', bridge])
	return read

def add_ports(bridge, port):
	subprocess.call(['sudo', 'ovs-vsctl', '--may-exist', 'add-port', bridge, port])

def del_ports(bridge, port):
	subprocess.call(['sudo', 'ovs-vsctl', '--if-exists', 'del-port', bridge, port])

def update_ports(bridge, port, action):
	subprocess.call(['sudo', 'ovs-ofctl', 'mod-port', bridge, port, action])


#-------------------------------Bridge-----------------------------------------
def get_bridge(bridge):
        read = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'Bridge', bridge])
        return read

def add_bridge(bridge):
        subprocess.call(['sudo', 'ovs-vsctl', '--may-exist', 'add-br', bridge])

def del_bridge(bridge):
        subprocess.call(['sudo', 'ovs-vsctl', '--if-exists', 'del-br', bridge])

def update_bridge(bridge, options):
        subprocess.call(['sudo', 'ovs-vsctl', 'set', 'Bridge', bridge, options])



#--------------------------------Port mirror-----------------------------------

def get_mirror(mirror):
        read = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'mirror', mirror])
        return read

def add_mirror(bridge, port1, port2, port3, port4, name, dest, source, output):
        subprocess.call(['sudo', 'ovs-vsctl', '--', 'set', 'Bridge', bridge, 'mirrors=@m', '--', port1, 'get', 'Port', port2, '--', port3, 'get', 'Port', port4, '--', '--id=@m', 'create', 'Mirror', name, dest, source, output])

def del_mirror(bridge, mirror):
        subprocess.call(['sudo', 'ovs-vsctl', '--', '--id=@m', 'get', 'mirror', mirror, '--', 'remove', 'bridge', bridge, 'mirrors', '@m'])



#---------------------------Netflow--------------------------
def get_netflow(bridge):
        read = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'netflow', bridge])
        return read

def add_netflow(bridge, target, timeout):
        subprocess.call(['sudo', 'ovs-vsctl', '--', 'set', 'Bridge', bridge, 'netflow=@nf', '--', '--id=@nf', 'create', 'NetFlow', target, timeout])

def update_netflow(bridge, options):
        subprocess.call(['sudo', 'ovs-vsctl', 'set', 'NetFlow', bridge, options])

def del_netflow(bridge):
        subprocess.call(['sudo', 'ovs-vsctl', 'clear', 'Bridge', bridge, 'netflow'])

