# ===========================================================================
#    Import Modules
# ===========================================================================

import pymel.core as pmc
import maya.mel

# ===========================================================================
#    Progress Bar
# ===========================================================================

class ProgressBar(object):


    def __init__(self, value, title, pb_window=False):

        #   Type of progress br
        self.progress_bar = 'progressBar'
        if not pb_window:
            self.progress_bar = maya.mel.eval('$tmp = $gMainProgressBar')

        self.pb_value = value
        self.pb_title = title

        if self.pb_value > 1:
            self.create()
        else:
            self.progress_bar = None

    #    Create Progress Bar
    def create(self):

        pb = pmc.progressBar(
            self.progress_bar,
            edit=True,
            beginProgress=True,
            isInterruptable=True,
            status='%s : 0/%s' % (self.pb_title , self.pb_value),
            maxValue=self.pb_value,
        )


    #    Update Progress Bar
    def update(self, idx_value):

        if not self.progress_bar:
            return

        if isinstance(idx_value, basestring):
            idx_value = int(idx_value)

        # progress Bar
        if idx_value >= self.pb_value - 1:
            self.kill()
        else:
            pmc.progressBar(
                self.progress_bar,
                edit=True,
                status='%s : %s/%s' % (self.pb_title, idx_value, self.pb_value),
                progress=idx_value
            )

    def kill(self):

        if not self.progress_bar:
            return
        
        pmc.progressBar(self.progress_bar, edit=True, endProgress=True)
