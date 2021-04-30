"""
This is where the implementation of the plugin code goes.
The PNCodeGen-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
import json

# Setup a logger
logger = logging.getLogger('PNCodeGen')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PNCodeGen(PluginBase):
 def main(self):
    core = self.core
    root_node = self.root_node
    active_node = self.active_node
    name = core.get_attribute(active_node, 'name')
    core.set_attribute(active_node, 'name', 'newName')

    places = [p for p in core.load_children(active_node) if core.is_instance_of(p, 'Place')]
    transitions = [t for t in core.load_children(active_node) if core.is_instance_of(t, 'Transition')]
    arcs = [a for a in core.load_children(active_node) if core.is_instance_of(a, "Inplaces") or core.is_instance_of(a, "Outplaces")]

    logger.info("Places ========")
    logger.info(json.dumps(places, indent=2))
    logger.info("Transitions ========")
    logger.info(json.dumps(transitions, indent=2))
    logger.info("Arcs ========")
    logger.info(json.dumps(arcs, indent=2))

    visited = set()
    states = set()
    graph = {"places": {}, "transitions": {}}

    for t in transitions:
        graph['transitions'][t['nodePath']] = {"parent": [], "children": []} 

    for p in places:
        graph['places'][p['nodePath']] = {"parent":[], "children":[]}

    for a in arcs:
        src = core.get_pointer_path(a, 'src')
        dst = core.get_pointer_path(a, 'dst')
        if dst in graph['transitions']:
            graph['transitions'][dst]['parent'].append(src)
        if dst in graph['places']:
            graph['places'][dst]['parent'].append(src)
        if src in graph['transitions']:
            graph['transitions'][src]['children'].append(dst)
        if src in graph['places']:
            graph['places'][src]['children'].append(dst)
    
    logger.info("Graph ========")
    logger.info(json.dumps(graph, indent=2))
    
    #Parent has only one child and transitions only have one parent
    def is_free_choice(graph):
        for t in graph['transitions']:
            for parent in graph['transitions'][t]['parent']:
                if graph['places'][parent]['children'] != [t]: 
                    if graph['transitions'][t]['parent'] != [parent]:
                        return False
        return True
    
    #Transitions only have one in one out
    def is_state_machine(graph):
        for t in graph['transitions']:
            if len(graph['transitions'][t]['children']) > 1 or len(graph['transitions'][t]['parent']) > 1:
                return False
        return True
    
    def is_marked_graph(graph):
        for p in graph['places']:
            if len(graph['places'][p]['children']) > 1 or len(graph['places'][p]['parent']) > 1:
                return False
        return True

    def is_workflow_net(graph):
        child_transitions = len([t for t in graph['transitions'] if len(graph['transitions'][t]['children']) == 0]) == 0
        parent_transitions = len([t for t in graph['transitions'] if len(graph['transitions'][t]['parent']) == 0]) == 0        
        one_exit = len([p for p in graph['places'] if len(graph['places'][p]['children']) == 0]) == 1
        one_entry = len([p for p in graph['places'] if len(graph['places'][p]['parent']) == 0]) == 1
        return one_exit and one_entry and child_transitions and parent_transitions

    if is_free_choice(graph): self.send_notification("YES -  Free-Choice PetriNet")
    if is_state_machine(graph): self.send_notification("YES - State Machine")
    if is_marked_graph(graph): self.send_notification("YES - Marked Graph")
    if is_workflow_net(graph): self.send_notification("YES - Workflow Net")