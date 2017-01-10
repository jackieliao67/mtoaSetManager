####################################
# Name: MtoA_Set_Manager           #
# Version: V1.0                    #
# Author: Jackie Liao              #
####################################

import maya.cmds as mc
import sys
import  maya.mel as mel
sys.path.insert(1,'/USERS/jackiel/workspace/script/maya/mtoaSetManager')

#import dispManager

global gMainWindow
gMainWindow = mel.eval('$tmpVar=$gMainWindow')

class mtoaSetManager(object):

    def __init__(self, parent):
        
        self.buildUI(parent)

    def buildUI(self,*args):
        # create window
        try:
            if mc.window("mtoaSetManager",ex=True):
                mc.deleteUI("mtoaSetManager")
        except:
            print 'cannot delete window'

        mc.window("mtoaSetManager",t="MtoA_Set_Manager", w = 900, sizeable=True, titleBar=True)
        form = mc.formLayout()
        tabs = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        mc.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

        child1 = mc.rowColumnLayout(numberOfColumns=1)
        import idGroupManager
        reload(idGroupManager)
        matteUI = idGroupManager.idGroupManager().ui
        mc.setParent( child1 )        
        mc.setParent( '..' )

        child2 = mc.rowColumnLayout(numberOfColumns=1)        
        import lightGroupManager
        reload(lightGroupManager)
        lightUI = lightGroupManager.lightGroupManager().ui
        mc.setParent( child2 )
        mc.setParent( '..' )

        child3 = mc.rowColumnLayout(numberOfColumns=1)        
        import dispManager
        reload(dispManager)
        dispUI = dispManager.dispManager().ui
        mc.setParent( child3 )
        mc.setParent( '..' )

        mc.tabLayout( tabs, edit=True, tabLabel=((child1, '        ID        '), (child2, ' Light Group '),(child3,'  Displacement  ')))
        mc.showWindow()

def main():
    global gMainWindow
    return mtoaSetManager(gMainWindow)

