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
MObject BlendShapePlus_Node::atargetWeightMap;


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
	CHECK_MSTATUS_AND_RETURN_IT(spaceAttr.setReadable(true));
	CHECK_MSTATUS_AND_RETURN_IT(spaceAttr.setWritable(true));
	CHECK_MSTATUS_AND_RETURN_IT(spaceAttr.setKeyable(true));
	CHECK_MSTATUS_AND_RETURN_IT(spaceAttr.setStorable(true));
	CHECK_MSTATUS_AND_RETURN_IT(spaceAttr.setConnectable(true));
	spaceAttr.addField("world", 0);
	spaceAttr.addField("object", 1);

	//	Add Compound attribute for inputGeo and inputWeight
	MFnCompoundAttribute targetGeoCompoundAttr;
	aTargetGeoCompound = targetGeoCompoundAttr.create("inputTargetGroup", "itg", &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS_AND_RETURN_IT(targetGeoCompoundAttr.setReadable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetGeoCompoundAttr.setWritable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetGeoCompoundAttr.setKeyable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetGeoCompoundAttr.setStorable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetGeoCompoundAttr.setConnectable(true));
	targetGeoCompoundAttr.setArray(true);
	targetGeoCompoundAttr.setUsesArrayDataBuilder(true);


	//	Add inputGeo and set in compound
	MFnTypedAttribute	targetMeshAttr;
	aTargetMesh = targetMeshAttr.create("targetMesh", "im", MFnData::kMesh, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS_AND_RETURN_IT(targetMeshAttr.setReadable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetMeshAttr.setWritable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetMeshAttr.setKeyable(false));
	CHECK_MSTATUS_AND_RETURN_IT(targetMeshAttr.setStorable(false));
	CHECK_MSTATUS_AND_RETURN_IT(targetMeshAttr.setConnectable(true));
	targetGeoCompoundAttr.addChild(aTargetMesh);

	
	//	Add inputWeight and set in compound
	MFnNumericAttribute targetWeightAttr;
	atargetWeight = targetWeightAttr.create("targetWeight", "tw", MFnNumericData::kFloat, 1.0f, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightAttr.setReadable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightAttr.setWritable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightAttr.setKeyable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightAttr.setStorable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightAttr.setConnectable(true));
	targetGeoCompoundAttr.addChild(atargetWeight);


	//	Add inputWeight and set in compound
	MFnNumericAttribute targetWeightMapAttr;
	atargetWeightMap = targetWeightMapAttr.create("weightMap", "twm", MFnNumericData::kFloat, 1.0f, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightMapAttr.setReadable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightMapAttr.setWritable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightMapAttr.setKeyable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightMapAttr.setStorable(true));
	CHECK_MSTATUS_AND_RETURN_IT(targetWeightMapAttr.setConnectable(true));
	targetWeightMapAttr.setArray(true);
	targetGeoCompoundAttr.addChild(atargetWeightMap);


	//	Add Attributes to node
	addAttribute(aSpace);
	addAttribute(aTargetGeoCompound);
	addAttribute(aTargetMesh);
	addAttribute(atargetWeightMap);


	//	Attributes Affects
	attributeAffects(aSpace, outputGeom);
	attributeAffects(aTargetGeoCompound, outputGeom);
	attributeAffects(aTargetMesh, outputGeom);
	attributeAffects(atargetWeightMap, outputGeom);
	

	// Make the deformer weights paintable
	MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer BlendShapePlus weightMap;");

	return MS::kSuccess;

}


// =================================================================
//	Check Connections
// =================================================================

MStatus BlendShapePlus_Node::connectionMade(const MPlug& plug, const MPlug& otherPlug, bool asSrc) {

	if (plug == aTargetMesh) {
		MStatus	status;
		MPlug	sGroup = plug.parent(&status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		int	index = sGroup.logicalIndex();
		// My function
	}

	return MPxNode::connectionMade(plug, otherPlug, asSrc);
}

MStatus BlendShapePlus_Node::connectionBroken(const MPlug& plug, const MPlug& otherPlug, bool asSrc) {

	if (plug == aTargetMesh) {
		MStatus	status;
		MPlug	sGroup = plug.parent(&status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
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
									unsigned int geomIndex
									) {
	
	MStatus status;

	//	Get All positions
	MPointArray	inputPoints;
	itGeo.allPositions(inputPoints);

	MPointArray finalPoints = inputPoints;

	//	Get env data
	float env = data.inputValue(envelope).asFloat();

	//	Input Array data
	MArrayDataHandle targetArray = data.inputArrayValue(aTargetGeoCompound);
	int targetArrayCount = targetArray.elementCount() - 1;

	// =============================================================
	//	Get New Points Position
	// =============================================================
	for (int idx = 0; idx < (int)targetArrayCount; idx++){
		
		targetArray.jumpToElement(idx);
		MDataHandle		targetElement = targetArray.inputValue();
		
		//	Get Weight
		// MFloatArray		weightMap = targetElement.child(atargetWeightMap).asFloat();
		float			weight = targetElement.child(atargetWeight).asFloat();

		//	Get Mesh
		MObject targetMesh = targetElement.child(aTargetMesh).asMesh();
		MFnMesh mfnTargetMesh(targetMesh);

		MPointArray targetPoints;
		mfnTargetMesh.getPoints(targetPoints);

		MString s("\nHODOR ");

		if (inputPoints.length() != targetPoints.length())
			return MS::kSuccess;

		for (int i = 0; i < (int)inputPoints.length(); i++) {
			finalPoints[i] += (targetPoints[i] - inputPoints[i]) * weight * env;
		}

	}

	itGeo.setAllPositions(finalPoints);

	return status;

}