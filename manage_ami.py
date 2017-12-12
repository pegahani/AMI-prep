import xml.etree.ElementTree as ET

class manage_ami:

    def __init__(self,_corpus_type):

        self.corpus_type = _corpus_type
        self.file = None

    def initializations(self):
        """if corpus type is manual"""
        if self.corpus_type == "MAN":
            self.file = "../../AMI/ami_public_manual/corpusResources/meetings.xml"
        #if corpus type is automatic
        elif self.corpus_type == "AUT":
            self.file = "../../AMI/ami_public_auto/corpusResources/meetings.xml"

        if self.file != None:
            self.tree_resource = ET.parse(self.file)
            self.root_resources = self.tree_resource.getroot()

        else:
            raise ValueError('entered corpus type not exist')

    def get_meeting_list(self):

        return self.root_resources[0].attrib

ex = manage_ami("MAN")
ex.initializations()
print ex.get_meeting_list()






