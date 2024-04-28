###### Flips tool ###############################################
#                                                               #
# 1: Creates the Basic Set for Dynamics. Without configuration. #
# Author: Luis Miguel                                           #
# Version 0.0.1                                                 #
#################################################################

# Get the root "obj" context
root = hou.node("/obj")

# Create geometry Node
# TODO: check if geo node is created
flips_Obj = root.createNode("geo", "FLIPS_TOOL")
color = hou.Color((1,0,0))
flips_Obj.setColor(color)
# Create the Basic Setup for Flips
# Sphere
geo_source = flips_Obj.createNode("sphere", "source")
# FlipSource
flip_source = geo_source.createOutputNode("flipsource")
out_source = flip_source.createOutputNode("null", "OUT_SOURCE")

# DopNetwork
dop_network = out_source.createOutputNode("dopnet", "dopnet_inhouse")

# Dinamics simulation (dopNetwork)

flip_object = dop_network.createNode("flipobject")
volume_source = dop_network.createNode("volumesource")
flip_solver = flip_object.createOutputNode("flipsolver")

gravity = flip_solver.createOutputNode("gravity")

# Connects to the output node
output_node = hou.node("/obj/FLIPS_TOOL/dopnet_inhouse/output")
output_node.setNextInput(gravity)

