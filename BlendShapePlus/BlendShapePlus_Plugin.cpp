// =================================================================
//	Load Modules
// =================================================================

#include "BlendShapePlus_Node.h"
#include "BlendShapePlus_Cmd.h"
#include <maya/MFnPlugin.h>


// =================================================================
//	Initialize Plugin | Uninitialize Plugin
// =================================================================

MStatus initializePlugin(MObject obj) {

	MStatus		status;

	MFnPlugin	plugin(
		obj,
		"Rémi Deletrain -- remi.deletrain@gmail.com",
		"1.0",
		"Any"
	);

	status = plugin.registerCommand("blendShapePlus", BlendShapePlus_Cmd::creator);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	status = plugin.registerNode(
		"BlendShapePlus",
		BlendShapePlus_Node::id,
		BlendShapePlus_Node::creator,
		BlendShapePlus_Node::initialize,
		MPxNode::kDeformerNode
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return status;

}


MStatus uninitializePlugin(MObject obj) {

	MStatus     status;
	MFnPlugin	plugin(obj);

	status = plugin.deregisterCommand("blendShapePlus");
	CHECK_MSTATUS_AND_RETURN_IT(status);

	status = plugin.deregisterNode(BlendShapePlus_Node::id);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return status;

}