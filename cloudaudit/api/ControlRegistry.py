__author__ = 'joshd'


import webob
from cloudaudit.api.InitControl import InitController
import cloudaudit.api.Control_Nist800_53_AC_7
from xml.dom.minidom import Document


class ControlRegistry(object):

    """
        This class acts as a registry and factory for all Control class implementations

        Registry head is a N-tiered dictionary with the following conventions:

        { Compliance Regimes } -> { Compliance Versions } -> { Control Ids } -> Class Instances
    """

    registryHead = { }

    def __init__(self):

        newControl = cloudaudit.api.Control_Nist800_53_AC_7.Control_Nist800_53_AC_7()
        versionsDict = { }
        controlDict = { }


        if newControl.regime in self.registryHead.keys():
            versionsDict = self.registryHead[newControl.regime]
        else:
            self.registryHead[newControl.regime] = { }
            versionsDict = self.registryHead[newControl.regime]

        if newControl.regime_version in versionsDict.keys():
            controlDict = self.versionsDict[newControl.regime_version]
        else:
            versionsDict[newControl.regime_version] = { }
            controlDict = versionsDict[newControl.regime_version]

        if newControl.control_id in controlDict.keys():
            return
        else:
            controlDict[newControl.control_id] = newControl

    def getControlFromUrl(self, url):
        # We match greedily at each stage, so first try to match the entire Url and then remove the least most
        # significant url portion until we get a match

        tempUrl = url

        while not tempUrl in self.registryHead.keys():
            tempUrl = str.rsplit(tempUrl, "/", 1)
            if len(tempUrl) == 1:
                raise Exception("Could not find a compliance regime for the Url:  " + url)
            tempUrl = tempUrl[0]

        versionDict = self.registryHead[tempUrl]

        index = len(tempUrl) + 1

        subUrl = url[index:]
        tempUrl = subUrl

        while not tempUrl in versionDict.keys():
            tempUrl = str.rsplit(tempUrl, "/", 1)
            if len(tempUrl) == 1:
                raise Exception("Could not find a control version for the Url:  " + url)
            tempUrl = tempUrl[0]

        controlDict = versionDict[tempUrl]
        index = len(tempUrl) + 1
        subUrl = subUrl[index:]
        tempUrl = subUrl
        
        while not tempUrl in controlDict.keys():
            tempUrl = str.rsplit(tempUrl, "/", 1)
            if len(tempUrl) == 1:
                raise Exception("Could not find a control id for the Url:  " + url)
            tempUrl = tempUrl[0]

        control = controlDict[tempUrl]
        return control