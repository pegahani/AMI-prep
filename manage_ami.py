import xml.etree.ElementTree as ET

class manage_meeting:

    def __init__(self,_corpus_type, _meeting):

        self.corpus_type = _corpus_type
        self.file = None
        self.meeting = _meeting

    def initializations(self):
        """if corpus type is manual"""
        if self.corpus_type == "MAN":
            self.file = "../../AMI/ami_public_manual"
        #if corpus type is automatic
        elif self.corpus_type == "AUT":
            self.file = "../../AMI/ami_public_auto"

        schema = self.file+ "/corpusResources/meetings.xml"

        if file != None:
            self.tree_resource = ET.parse(schema)
            self.root_resources = self.tree_resource.getroot()
            self.num_meetings = len(self.root_resources.getchildren())

        else:
            raise ValueError('entered corpus type not exist')

    def get_meeting_list(self):

        self.meeting_list = []

        for i in range(self.num_meetings):
            self.meeting_list.append(self.root_resources[i].attrib['{http://nite.sourceforge.net/}id'])

        return self.meeting_list

    def get_meeting_id_by_name(self):
        return self.meeting_list.index(self.meeting)

    def get_participants(self):

        participant = {}
        _meeting_id = self.get_meeting_id_by_name()

        for child in self.root_resources[_meeting_id].findall('speaker'):
            participant[child.attrib['nxt_agent']] = child.attrib["global_name"]

        return participant

    def get_files(self):

        words_files = []
        segments_file = []

        _meeting_id = self.get_meeting_id_by_name()
        file_name = self.root_resources[_meeting_id].attrib["observation"]

        for key in self.get_participants().iterkeys():
            words_files.append(self.file + "/words/" + file_name + '.' + key + '.words.xml')
            segments_file.append(self.file + "/segments/" + file_name + '.' + key+'.segments.xml' )

        return (words_files, segments_file)

    def get_roots(self):

        (word_list, segment_list) = self.get_files()

        participants = [item for item in self.get_participants().iterkeys()]
        word_roots = segment_roots = dict.fromkeys(participants)

        for item in range(len(participants)):
            tree = ET.parse(word_list[item])
            word_roots[participants[item]] = tree.getroot()
            tree = ET.parse(segment_list[item])
            segment_roots[participants[item]] = tree.getroot()

        return (word_roots, segment_roots)

    def generate_text(self):

        (word_roots, segment_roots) = self.get_roots()
        


        return


ex = manage_meeting("MAN", "meet_1")
ex.initializations()
ex.get_meeting_list()
#ex.get_participants('meet_1')

ex.get_roots()




