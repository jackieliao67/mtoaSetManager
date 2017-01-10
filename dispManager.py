####################################
# Name: Displacement_Set_Manager   #
# Version: V1.0                    #
# Author: Jackie Liao              #
# Latest Update: 01/10/2017        #
####################################

import maya.cmds as mc

class dispManager(object):

    def __init__(self):
        self.setTreeName = 'dispSetTree'
        self.dispSetPrefix = 'MtoA_displacement_set1'
        self.setColor = [.7,.9,1]
        self.warningColor = [1,.1,.1]
        # build UI
        self.ui = self.buildUI()

    def buildUI(self,*args):
        # create window
        widget=mc.columnLayout()
        mc.rowLayout(nc = 3, cw3 = (300,300,300), adjustableColumn = 3, cal = [(1,'center'),(2,'center'),(3,'center')],columnAttach=[(1, 'both', 0), (2, 'both', 0),(3,'both',0)])
        mc.button(l='Create Displacement Set', c = self.createDispSet)
        mc.button(l='Delete Displacement Set', c = self.deleteDispSet)
        mc.button(l='Refresh', c = self.rebuildSetTree)
        mc.setParent('..')
        mc.separator(h = 10, w = 900)
        mc.setParent('..')
        mc.rowColumnLayout(nc=3,cw=[(1,440),(2,20),(3,440)])
        mc.text(l='OBJECTS')
        mc.text(l='')
        mc.text(l='SETS')
        mc.frameLayout( labelVisible=False, w = 440,h = 500)
        self.buildObjectTree()
        mc.setParent('..')
        mc.setParent('..')
        mc.columnLayout(cw = 20,cal = 'center', columnAttach = ('both',0))
        mc.text(l='')
        mc.setParent('..')
        mc.frameLayout( labelVisible=False, w = 440,h = 500)
        self.createSetTreeLayout()
        self.buildSetTree()
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')
        mc.rowLayout(nc = 3, cw3 = (440,20,440), adjustableColumn = 3, cal = [(1,'center'),(2,'center'),(3,'center')],columnAttach=[(1, 'both', 0), (2, 'both', 0),(3,'both',0)])
        mc.button(l=' Add To Set      ==== > ', c = self.addItemToSet)
        mc.text('')
        mc.button(l=' < ====      Remove From Set ', c = self.removeItemFromSet)
        mc.setParent('..')
        mc.separator(h = 15, w = 900)
        mc.rowLayout(nc = 3, cw3 = (300,300,300), adjustableColumn = 3, cal = [(1,'center'),(2,'center'),(3,'center')],columnAttach=[(1, 'both', 0), (2, 'both', 0),(3,'both',0)])
        mc.text("")
        return widget

    def listSelected(self):
        listSelected = mc.ls(sl=True,l=True)
        selList = []
        for node in listSelected:
            selList.append(node)
        return selList

    def buildObjectTree(self):
        panel = mc.outlinerPanel(menuBarVisible=False)
        outliner = mc.outlinerPanel(panel, query=True, outlinerEditor=True)
        mc.outlinerEditor( outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, filter='DefaultGeometryFilter' )

    def createDispSet(self,*args):
        newDispSet = mc.sets(name = self.dispSetPrefix)
        ## Subdivision
        type_enumItems = "none=0:catclark=1:linear=2"
        mc.addAttr(newDispSet, ln = "aiSubdivType", niceName = "Type", at = "enum", enumName=type_enumItems, k=True, r=True, dv = 0)
        mc.addAttr(newDispSet, ln = "aiSubdivIterations", niceName = "Iterations", at = "byte", r=True, hxv=True, max=100, dv=0)
        metric_enumItems = "auto=0:edge_length=1:flatness=2"
        mc.addAttr(newDispSet, ln = "aiSubdivAdaptiveMetric", niceName = "Adaptive Metric", at = "enum", enumName=metric_enumItems, k=True, r=True, dv = 0)
        mc.addAttr(newDispSet, ln = "aiSubdivPixelError", niceName = "Pixel Error", at = "float", r=True, dv=0.0) #missing slider
        #mc.addAttr(newDispSet, ln = "aiSubdivDicingCamera", niceName = "Dicing Camera", at = "message", r=True)
        smooth_enumItems = "pin_corners=0:pin_borders=1:linear=2:smooth=3"
        mc.addAttr(newDispSet, ln = "aiSubdivUvSmoothing", niceName = "UV Smoothing", at = "enum", enumName=smooth_enumItems, k=True, r=True, dv = 0)
        mc.addAttr(newDispSet, ln = "aiSubdivSmoothDerivs", niceName = "Smooth Tangents", at = "bool", r=True, dv=False)
        ## Displacement Attributes
        mc.addAttr(newDispSet, ln = "aiDispHeight",niceName = "Height", at = "float", r=True, dv=1.0)
        mc.addAttr(newDispSet, ln = "aiDispPadding", niceName = "Bounds Padding", at = "float", r=True, dv=0.0)
        mc.addAttr(newDispSet, ln = "aiDispZeroValue",niceName = "Scalar Zero Value", at = "float", r=True, dv=0.0)
        mc.addAttr(newDispSet, ln = "aiDispAutobump",niceName = "Auto Bump", at = "bool", r=True, dv=False)
        self.rebuildSetTree()

    def deleteDispSet(self,*args):
        setList = self.selectedSets()
        for node in setList:
            mc.delete(node)
        self.rebuildSetTree()

    def listDispSets(self):
        listSets = mc.listSets(allSets=True)
        mtoaDispSets = []
        for setNode in listSets:
            if mc.objExists(setNode +".aiDispHeight"):
                mtoaDispSets.append(setNode)
        return mtoaDispSets

    def listDispSetsMember(self):
        setList = self.listDispSets()
        setMemberList = []
        for node in setList:
            memberList = mc.sets(node,q=True)
            for member in memberList:
                setMemberList.append(member)
        return setMemberList

    def selectedSets(self,*args):
        setList = self.listDispSets()
        setTreeName = self.setTreeName
        selSetList = []
        for node in setList:
            selValue = mc.treeView(setTreeName, q = True, isl = node)
            if selValue == 1:
                selSetList.append(node)
        return selSetList

    def selectedMembers(self,*args):
        setList = self.listDispSets()
        setTreeName = self.setTreeName
        selMemberList = []
        for node in setList:
            memberList = mc.treeView(setTreeName, q = True, ch = node)
            for member in memberList:
                if member not in setList:
                    selValue = mc.treeView(setTreeName, q = True, isl = member)
                    if selValue == 1:
                        selMemberList.append(member)
        return selMemberList

    def createSetTreeLayout(self):
        setTreeName = self.setTreeName
        layout = mc.formLayout()
        setTree = mc.treeView(setTreeName, parent = layout, abr = False)
        mc.formLayout(layout, e = True, attachForm=(setTree,'top',2))
        mc.formLayout(layout, e = True, attachForm=(setTree,'left',2))
        mc.formLayout(layout, e = True, attachForm=(setTree,'bottom',2))
        mc.formLayout(layout, e = True, attachForm=(setTree,'right',2))

    def buildSetTree(self):
        setList = self.listDispSets()
        setTreeName = self.setTreeName
        setColor = self.setColor
        warningColor = self.warningColor
        
        idx = 1
        for node in setList:
            mc.treeView (setTreeName, e = True, addItem = (node,''))
            mc.treeView (setTreeName, e = True, fn = (node,"boldLabelFont"), tc = (node,setColor[0],setColor[1],setColor[2]))
            memberList = mc.sets(node,q=True)
            
            if memberList:
                for member in memberList:
                    memberExist = mc.treeView(setTreeName, q = True, iex=member)
                    if memberExist == 1:
                        memberAdj = member + ' ('+str(idx+1)+ ')'
                        idx += 1
                        mc.treeView (setTreeName, e = True, addItem = (memberAdj,node))
                        mc.treeView (setTreeName, e = True, tc = (memberAdj,warningColor[0],warningColor[1],warningColor[2]))
                    else:
                        mc.treeView (setTreeName, e = True, addItem = (member,node))
            

    def rebuildSetTree(self,*args):
        setTreeName = self.setTreeName
        mc.treeView(setTreeName, e = True, ra = True)
        self.buildSetTree()      

    def addItemToSet(self,*args):
        selList = self.listSelected()
        selSetList = self.selectedSets()
        for setNode in selSetList:
            for selNode in selList:
                mc.sets(selNode, add = setNode)
        self.rebuildSetTree()

    def removeItemFromSet(self,*args):
        selMemberList = self.selectedMembers()
        setTreeName = self.setTreeName
        for member in selMemberList:
            if len(member.split('(')) > 1:
                memberName = member.split('(')
                parentSet = mc.treeView(setTreeName, q = True, ip =member)
                mc.sets(memberName[0], rm = parentSet)
            else:
                parentSet = mc.treeView(setTreeName, q = True, ip =member)
                mc.sets(member, rm = parentSet)
        self.rebuildSetTree()
