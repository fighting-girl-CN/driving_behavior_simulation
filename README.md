# A Microscopic Traffic Simulation Project Based on SUMO and TraCI

This project is a microscopic traffic simulation Python project built on **SUMO (Simulation of Urban MObility)** and **TraCI (Traffic Control Interface)**. By introducing differentiated vehicle types, dynamic route generation, and a custom "Humanity" driver behavior layer, the project achieves a realistic simulation of heterogeneous traffic flow.

## 🌟 Core Features & Functions

1. **Vehicle Modeling Parameters (`veh_types.py`)**:
   - Standardizes basic SUMO vehicle attributes and LC2013-based lane-changing parameters into a two-level dictionary structure, facilitating manual configuration of vehicle types.

2. **Custom "Humanity" Driver Behavior Layer (`humanity.py`)**:
   - SUMO's built-in driving and LC2013 lane-changing models cannot achieve the required granularity and multi-factor driving behaviors. Therefore, a Python-based `Humanity` class was implemented via TraCI to work alongside SUMO's built-in driving model, forming a more powerful driving behavior model. Currently, this implements random lane-changing behavior for human drivers, with dimensions such as driver emotions to be implemented in future updates.

3. **Dynamic Routes and Traffic Generation**:
   - To maximize control over traffic flow while reducing the need for manual parameter configuration, the `VehicleCreator` class was developed. It allows automated pre-definition of traffic flows through the configuration of just a few parameters.