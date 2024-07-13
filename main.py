from typing import List, Tuple


class Mesh:
    """
    Handles the Mesh and Boundary Conditions
    """

    DEFAULT_SIZE = 100  # Width and height in terms of number of nodes

    def __init__(self, mesh_size: int = DEFAULT_SIZE):
        self.mesh_size = mesh_size
        self.nodes = []
        self._gen_mesh()

    def _gen_mesh(self):
        id = 0
        for x in range(self.mesh_size):
            for y in range(self.mesh_size):
                self.nodes.append(Node(id, x, y))
                id += 1

    def _get_node_id(self, x: int, y: int):
        """Determines the node id in a mesh based on the way the mesh is generated"""
        return x * self.mesh_size + y

    def init_values(
        self, boundary_conditions: List[Tuple[int, int, float]], initial_guess: float
    ):
        """Sets the initial values for the mesh

        Args:
            boundary_conditions (List[Tuple[int, int, float]]): In the format x, y, temperature. Only nodes with boundary conditions are specified
            initial_guess float: The value to default all node temperatures to
        """
        # Set all node values
        for node in self.nodes:
            node.temp = initial_guess

        # Set boundary conditions
        for bc_tuple in boundary_conditions:
            node_id = self._get_node_id(bc_tuple[0], bc_tuple[1])
            self.nodes[node_id].temp = bc_tuple[2]
            self.nodes[node_id].is_fixed_temp = True


class Node:

    def __init__(
        self, id: int, x: float, y: float, is_fixed_temp: bool = False
    ) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.is_fixed_temp = is_fixed_temp
        self.temp = -1


class Element:
    def __init__(self, nodes: List[Node]) -> None:
        self.nodes = nodes

    def get_mean_temp(self) -> float:
        return sum(node.temp for node in self.nodes) / 4


if __name__ == "__main__":
    pass
