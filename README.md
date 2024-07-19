
# Finite Difference Method For Transient Heat Transfer
#### Analyzes 2D spaces over time using the finite difference method to determine temperatures
<p align="center">
  <img src="https://github.com/slehmann1/TemperatureFDM/blob/master/res/TemperatureFDMDemonstration.gif?raw=true" alt="Temperature Overview"/>
</p>

### Methodology
The finite difference method is a numerical technique that approximates derivatives with finite differences. This methodology can be used to solve the heat equation. A strong overview of this methodology is available [here](https://www.visualslope.com/Library/FDM-for-heat-transfering.pdf). 

### Overview
This program solves the heat equation for two dimensional meshes, making an assumption that boundaries are insulated. It is capable of transient analysis, and uses an explicit formulation to do so.

Currently only fixed temperature boundary conditions and insulated walls are supported. It would be easy to extend this program to add additional cases. The program is designed to be simple and lightweight; more advanced programs are available for solving challenging problems. 

#### Dependencies
Matplotlib and Numpy 
