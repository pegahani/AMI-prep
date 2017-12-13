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
            self.num_meetings = len(self.root_resources.getchildren())

        else:
            raise ValueError('entered corpus type not exist')

    def get_meeting_list(self):

        self.meeting_list = []

        for i in range(self.num_meetings):
            self.meeting_list.append(self.root_resources[i].attrib['{http://nite.sourceforge.net/}id'])

        return self.meeting_list

    def get_participants(self, _meeting):

        participant = {}
        _meeting_id = self.meeting_list.index(_meeting)

        print self.root_resources[_meeting_id][0]

        for child in self.root_resources[_meeting_id].findall('speaker'):
            participant[child.attrib['nxt_agent']] = child.attrib["global_name"]

        return participant


ex = manage_ami("MAN")
ex.initializations()
print ex.get_meeting_list()

print ex.get_participants('meet_1')






