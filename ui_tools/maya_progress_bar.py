# ================================================================================
#    Import Modules
# ================================================================================
import pymel.core as pmc
import maya.mel

#===========================================================================
#    Progress Bar
#===========================================================================
class ProgressBar():


    #    Create Progress Bar
    @classmethod
    def create(cls, progressBar_type, value, title):

        # Progress Bar
        if progressBar_type == 0:
            MProgressBar = 'progressBar'
        if progressBar_type == 1:
            MProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

        pmc.progressBar(
            MProgressBar,
            edit=True,
            beginProgress=True,
            isInterruptable=False,
            status='%s : 1/%s' % (title, str(value)),
            maxValue=value,
        )


        return MProgressBar


    #    Update Progress Bar
    @classmethod
    def update(cls, MProgressBar, value, end_value, title):

        # progress Bar
        if value >= end_value - 1:

            pmc.progressBar(
                MProgressBar,
                edit=True,
                endProgress=True
            )

        else:

            pmc.progressBar(
                MProgressBar,
                edit=True,
                status='%s : %s/%s' % (title, value, end_value),
                progress=value
            )