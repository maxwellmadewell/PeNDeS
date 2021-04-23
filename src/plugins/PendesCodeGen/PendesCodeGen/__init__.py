"""
MAX COURSEY
Vanderbilt University - CS6388

This is where the implementation of the plugin code goes.
The PendesCodeGen-class is imported from both run_plugin.py and run_debug.py

TRAVERSES PETRINET MODEL AND CREATE STRUCTURED DATA MODEL
"""

########## LIBRARIES ##########
import sys
import logging
from webgme_bindings import PluginBase

#TODO - mxm addl libs

###############################

# Setup a logger
logger = logging.getLogger('PendesCodeGen')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PendesCodeGen(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
	META = self.META
        active_node = self.active_node # we assume the active node is the state machine node

        graph = {}
        places = set()
        transitions = set()
        inplaces = []
        outplaces = []

        # we build the most simple graph representation possible
        nodes = core.load_children(active_node)

        for node in nodes:
            if core.is_type_of(node, META['Place']):
                places.add(core.get_path(node))
	    elif core.is_type_of(node, META['Transition']):
		transitions.add(core.get_path(node))  #TODO - not sure if I need this 
        
	for node in nodes:
            if core.is_type_of(node, META['Inplaces']):
                src = core.get_pointer_path(node, 'src')
                dst = core.get_pointer_path(node, 'dst')
                inplaces.add({'src': src, 'dst': dst})
                if src in graph:
                    graph[src].append(dst)
                else:
                    graph[src] = [dst]

            elif core.is_type_of(node, META['Outplaces']):
                src = core.get_pointer_path(node, 'src')
                dst = core.get_pointer_path(node, 'dst')
                outplaces.add({'src': src, 'dst': dst})
                if src in graph:
                    graph[src].append(dst)
                else:
                    graph[src] = [dst]
        

