import os
import maya.cmds as mc
import mtoa.aovs as aovs



class matteGroupManager(object):

    def __init__(self):
        self.shotName = os.environ.get('SHOT')
        self.setTreeName = 'idGroupSetTree'
        self.idGroupAttr = 'mtoa_constant_idGroup'
        self.idColorAttr = 'mtoa_constant_'+ self.shotName + '_idColor_'
        self.idGroupSetPrefix = self.shotName + '_MtoA_IdGroup_'
        self.idGroupNum = 20
        self.setColorList = [[.7,.9,1],[.9,.7,.4],[.8,.3,.1],[.2,.6,.2],[.9,.7,.7],[.2,.5,.9],[1,.35,.3],[.5,.5,.9],[1,.9,.5],[.4,.8,.3]]
        self.warningColor = [1,.7,.7]
        
        # build UI
        self.ui = self.buildUI()

    def buildUI(self,*args):
        # create window
        widget=mc.columnLayout()
        mc.rowLayout(nc = 3, cw3 = (300,300,300), adjustableColumn = 3, cal = [(1,'center'),(2,'center'),(3,'center')],columnAttach=[(1, 'both', 0), (2, 'both', 0),(3,'both',0)])
        mc.button(l='Create ID Set', c = self.createIdSet)
        mc.button(l='Delete ID Set', c = self.deleteIdSet)
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
        mc.button(l='Add ID Attribute', c = self.addIdAttr)
        mc.button(l='Delete ID Attribute', c = self.deleteIdAttr)
        mc.button(l='Create AOVs', c = self.createCustomAovs)
        return widget

    def listSelected(self):
        listSelected = mc.ls(sl=True,l=True)
        selList = []
        for node in listSelected:
            selList.append(node)
        return selList

    def listIdSets(self):
        listSets = mc.listSets(allSets=True)
        mtoaIdSets = []
        for setNode in listSets:
            if mc.objExists(setNode +'.'+self.idGroupAttr):
                mtoaIdSets.append(setNode)
        return mtoaIdSets

    def listIdSetsMember(self, sets):
        setList = sets
        setMemberList = []
        for node in setList:
            memberList = mc.sets(node,q=True)
            if memberList:
                for member in memberList:
                    setMemberList.append(member)
        return setMemberList

    def listConnectedSets(self,node):
        inputNode = node
        setList = []
        connections = mc.listConnections(inputNode)
        for connect in connections:
            if '_MtoA_IdGroup_' in connect:
                setList.append(connect) 
        return setList

    def selectedSets(self,*args):
        setList = self.listIdSets()
        setTreeName = self.setTreeName
        selSetList = []
        for node in setList:
            selValue = mc.treeView(setTreeName, q = True, isl = node)
            if selValue == 1:
                selSetList.append(node)
        return selSetList

    def selectedMembers(self,*args):
        setList = self.listIdSets()
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

    def getMeshList(self,items):
        inputList = items
        meshList = []
        for obj in inputList:
            objShape = mc.listRelatives(obj,s=True,f=True,type='mesh',ad=True)
            if objShape:
                meshList.append(objShape[0])
            else:
                children = mc.listRelatives(obj,c=True,f=True,ad=True)
                for child in children:
                    childShape = mc.listRelatives(child,s=True,f=True,type='mesh',ad=True)
                    if childShape:
                        meshList.append(childShape[0])
        return meshList

    def buildObjectTree(self):
        panel = mc.outlinerPanel(menuBarVisible=False)
        outliner = mc.outlinerPanel(panel, query=True, outlinerEditor=True)
        mc.outlinerEditor( outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, filter='DefaultGeometryFilter' )

    def buildIdSetDict(self,*args):
        idSetName = {}
        matteGrpNum = self.idGroupNum
        for i in range(1,matteGrpNum*3+1):
            grpNum = (i-1)/3+1
            idx = i-(grpNum-1)*3
            if idx == 1:
                idName = 'id_'+ str(i)
                setName = self.idGroupSetPrefix + str(grpNum) +'_R'
                idSetName.update({idName : setName})
            if idx == 2:
                idName = 'id_'+ str(i)
                setName = self.idGroupSetPrefix + str(grpNum) +'_G'
                idSetName.update({idName : setName})
            if idx == 3:
                idName = 'id_'+ str(i)
                setName = self.idGroupSetPrefix + str(grpNum) +'_B'
                idSetName.update({idName : setName})
        return idSetName

    def createIdSet(self,*args):
        selList = self.listSelected()
        meshList = self.getMeshList(selList)
        self.addIdAttr()
        setList = self.listIdSets()
        idSetDict = self.buildIdSetDict()
        existIdNum = []
        if setList:
            for setNode in setList:
                if mc.objExists(setNode+'.'+self.idGroupAttr):
                    idNum = mc.getAttr(setNode+'.'+self.idGroupAttr)
                    existIdNum.append(idNum)
        idx = 1
        for idx in range(1,self.idGroupNum*3+1):
            if idx in existIdNum:
                continue
            else:
                # create new set
                newIdSet = mc.sets(name = idSetDict['id_'+str(idx)])
                # create id attribute on set
                mc.addAttr(newIdSet,ln = self.idGroupAttr,sn = self.idGroupAttr,at = "long",dv = idx)
                # create color attribute on set
                idColor = newIdSet.split('_')[-1:][0]
                idColorNum = newIdSet.split('_')[-2:][0]
                self.addColorAttr(meshList, idColorNum)
                if not mc.objExists(newIdSet + '.' + self.idColorAttr + idColorNum):
                    if idColor == 'R':
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum, sn = self.idColorAttr + idColorNum, usedAsColor = True, at = 'float3')
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setR', at = 'float', parent = self.idColorAttr + idColorNum, dv = 1)
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setG', at = 'float', parent = self.idColorAttr + idColorNum, dv = 0)
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setB', at = 'float', parent = self.idColorAttr + idColorNum, dv = 0)
                    if idColor == 'G':
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum, sn = self.idColorAttr + idColorNum, usedAsColor = True, at = 'float3')
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setR', at = 'float', parent = self.idColorAttr + idColorNum, dv = 0)
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setG', at = 'float', parent = self.idColorAttr + idColorNum, dv = 1)
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setB', at = 'float', parent = self.idColorAttr + idColorNum, dv = 0)
                    if idColor == 'B':
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum, sn = self.idColorAttr + idColorNum, usedAsColor = True, at = 'float3')
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setR', at = 'float', parent = self.idColorAttr + idColorNum, dv = 0)
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setG', at = 'float', parent = self.idColorAttr + idColorNum, dv = 0)
                        mc.addAttr(newIdSet,ln = self.idColorAttr + idColorNum + '_setB', at = 'float', parent = self.idColorAttr + idColorNum, dv = 1)
                break

        self.rebuildSetTree()

    def deleteIdSet(self,*args):
        setList = self.selectedSets()
        setMembers = self.listIdSetsMember(setList)
        meshList = self.getMeshList(setMembers)
        
        for node in setList:
            mc.delete(node)
        
        self.rebuildSetTree()

    def createSetTreeLayout(self):
        setTreeName = self.setTreeName
        layout = mc.formLayout()
        setTree = mc.treeView(setTreeName, parent = layout, abr = False)
        mc.formLayout(layout, e = True, attachForm=(setTree,'top',2))
        mc.formLayout(layout, e = True, attachForm=(setTree,'left',2))
        mc.formLayout(layout, e = True, attachForm=(setTree,'bottom',2))
        mc.formLayout(layout, e = True, attachForm=(setTree,'right',2))

    def buildSetTree(self):
        setList = self.listIdSets()
        setTreeName = self.setTreeName
        idSetDict = self.buildIdSetDict()
        setColorList = self.setColorList
        warningColor = self.warningColor
        newSetList = []
        newColorDict = {}
        for i in range(1,self.idGroupNum*3+1):
            if idSetDict['id_'+str(i)] in setList:
                newSetList.append(idSetDict['id_'+str(i)])
                colorNum = (i-1)/3 - ((i-1)/3/10)*10
                newColorDict.update({idSetDict['id_'+str(i)] : setColorList[colorNum]})
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

    def addIdAttr(self,*args):
        selList = self.listSelected()
        meshList = self.getMeshList(selList)
        # add attribute to selected meshes
        for mesh in meshList:
            if not mc.objExists(mesh+'.'+self.idGroupAttr):
                mc.addAttr(mesh,ln = self.idGroupAttr,sn = self.idGroupAttr,at = "long",dv = -1)

    def deleteIdAttr(self,*args):
        selList = self.listSelected()
        meshList = self.getMeshList(selList)
        self.deleteColorAttr(meshList)
        # add attribute to selected meshes
        for mesh in meshList:
            if mc.objExists(mesh+'.'+self.idGroupAttr):
                mc.deleteAttr(mesh+'.'+self.idGroupAttr)

    def addColorAttr(self, nodes, number):
        nodeList = nodes
        idColorNum = number
        # add attribute to selected meshes
        for node in nodeList:
            if not mc.objExists(node + '.' + self.idColorAttr + idColorNum):
                mc.addAttr(node, ln = self.idColorAttr + idColorNum, sn = self.idColorAttr + idColorNum, usedAsColor = True, at = 'float3')
                mc.addAttr(node, ln = self.idColorAttr + idColorNum + '_R', at = 'float', parent = self.idColorAttr + idColorNum)
                mc.addAttr(node, ln = self.idColorAttr + idColorNum + '_G', at = 'float', parent = self.idColorAttr + idColorNum)
                mc.addAttr(node, ln = self.idColorAttr + idColorNum + '_B', at = 'float', parent = self.idColorAttr + idColorNum)

    def deleteColorAttr(self, nodes):
        nodeList = nodes
        # add attribute to selected meshes
        for node in nodeList:
            for i in range(1,100):
                if mc.objExists(node + '.' + self.idColorAttr + str(i)):
                    mc.deleteAttr(node + '.' + self.idColorAttr + str(i))

    def addItemToSet(self,*args):
        selList = self.listSelected()
        meshList = self.getMeshList(selList)
        selSetList = self.selectedSets()
        self.addIdAttr()
        for setNode in selSetList:
            for selNode in selList:
                mc.sets(selNode, add = setNode)
                idColorNum = setNode.split('_')[-2:][0]
                self.addColorAttr(meshList, idColorNum)
        self.rebuildSetTree()

    def removeItemFromSet(self,*args):
        selMemberList = self.selectedMembers()
        setTreeName = self.setTreeName
        for member in selMemberList:
            if len(member.split('(')) > 1:
                memberName = member.split(' (')
                meshList = self.getMeshList([memberName[0]])
                parentSet = mc.treeView(setTreeName, q = True, ip =member)
                mc.sets(memberName[0], rm = parentSet)
            else:
                meshList = self.getMeshList(selMemberList)
                parentSet = mc.treeView(setTreeName, q = True, ip =member)
                mc.sets(member, rm = parentSet)
        self.rebuildSetTree()

    def createCustomAovs(self,*args):
        setList = self.listIdSets()
        for node in setList:
            idColor = node.split('_')[-1:][0]
            idColorNum = node.split('_')[-2:][0]
            colorDataNodeName = self.shotName + '_colorData_IdGroup_' + idColorNum
            aovName = self.shotName + '_ID_group_' + idColorNum
            if not mc.objExists(colorDataNodeName):
                colorNode = mc.shadingNode('aiUserDataColor', asShader=True, name = colorDataNodeName)
                mc.setAttr(colorNode+'.colorAttrName', self.shotName + '_idColor_' + idColorNum, type = 'string')
            if not mc.objExists('aiAOV_' + aovName):
                aovs.AOVInterface().addAOV( aovName )
                mc.connectAttr(colorNode+'.outColor','aiAOV_'+aovName+'.defaultValue')
