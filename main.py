from typing import List, Tuple

import numpy as np


class Mesh:
    """
    Handles the Mesh and Boundary Conditions
    """

    DEFAULT_SIZE = 10  # Width and height in terms of number of nodes

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

    def get_node_temp_or_nil(self, x: int, y: int):
        try:
            return self.nodes[self.get_node_id(x, y)].temp[-1]
        except IndexError:
            return 0.0

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
            node.temp.append(initial_guess)

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


def get_temp(
    tau: float, t_node_i: float, t_left=0.0, t_right=0.0, t_top=0.0, t_bottom=0.0
):
    # Driving FDM Equation Without Heat Generation
    # T_Node_i+1 = tau(T_left_i + T_top_i + T_right_i + T_bottom_i) + (1-4tau)(T_Node_i)
    return tau * (t_left + t_top + t_right + t_bottom) + (1 - 4 * tau) * (t_node_i)


def calc_time_iteration(mesh: Mesh, tau: float):
    for x in range(0, mesh.mesh_size):
        for y in range(0, mesh.mesh_size):
            t_left = mesh.get_node_temp_or_nil(x - 1, y)
            t_right = mesh.get_node_temp_or_nil(x + 1, y)
            t_top = mesh.get_node_temp_or_nil(x, y + 1)
            t_bottom = mesh.get_node_temp_or_nil(x, y - 1)
            t_node_i = mesh.nodes[mesh.get_node_id(x, y)].temp[-1]
            mesh.nodes[mesh.get_node_id(x, y)].temp.append(
                get_temp(tau, t_node_i, t_left, t_right, t_top, t_bottom)
            )


def print_mesh_temps(mesh: Mesh, index: int):
    line = ""
    for x in range(0, mesh.mesh_size):
        for y in range(0, mesh.mesh_size):
            line += f"{mesh.get_node_temp_or_nil(x, y):.2f} "
        line += "\n"

    print(line)


if __name__ == "__main__":

    bcs = [(5, 5, 52.2)]
    k = 167  # W/m-k for Aluminium
    density = 2700  # kg/m^3 for Aluminium
    heat_capacity = 0.896  # J/g-k for Aluminium
    total_time = 10  # s
    time_step = 0.1  # s

    tau = k / density / heat_capacity * time_step
    print(f"Tau {tau}")

    mesh = Mesh()
    mesh.init_values(bcs, 21.1)

    calc_time_iteration(mesh, tau)
    print_mesh_temps(mesh, 0)
    calc_time_iteration(mesh, tau)
    print_mesh_temps(mesh, 0)
    calc_time_iteration(mesh, tau)
    print_mesh_temps(mesh, 0)
