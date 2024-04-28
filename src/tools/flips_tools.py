# Get the root "obj" context
root = hou.node("/obj")

# Create geometry Node
# TODO: check if geo node is created
flips_obj = root.createNode("geo", "FLIPS_TOOL")
color = hou.Color((1,0,0))
flips_obj.setColor(color)

# Create the Basic Setup for Flips

# Sphere
geo_source = flips_obj.createNode("sphere", "source")
# TODO: promote ty
geo_source.parm("ty").set(2)
geo_source.parm("scale").set(0.2)

# FlipSource
flip_source = geo_source.createOutputNode("flipsource")
out_source = flip_source.createOutputNode("null", "OUT_SOURCE")

# Box bounds for the simulation (reference on DopNetwork>flipSolver)
box_bounds = flips_obj.createNode("box", "box_bounds")
box_bounds.moveToGoodPosition()
box_bounds.parm("sizex").set(4)
box_bounds.parm("sizey").set(4)
box_bounds.parm("sizez").set(4)
box_bounds.parm("ty").setExpression("ch('sizey')/2")

out_bounds = box_bounds.createOutputNode("null", "OUT_BOUNDS")
# TODO: Promote box

# DopNetwork
dop_network = out_source.createOutputNode("dopnet", "dopnet_inhouse")

# Dinamics simulation (dopNetwork)

flip_object = dop_network.createNode("flipobject", "tool_flipsObject")
volume_source = dop_network.createNode("volumesource")
volume_source.moveToGoodPosition()
flip_solver = flip_object.createOutputNode("flipsolver")
flip_solver.setInput(3, volume_source)
gravity = flip_solver.createOutputNode("gravity")

# Connects to the output node
output_node = hou.node("/obj/FLIPS_TOOL/dopnet_inhouse/output")
output_node.setNextInput(gravity)
output_node.moveToGoodPosition()
#output_node.layoutChildren()

# Setup and parameters

# DopNetwork:

# flipObject
voxelParm = hou.FloatParmTemplate("flipObjVoxelSize", "Voxel Size", 1, (1.0,0.0,0.0), default_expression=("ch('particlesep')*ch('gridscale')", "", ""))

# Add parm into node
flip_object.addSpareParmTuple(voxelParm)
flip_object.parm("particlesep").set(0.05)
flip_object.parm("closedends").set(True)
flip_object.parm("surfacetype").set(1)
flip_object.parm("soppath").set("../../OUT_SOURCE")
flip_object.parm("visprim").set(3)

# volumeSource
volume_source.parm("initialize").set(7)
volume_source.parm("soppath").set("../../OUT_SOURCE")
volume_source.parm("sourceparticles").set(True)
# flipSolver
# Box limits, reference to box layout.
flip_solver.parm("limit_sizex").setExpression("bbox('../../OUT_BOUNDS/', D_XSIZE)")
flip_solver.parm("limit_sizey").setExpression("bbox('../../OUT_BOUNDS/', D_YSIZE)")
flip_solver.parm("limit_sizez").setExpression("bbox('../../OUT_BOUNDS/', D_ZSIZE)")

flip_solver.parm("limit_tx").setExpression("ch('../../box_bounds/tx')")
flip_solver.parm("limit_ty").setExpression("ch('../../box_bounds/ty')")
flip_solver.parm("limit_tz").setExpression("ch('../../box_bounds/tz')")

