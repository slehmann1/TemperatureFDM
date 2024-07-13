from typing import List, Tuple

import numpy as np


class Mesh:
    """
    Handles the Mesh and Boundary Conditions
    """

    DEFAULT_SIZE = 100  # Width and height in terms of number of nodes

    def __init__(self, mesh_size: int = DEFAULT_SIZE):
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

    def get_node_id(self, x: int, y: int):
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
            node_id = self.get_node_id(bc_tuple[0], bc_tuple[1])
            self.nodes[node_id].temp = bc_tuple[2]
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
        self.temp = -1
        self.is_boundary_node = is_boundary_node


def gen_matrix(mesh: Mesh, tau):
    matrix = np.zeros((mesh.mesh_size**2, mesh.mesh_size**2))
    # Generate equations for all interior elements
    for x in range(2, mesh.mesh_size - 1):
        for y in range(2, mesh.mesh_size - 1):
            matrix_row = np.zeros(mesh.mesh_size**2)

            if mesh.nodes[mesh.get_node_id(x, y)].is_fixed_temp:
                matrix_row[mesh.get_node_id(x, y)] = mesh.nodes[
                    mesh.get_node_id(x, y)
                ].temp

            else:
                # Driving FDM Equation Without Heat Generation
                # T_Node_i+1 = tau(T_left_i + T_top_i + T_right_i + T_bottom_i) + (1-4tau)(T_Node_i)

                matrix_row[mesh.get_node_id(x - 1, y)] = tau
                matrix_row[mesh.get_node_id(x + 1, y)] = tau
                matrix_row[mesh.get_node_id(x, y - 1)] = tau
                matrix_row[mesh.get_node_id(x, y + 1)] = tau
                matrix_row[mesh.get_node_id(x, y)] = 1 - 4 * tau

            matrix[mesh.get_node_id(x, y), :] = matrix_row

    # Generate equations for boundary elements

    return matrix


if __name__ == "__main__":

    bcs = [(21, 37, 52.2)]
    k = 167  # W/m-k for Aluminium
    density = 2700  # kg/m^3 for Aluminium
    heat_capacity = 0.896  # J/g-k for Aluminium
    total_time = 10  # s
    time_step = 0.1  # s

    tau = k / density / heat_capacity * time_step
    print(f"Tau {tau}")

    mesh = Mesh()
    mesh.init_values(bcs, 21.1)

    gen_matrix(mesh, tau)
