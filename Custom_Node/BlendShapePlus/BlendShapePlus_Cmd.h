// =================================================================
// Inlcudes
// =================================================================


#include <maya/MPxCommand.h>

#include <maya/MGlobal.h>
#include <maya/MDagPath.h>
#include <maya/MArgList.h>
#include <maya/MString.h>
#include <maya/MStringArray.h>
#include <maya/MPlug.h>
#include <maya/MSelectionList.h>

#include <maya/MFnNurbsSurface.h>
#include <maya/MFnMesh.h>


// =================================================================
// Node Commande
// =================================================================
class BlendShapePlus_Cmd : public MPxCommand {

public:

	BlendShapePlus_Cmd();
	virtual			~BlendShapePlus_Cmd();

	static void*	creator();

	bool			isUndoable() const;
	MStatus			undoIt();

	MStatus			doIt(const MArgList&);
	MStatus			redoIt();

	MStatus			createNode(MSelectionList& selectionList);

	MStatus			checkName(MString& nodeName, int idx);
	MString			getShortName(MString& nodeName);

public:

	bool			nodeCreated;
	bool			positionSpecified;
	bool			normalSpecified;
	bool			faceIndexSpecified;
	bool			parameterUSpecified;
	bool			parameterVSpecified;

	MString			objectNodeName;
	MString			BlendShapePlusName;

	bool			relative;

	double			parameterU;
	double			parameterV;

};