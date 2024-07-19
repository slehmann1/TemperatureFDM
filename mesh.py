from typing import List, Tuple


class Mesh:
    """
    Handles the Mesh and Boundary Conditions
    """

    def __init__(self, mesh_size: int):
        self.mesh_size = mesh_size
        self.nodes = []
        self.elements = []
        self._gen_mesh()

    def _gen_mesh(self):
        id = 0
        for x in range(self.mesh_size):
            for y in range(self.mesh_size):
                if x in [0, self.mesh_size] or y in [0, self.mesh_size]:
                    self.nodes.append(Node(id, x, y, is_boundary_node=True))
                else:
                    self.nodes.append(Node(id, x, y))
                id += 1

    def get_node_temp_or_none(self, x: int, y: int):
        try:
            temp = self.nodes[self.get_node_id(x, y)].temp[-1]
            return temp
        except (IndexError, TypeError):
            return None

    def get_node_id(self, x: int, y: int):
        """Determines the node id in a mesh based on the way the mesh is generated"""
        id = x * self.mesh_size + y
        if id < 0:
            return None
        return id

    def init_values(
        self, boundary_conditions: List[Tuple[int, int, float]], initial_temp: float
    ):
        """Sets the initial values for the mesh

        Args:
            boundary_conditions (List[Tuple[int, int, float]]): In the format x, y, temperature. Only nodes with boundary conditions are specified
            initial_temp float: The value to default all node temperatures to
        """
        # Set all node values
        for node in self.nodes:
            node.temp.append(initial_temp)

        # Set boundary conditions
        for bc_tuple in boundary_conditions:
            node_id = self.get_node_id(bc_tuple[0], bc_tuple[1])
            self.nodes[node_id].temp[0] = bc_tuple[2]
            self.nodes[node_id].is_fixed_temp = True


class Node:

    def __init__(
        self,
        id: int,
        x: float,
        y: float,
        is_fixed_temp: bool = False,
        is_boundary_node=False,
    ) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.is_fixed_temp = is_fixed_temp
        self.temp = []
        self.is_boundary_node = is_boundary_node
