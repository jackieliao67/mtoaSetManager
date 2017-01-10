####################################
# Name: Light_Group_Manager        #
# Version: V1.0                    #
# Author: Jackie Liao              #
# Latest Update: 01/10/2017        #
####################################

import maya.cmds as mc

class lightGroupManager(object):

    def __init__(self):
        self.setTreeName = 'lightGroupSetTree'
        self.lgtGrpSetPrefix = 'MtoA_lightGroup_'
        self.lightGroupNum = 20
        self.lightType = mc.itemFilter(byType = ('light','aiAreaLight','aiSkyDomeLight','aiPhotometricLight'))
        self.setColorList = [[.7,.9,1],[.9,.7,.4],[.8,.3,.1],[.2,.6,.2],[.9,.7,.7],[.2,.5,.9],[1,.35,.3],[.5,.5,.9],[1,.9,.5],[.4,.8,.3]]
        self.warningColor = [1,.1,.1]
        # build UI
        self.ui = self.buildUI()

    def buildUI(self,*args):
        # create window
        widget=mc.columnLayout()
        mc.rowLayout(nc = 3, cw3 = (300,300,300), adjustableColumn = 3, cal = [(1,'center'),(2,'center'),(3,'center')],columnAttach=[(1, 'both', 0), (2, 'both', 0),(3,'both',0)])
        mc.button(l='Create Light Group Set', c = self.createLgtGrpSet)
        mc.button(l='Delete Light Group Set', c = self.deleteLgtGrpSet)
        mc.button(l='Refresh', c = self.rebuildSetTree)
        mc.setParent('..')
        mc.separator(h = 10, w = 900)
        mc.setParent('..')
        mc.rowColumnLayout(nc=3,cw=[(1,440),(2,20),(3,440)])
        mc.text(l='LIGHTS')
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
        mc.button(l='Add Light Group Attribute', c = self.addLgtGrpAttr)
        mc.button(l='Delete Light Group Attribute', c = self.deleteLgtGrpAttr)
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
        mc.outlinerEditor( outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, filter= self.lightType )

    def createLgtGrpSet(self,*args):
        self.addLgtGrpAttr()
        setList = self.listLgtGrpSets()
        existLgtGrpNum = []
        if setList:
            for setNode in setList:
                if mc.objExists(setNode+'.mtoa_constant_lightGroup'):
                    lgtGrpNum = mc.getAttr(setNode+'.mtoa_constant_lightGroup')
                    existLgtGrpNum.append(lgtGrpNum)
        idx = 1
        for idx in range(1,self.lightGroupNum+1):
            if idx in existLgtGrpNum:
                continue
            else:
                newLgtGrpSet = mc.sets(name = self.lgtGrpSetPrefix +str(idx))
                mc.addAttr(newLgtGrpSet,ln = "mtoa_constant_lightGroup",sn = "mtoa_constant_lightGroup",at = "long",dv = idx)
                break

        self.rebuildSetTree()

    def deleteLgtGrpSet(self,*args):
        setList = self.selectedSets()
        for node in setList:
            mc.delete(node)
        self.rebuildSetTree()

    def listLgtGrpSets(self):
        listSets = mc.listSets(allSets=True)
        mtoalgtGrpSets = []
        for setNode in listSets:
            if mc.objExists(setNode +".mtoa_constant_lightGroup"):
                mtoalgtGrpSets.append(setNode)
        return mtoalgtGrpSets

    def listLgtGrpSetsMember(self):
        setList = self.listLgtGrpSets()
        setMemberList = []
        for node in setList:
            memberList = mc.sets(node,q=True)
            for member in memberList:
                setMemberList.append(member)
        return setMemberList

    def selectedSets(self,*args):
        setList = self.listLgtGrpSets()
        setTreeName = self.setTreeName
        selSetList = []
        for node in setList:
            selValue = mc.treeView(setTreeName, q = True, isl = node)
            if selValue == 1:
                selSetList.append(node)
        return selSetList

    def selectedMembers(self,*args):
        setList = self.listLgtGrpSets()
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
        setList = self.listLgtGrpSets()
        setTreeName = self.setTreeName
        setColorList = self.setColorList
        warningColor = self.warningColor
        newSetList = []
        newColorDict = {}
        for i in range(1,self.lightGroupNum+1):
            if self.lgtGrpSetPrefix + str(i) in setList:
                newSetList.append(self.lgtGrpSetPrefix + str(i))
                colorNum = (i-1) - ((i-1)/10)*10
                newColorDict.update({self.lgtGrpSetPrefix + str(i) : setColorList[colorNum]})  
        idx = 1
        for node in newSetList:
            setColor = newColorDict[node]
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

    def addLgtGrpAttr(self,*args):
        selList = self.listSelected()
        selLightList = []
        # get mesh list
        for obj in selList:
            objShape = mc.listRelatives(obj,s=True,f=True,type=('light','aiAreaLight','aiSkyDomeLight','aiPhotometricLight'),ad=True)
            if objShape:
                selLightList.append(objShape[0])
            else:
                children = mc.listRelatives(obj,c=True,f=True,ad=True)
                for child in children:
                    childShape = mc.listRelatives(child,s=True,f=True,type=('light','aiAreaLight','aiSkyDomeLight','aiPhotometricLight') ,ad=True)
                    if childShape:
                        selLightList.append(childShape[0])
        # add attribute to selected meshes
        for lgt in selLightList:
            if not mc.objExists(lgt+'.mtoa_constant_lightGroup'):
                mc.addAttr(lgt,ln = "mtoa_constant_lightGroup",sn = "mtoa_constant_lightGroup",at = "long",dv = -1)

    def deleteLgtGrpAttr(self,*args):
        selList = self.listSelected()
        selLightList = []
        # get mesh list
        for obj in selList:
            objShape = mc.listRelatives(obj,s=True,f=True,type=('light','aiAreaLight','aiSkyDomeLight','aiPhotometricLight'),ad=True)
            if objShape:
                selLightList.append(objShape[0])
            else:
                children = mc.listRelatives(obj,c=True,f=True,ad=True)
                for child in children:
                    childShape = mc.listRelatives(child,s=True,f=True,type=('light','aiAreaLight','aiSkyDomeLight','aiPhotometricLight'),ad=True)
                    if childShape:
                        selLightList.append(childShape[0])
        # add attribute to selected meshes
        for lgt in selLightList:
            if mc.objExists(lgt+'.mtoa_constant_lightGroup'):
                mc.deleteAttr(lgt+'.mtoa_constant_lightGroup')        

    def addItemToSet(self,*args):
        self.addLgtGrpAttr()
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

