from typing import List, Tuple

import matplotlib.cm as cm
import matplotlib.colors as mcol
import matplotlib.pyplot as plt
import numpy as np


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


def get_temp(
    tau: float, t_node_i: float, t_left=0.0, t_right=0.0, t_top=0.0, t_bottom=0.0
):
    # Driving FDM Equation Without Heat Generation
    # T_Node_i+1 = tau(T_left_i + T_top_i + T_right_i + T_bottom_i) + (1-4tau)(T_Node_i)
    return tau * (t_left + t_top + t_right + t_bottom) + (1 - 4 * tau) * (t_node_i)


def calc_time_iteration(mesh: Mesh, tau: float):
    for x in range(0, mesh.mesh_size):
        for y in range(0, mesh.mesh_size):
            t_left = mesh.get_node_temp_or_none(x - 1, y)
            t_right = mesh.get_node_temp_or_none(x + 1, y)
            t_top = mesh.get_node_temp_or_none(x, y + 1)
            t_bottom = mesh.get_node_temp_or_none(x, y - 1)

            # Check if edge or corner boundary and mirror where appropriate
            if t_left is None:
                t_left = t_right
            if t_right is None:
                t_right = t_left
            if t_top is None:
                t_top = t_bottom
            if t_bottom is None:
                t_bottom = t_top

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


def show_plot(mesh: Mesh, time_step: float):
    plt.plot()
    plt.ion()
    plt.show()

    # Create a blue, green, yellow, red colourmap
    cmap = mcol.LinearSegmentedColormap.from_list(
        "MyCmapName", ["b", "#00FF00", "#FFF000", "r"]
    )

    for time_index in range(0, len(mesh.nodes[0].temp)):

        plt.title(f"Temperature for time = {time_step*time_index:.2f}")

        # Generate Z values
        z_vals = np.zeros([mesh.mesh_size, mesh.mesh_size])

        for x in range(0, mesh.mesh_size):
            for y in range(0, mesh.mesh_size):
                z_vals[x, y] = mesh.nodes[mesh.get_node_id(x, y)].temp[time_index]

        im = plt.pcolormesh(
            range(0, mesh.mesh_size), range(0, mesh.mesh_size), z_vals, cmap=cmap
        )

        if time_index == 0:
            # Set the colourmap on the first iteration. This step will contain the minimum and maximum values
            plt.gcf().colorbar(im)

        plt.draw()
        plt.pause(time_step)


if __name__ == "__main__":

    bcs = [(5, 5, 52.2)]
    k = 167  # W/m-k for Aluminium
    density = 2700  # kg/m^3 for Aluminium
    heat_capacity = 0.896  # J/g-k for Aluminium
    total_time = 10  # s
    time_step = 0.1  # s

    tau = k / density / heat_capacity * time_step
    print(f"Tau {tau}")

    mesh = Mesh(25)
    mesh.init_values(bcs, 21.1)

    for _ in range(0, int(total_time / time_step)):
        calc_time_iteration(mesh, tau)

    show_plot(mesh, time_step)
