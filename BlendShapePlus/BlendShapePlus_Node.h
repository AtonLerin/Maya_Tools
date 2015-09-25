#ifndef BLENDNODE_H
#define BLENDNODE_H


// =================================================================
//	Load Modules
// =================================================================

#include <maya/MPxDeformerNode.h>

#include <maya/MDataBlock.h>
#include <maya/MPointArray.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MGlobal.h>
#include <maya/MItGeometry.h>
#include <maya/MItMeshVertex.h>
#include <maya/MStatus.h>

#include <maya/MFnMesh.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>


// =================================================================
//	Init Class BlendShape Plus
// =================================================================
class BlendShapePlus_Node : public MPxDeformerNode {

	public:

		BlendShapePlus_Node();
		virtual						~BlendShapePlus_Node();

		static void*				creator();
		static MStatus				initialize();

		virtual MStatus				deform(
											MDataBlock& data, MItGeometry& itGeo,
											const MMatrix &localToWorldMatrix,
											unsigned int mIndex
											);

		virtual MStatus				connectionMade(const MPlug& plug, const MPlug& otherPlug, bool asSrc);
		virtual MStatus				connectionBroken(const MPlug& plug, const MPlug& otherPlug, bool asSrc);


	public:

		static MTypeId				id;
		static MObject				aSpace;
		static MObject				aTargetGeoCompound;
		static MObject				aTargetMesh;
		static MObject				atargetWeight;

};

#endif