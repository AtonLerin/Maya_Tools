// =================================================================
//	Inlcudes
// =================================================================

#include "BlendShapePlus_Cmd.h"



// =================================================================
//	Constructor | Destructor | Creator
// =================================================================

BlendShapePlus_Cmd::BlendShapePlus_Cmd(){}
BlendShapePlus_Cmd::~BlendShapePlus_Cmd(){}

void* BlendShapePlus_Cmd::creator(){
	return new BlendShapePlus_Cmd;
}


// =================================================================
//	Undo
// =================================================================

// Undoable
bool BlendShapePlus_Cmd::isUndoable() const{
	return true;
}

// Undo
MStatus BlendShapePlus_Cmd::undoIt() {

	if (nodeCreated) {
		MString deleteCmd = "delete ";
		deleteCmd += BlendShapePlusName;
		MGlobal::executeCommand(deleteCmd);
	}

	return MStatus::kSuccess;

}


// =================================================================
//	Do it
// =================================================================
MStatus BlendShapePlus_Cmd::doIt(const MArgList & args) {

	// Initialize private Data
	nodeCreated = positionSpecified = normalSpecified = faceIndexSpecified = parameterUSpecified = parameterVSpecified = false;
	objectNodeName = BlendShapePlusName = "";

	// Parse command argument
	for (unsigned i = 0; i<args.length(); i++) {

		if ((MString("-name") == args.asString(i)) || (MString("-n") == args.asString(i))) {
			BlendShapePlusName = args.asString(++i);
		}

		else {
			MString errorMessage = "Invalid flag: ";
			errorMessage += args.asString(i);
			MGlobal::displayError(errorMessage);
			return MS::kFailure;
		}

	}

	return redoIt();

}


// =================================================================
// Re do it
// =================================================================
MStatus BlendShapePlus_Cmd::redoIt() {

	MStatus status;
	MSelectionList selectionList;
	MDagPath objectDagPath;

	// Check selection
	if (objectNodeName == "") {
		MGlobal::getActiveSelectionList(selectionList);
		if (selectionList.length() == 0) {
			MGlobal::displayError("No transform specified!");
			return MS::kFailure;
		}
	}
	else if (selectionList.add(objectNodeName) == MS::kInvalidParameter) {
		MGlobal::displayError("Specified maya node does not exist!");
		return MS::kFailure;
	}

	selectionList.getDagPath(0, objectDagPath);


	if (objectDagPath.node().hasFn(MFn::kMesh)){
		status = createNode(selectionList);
	}
	else if (objectDagPath.node().hasFn(MFn::kTransform) && objectDagPath.hasFn(MFn::kMesh)){
		status = createNode(selectionList);
	}
	else {
		displayError("Invalid type!  Only a mesh or its transform can be specified!");
		return MStatus::kFailure;
	}

	setResult(status);
	return MS::kSuccess;

}


// =================================================================
//	Other Function
// =================================================================
MStatus BlendShapePlus_Cmd::createNode(MSelectionList& selectionList){

	MStatus status = MS::kSuccess;
	MDagPath geoToDeform;

	//	Check Selection
	if (selectionList.length() == 0){
		MGlobal::displayError("No transform selected!");
		return MS::kFailure;
	}

	else if (selectionList.length() == 1)
		status = selectionList.getDagPath(0, geoToDeform);

	else if (selectionList.length() > 1)
		status = selectionList.getDagPath(selectionList.length() - 1, geoToDeform);

	CHECK_MSTATUS_AND_RETURN_IT(status);

	//	Create BlendShapePlus Node
	MGlobal::executeCommand("select -clear");

	if (BlendShapePlusName == "")
		BlendShapePlusName = geoToDeform.fullPathName() + "BSP";
	checkName(BlendShapePlusName, 0);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MGlobal::displayInfo(BlendShapePlusName);
	getShortName(BlendShapePlusName);
	MGlobal::displayInfo(BlendShapePlusName);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	status = MGlobal::executeCommand("deformer -type BlendShapePlus -name " + BlendShapePlusName + ";");
	CHECK_MSTATUS_AND_RETURN_IT(status);


	//	Add last selectedShape to deformer
	status = MGlobal::executeCommand("deformer -edit -geometry " + geoToDeform.fullPathName() + " " + BlendShapePlusName + ";");
	CHECK_MSTATUS_AND_RETURN_IT(status);

	//	connect selected shape
	/*
	for (int idx = 0; idx < selectionList.length() - 1; idx++){

	}
	*/

	MGlobal::selectByName(BlendShapePlusName);

	return status;

}

MStatus BlendShapePlus_Cmd::checkName(MString& nodeName, int idx) {

	if (MGlobal::selectByName(nodeName) == MS::kFailure)
		return MS::kSuccess;

	idx += 1;
	if (MGlobal::selectByName(nodeName + idx))
		checkName(nodeName, idx);

	nodeName = nodeName + idx;

	MGlobal::executeCommand("select -clear");

	return MS::kSuccess;

}

MString BlendShapePlus_Cmd::getShortName(MString& nodeName) {

	MStringArray nodeNameSplited;
	nodeName.split('|', nodeNameSplited);
	nodeName = nodeNameSplited[nodeNameSplited.length() - 1];

	return nodeName;

}
