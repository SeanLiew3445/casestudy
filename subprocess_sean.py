import subprocess, sys
from flask import Flask, jsonify

def bridge_pc(bridge):
	check = subprocess.Popen(('sudo ovs-vsctl list-br | grep ' + bridge), shell=True, stdout=subprocess.PIPE).communicate()[0]
	return check

#---------------------------PORT-----------------------------------------------

def int_pc(interface):
	check = subprocess.Popen(('sudo ifconfig | grep ' + interface),shell=True, stdout=subprocess.PIPE).communicate()[0]
        return check

def port_bridge(bridge, port):
	check = subprocess.Popen(('sudo ovs-vsctl list-ports ' + bridge + ' | grep ' + port), shell=True, stdout=subprocess.PIPE).communicate()[0]
        return check

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

