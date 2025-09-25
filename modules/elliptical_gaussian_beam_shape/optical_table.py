from .beam import EllipticalGaussianBeam
from .elliptical_lens import EllipticalLens

from typing import List
from collections import deque

class OpticalTable:

    nodes: List['Node']
    nodes_dict: dict

    beam_paths: List['BeamPath']
    beam_paths_dict: dict

    def __init__(self):
        self.nodes = []
        self.nodes_dict = {}

        self.beam_paths = []
        self.beam_paths_dict = {}

    def add_node(self, id: str = None) -> str:
        if id is None:
            id = f"node_{len(self.nodes)}"
        assert id not in self.nodes_dict.keys(), f"A node with this id: '{id}' already exists in the object."

        n = Node(id = id)
        self.nodes.append(n)
        self.nodes_dict[id] = n
        return id
    
    def get_nodes(self) -> dict:
        return dict(self.nodes_dict)
    
    def get_node(self, id: str) -> 'Node':
        return self.nodes_dict.get(id)
    
    def connect_two_nodes(self, id1: str, id2: str, distance: float):
        assert id1 in self.nodes_dict.keys(), f"A node with this id: {id1} does not exist in the object."
        assert id2 in self.nodes_dict.keys(), f"A node with this id: {id2} does not exist in the object."

        n1, n2 = self.get_node(id1), self.get_node(id2)
        n1.connect_to_node(n2, distance)

    def add_beam_path(self, b: EllipticalGaussianBeam, node_id: str, beam_path_id: str = None, forward: bool = True) -> str:
        if beam_path_id is None:
            beam_path_id = f"beam_{len(self.beam_paths)}"
        assert beam_path_id not in self.beam_paths_dict.keys(), f"The beam with the id: '{beam_path_id} already exists in the object."
        
        n = self.get_node(node_id)
        assert n is not None, f"A node with this id: {node_id} does not exist in the object."
        
        b2 = EllipticalGaussianBeam.copy(b)
        bpath = BeamPath(beam_path_id, b2, n, forward)

        self.beam_paths.append(bpath)
        self.beam_paths_dict[beam_path_id] = bpath

        return beam_path_id

    def evolve_beams(self):
        for path_id in self.beam_paths_dict.keys():
            self._evolve_beam_path(path_id)
            
    def _evolve_beam_path(self, id: str):
        beam_path: BeamPath = self.beam_paths_dict.get(id)
        assert beam_path is not None, f"The beam path with id: {id} has not been defined in this object."

        beam: EllipticalGaussianBeam = beam_path.get_beam()
        node: Node = beam_path.get_initial_node()
        
        q = deque()
        
        q.append((node, EllipticalGaussianBeam.copy(beam)))
        while len(q) > 0:
            node, beam = q.popleft()
            node.add_beam(id, beam)

            beam = node.get_beam(id)
            index = beam_path.is_forward()
            edges = node.get_forward_edges() if beam_path.is_forward() else node.get_backward_edges()
            for edge in edges:
                beam_evolved: EllipticalGaussianBeam = EllipticalGaussianBeam.copy(beam)
                beam_evolved.evolve(edge.get_distance())
                q.append((
                    edge.get_nodes()[index], beam_evolved
                ))


class BeamPath:

    id: str
    initial_beam: EllipticalGaussianBeam
    initial_node: 'Node'
    forward: bool

    def __init__(self, id: str, b: EllipticalGaussianBeam, initial_node: 'Node', forward: bool = True):
        self.id = id
        self.initial_beam = b
        self.initial_node = initial_node
        self.forward = forward

    def get_id(self) -> str:
        return self.id

    def is_forward(self) -> bool:
        return self.forward
    
    def get_initial_node(self) -> 'Node':
        return self.initial_node
    
    def get_beam(self) -> EllipticalGaussianBeam:
        return self.initial_beam


class Node:

    id: str
    forward_edges: List['Edge']
    backward_edges: List['Edge']
    elliptical_lenses = List[EllipticalLens]
    beams_dict: dict
    
    def __init__(self, id: str):
        self.id = id
        self.forward_edges = []
        self.backward_edges = []
        self.elliptical_lenses = []
        self.beams_dict = {}

    def get_id(self) -> str:
        return self.id

    def add_elliptical_lens(self, l: EllipticalLens):
        self.elliptical_lenses.append(l)

    def connect_to_node(self, n2: 'Node', distance: float):
        e = Edge(self, n2, distance)
        self.add_forward_edge(e)
        n2.add_backward_edge(e)

    def get_forward_edges(self):
        return self.forward_edges
    
    def get_backward_edges(self):
        return self.backward_edges
    
    def add_forward_edge(self, e: 'Edge'):
        self.forward_edges.append(e)

    def add_backward_edge(self, e: 'Edge'):
        self.backward_edges.append(e)

    def add_beam(self, id: str, b: EllipticalGaussianBeam):
        b = EllipticalGaussianBeam.copy(b)
        for l in self.elliptical_lenses:
            b.apply_elliptical_lens(l)
        self.beams_dict[id] = b

    def get_beam(self, id: str) -> EllipticalGaussianBeam:
        return self.beams_dict.get(id)
    
    def get_beams(self) -> dict:
        return dict(self.beams_dict)

class Edge:

    n1: Node
    n2: Node
    distance: float

    def __init__(self, n1: 'Node', n2: 'Node', distance: float):
        self.n1 = n1
        self.n2 = n2
        self.distance = distance

    def get_nodes(self):
        return self.n1, self.n2
    
    def get_distance(self):
        return self.distance