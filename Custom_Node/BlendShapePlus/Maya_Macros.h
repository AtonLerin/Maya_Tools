#define MAYA_CHECK_ERR(status, msg)						\
	if( MStatus::kSuccess != status ) {					\
		MGlobal::displayWarning(msg);					\
		status.perror(msg);								\
		return status;									\
		}

#define MAYA_RETURN_ON_ERR(status, msg)					\
	if( MStatus::kSuccess != status ) {					\
		MGlobal::displayWarning(msg);					\
		status.perror(msg);								\
		return status;									\
		}

#define MAYA_BREAK_ON_ERR(status, msg)					\
	if( MStatus::kSuccess != status ) {					\
		MGlobal::displayWarning(msg);					\
		status.perror(msg);								\
		break;											\
		}

#define MAYA_CONTINUE_ON_ERR(status, msg)				\
	if( MStatus::kSuccess != status ) {					\
		MGlobal::displayWarning(msg);					\
		status.perror(msg);								\
		continue;										\
		}

#define MAYA_MAKE_ERR(status, msg)						\
	status = MStatus::kFailure;							\
	MGlobal::displayWarning(msg);						\
	status.perror(msg);									\
	return status;