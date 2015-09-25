// =================================================================
//	Load Modules
// =================================================================

#include "BlendShapePlus_Node.h"


// =================================================================
//	Init Static Variables
// =================================================================

MTypeId BlendShapePlus_Node::id(0x00000002);

MObject BlendShapePlus_Node::aSpace;
MObject BlendShapePlus_Node::aTargetGeoCompound;
MObject BlendShapePlus_Node::aTargetMesh;
MObject BlendShapePlus_Node::atargetWeight;


// =================================================================
//	Constructor | Destructor | Creator
// =================================================================

BlendShapePlus_Node::BlendShapePlus_Node(){}
BlendShapePlus_Node::~BlendShapePlus_Node(){}

void* BlendShapePlus_Node::creator() {
	return new BlendShapePlus_Node;
}


// =================================================================
//	Node Construction
// =================================================================

MStatus BlendShapePlus_Node::initialize() {

	MStatus status;

	//	Comparison space attribute
	MFnEnumAttribute spaceAttr;
	aSpace = spaceAttr.create("space", "sp", 0, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS(spaceAttr.setReadable(true));
	CHECK_MSTATUS(spaceAttr.setWritable(true));
	CHECK_MSTATUS(spaceAttr.setKeyable(true));
	CHECK_MSTATUS(spaceAttr.setStorable(true));
	CHECK_MSTATUS(spaceAttr.setConnectable(true));
	spaceAttr.addField("world", 0);
	spaceAttr.addField("object", 1);

	//	Add Compound attribute for inputGeo and inputWeight
	MFnCompoundAttribute targetGeoCompoundAttr;
	aTargetGeoCompound = targetGeoCompoundAttr.create("inputTargetGroup", "itg", &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS(targetGeoCompoundAttr.setReadable(true));
	CHECK_MSTATUS(targetGeoCompoundAttr.setWritable(true));
	CHECK_MSTATUS(targetGeoCompoundAttr.setKeyable(true));
	CHECK_MSTATUS(targetGeoCompoundAttr.setStorable(true));
	CHECK_MSTATUS(targetGeoCompoundAttr.setConnectable(true));
	targetGeoCompoundAttr.setArray(true);
	targetGeoCompoundAttr.setIndexMatters(true);


	//	Add inputGeo and set in compound
	MFnTypedAttribute	targetMeshAttr;
	aTargetMesh = targetMeshAttr.create("targetMesh", "im", MFnData::kMesh, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS(targetMeshAttr.setReadable(true));
	CHECK_MSTATUS(targetMeshAttr.setWritable(true));
	CHECK_MSTATUS(targetMeshAttr.setKeyable(false));
	CHECK_MSTATUS(targetMeshAttr.setStorable(false));
	CHECK_MSTATUS(targetMeshAttr.setConnectable(true));
	targetGeoCompoundAttr.addChild(aTargetMesh);

	
	//	Add inputWeight and set in compound
	MFnNumericAttribute targetWeightAttr;
	atargetWeight = targetWeightAttr.create("inputWeight", "iw", MFnNumericData::kFloat, 0.0f, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS(targetWeightAttr.setReadable(true));
	CHECK_MSTATUS(targetWeightAttr.setWritable(true));
	CHECK_MSTATUS(targetWeightAttr.setKeyable(true));
	CHECK_MSTATUS(targetWeightAttr.setStorable(true));
	CHECK_MSTATUS(targetWeightAttr.setConnectable(true));
	targetGeoCompoundAttr.addChild(atargetWeight);


	//	Add Attributes to node
	addAttribute(aSpace);
	addAttribute(aTargetGeoCompound);
	addAttribute(aTargetMesh);
	addAttribute(atargetWeight);


	//	Attributes Affects
	attributeAffects(aSpace, outputGeom);
	attributeAffects(aTargetGeoCompound, outputGeom);
	attributeAffects(aTargetMesh, outputGeom);
	attributeAffects(atargetWeight, outputGeom);
	

	// Make the deformer weights paintable
	MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer blendNode weights;");

	return MS::kSuccess;

}


// =================================================================
//	Check Connections
// =================================================================

MStatus BlendShapePlus_Node::connectionMade(const MPlug& plug, const MPlug& otherPlug, bool asSrc) {

	if (plug == aTargetMesh) {
		MStatus	status;
		MPlug	sGroup = plug.parent(&status);
		CHECK_MSTATUS(status);
		int	index = sGroup.logicalIndex();
		// My function
	}

	return MPxNode::connectionMade(plug, otherPlug, asSrc);
}

MStatus BlendShapePlus_Node::connectionBroken(const MPlug& plug, const MPlug& otherPlug, bool asSrc) {

	if (plug == aTargetMesh) {
		MStatus	status;
		MPlug	sGroup = plug.parent(&status);
		CHECK_MSTATUS(status);
		int	index = sGroup.logicalIndex();
		// My function
	}

	return MPxNode::connectionBroken(plug, otherPlug, asSrc);

}


// =================================================================
//	Deform // Compute
// =================================================================

MStatus BlendShapePlus_Node::deform(
									MDataBlock& data,
									MItGeometry& itGeo,
									const MMatrix &localToWorldMatrix,
									unsigned int mIndex
									) {
	
	MStatus status;

	//	Get Enveloppe data
	float env = data.inputValue(envelope).asFloat();

	//	Get Input data
	MArrayDataHandle targetArray = data.inputArrayValue(aTargetGeoCompound);
	int targetArrayCount = targetArray.elementCount();

	for (int idx = 0; idx < targetArrayCount; idx++){
		
		targetArray.jumpToElement(idx);
		MDataHandle targetElement = targetArray.inputValue();
		
		//	Get Weight
		float targetWeight = targetElement.child(atargetWeight).asFloat();
		targetWeight *= env;

		//	Get Mesh
		MObject targetMesh = targetElement.child(aTargetMesh).asMesh();

		MFnMesh mfnTargetMesh(targetMesh, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		if (targetMesh.isNull())
			return MS::kSuccess;

		// Get the blend points
		MPointArray targetPoints;
		mfnTargetMesh.getPoints(targetPoints);

		MPoint pt;
		MPoint vPos;
		float w = 0.0f;

		for (; !itGeo.isDone(); itGeo.next()) {

			// Get the input point
			pt = itGeo.position();

			// Get the painted weight value
			w = weightValue(data, mIndex, itGeo.index());

			// Perform the deformation
			pt = pt + (targetPoints[itGeo.index()] - pt) * targetWeight * w;

			// Set the new output point
			itGeo.setPosition(pt);

		}

	}

	return MS::kSuccess;

}
