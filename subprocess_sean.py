import subprocess, sys
from flask import Flask, jsonify

def bridge_pc(bridge):
	show = subprocess.Popen(('sudo ovs-vsctl show | grep ' + bridge), shell=True, stdout=subprocess.PIPE).communicate()[0]
	return show

#---------------------------PORT-----------------------------------------------

def int_pc(interface):
	show = subprocess.Popen(('sudo ifconfig | grep ' + interface),shell=True, stdout=subprocess.PIPE).communicate()[0]
        return show

def port_bridge(port):
	show = subprocess.Popen(('sudo ovs-vsctl show | grep ' + port), shell=True, stdout=subprocess.PIPE).communicate()[0]
        return show

def get_ports(bridge):
	read = subprocess.call(['sudo', 'ovs-ofctl', 'dump-ports-desc', bridge])
	return read

def add_ports(bridge, port):
	add = subprocess.call(['sudo', 'ovs-vsctl', '--may-exist', 'add-port', bridge, port])

def del_ports(bridge, port):
	delete = subprocess.call(['sudo', 'ovs-vsctl', '--if-exists', 'del-port', bridge, port])

def update_ports(bridge, port, action):
	update = subprocess.call(['sudo', 'ovs-ofctl', 'mod-port', bridge, port, action])


#-------------------------------Bridge-----------------------------------------
def get_bridge(bridge):
        read = subprocess.call(['sudo', 'ovs-vsctl', 'list', 'Bridge', bridge])
        return read

def add_bridge(bridge):
        add = subprocess.call(['sudo', 'ovs-vsctl', '--may-exist', 'add-br', bridge])

def del_bridge(bridge):
        delete = subprocess.call(['sudo', 'ovs-vsctl', '--if-exists', 'del-br', bridge])

def update_bridge(bridge, options):
        update = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'Bridge', bridge, options])



#--------------------------------Port mirror-----------------------------------

