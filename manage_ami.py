import xml.etree.ElementTree as ET
import re

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

    def get_roots_words(self):

        tempo = self.get_files()
        word_list = tempo[0]

        self.participants = [item for item in self.get_participants().iterkeys()]
        word_roots = dict.fromkeys(self.participants)

        for item in range(len(self.participants)):
            tree_ = ET.parse(word_list[item])
            word_roots[self.participants[item]] = tree_.getroot()

        print word_roots['A'].attrib

        return word_roots

    def get_roots_segments(self):

        tempo = self.get_files()
        segment_roots = dict.fromkeys(self.participants)

        segment_list = tempo[1]

        for item in range(len(self.participants)):
            tree = ET.parse(segment_list[item])
            segment_roots[self.participants[item]] = tree.getroot()

        print segment_roots['A'].attrib

        return segment_roots

    def generate_text(self):

        # a minimum timer among all participants
        total_time_pointer = 10000000.0
        total_speaker_pointer = None

        word_roots = self.get_roots_words()
        print 'MMMMMMMMMM', word_roots['A'].attrib
        segment_roots = self.get_roots_segments()
        print 'MMMMMMMMMM', segment_roots['A'].attrib

        print  segment_roots
        print word_roots

        #timer on each participants that shows which time of speaker we are analysing at the moment
        time_pointer_on_participants = {i: float(segment_roots[i][0].attrib['transcriber_start']) for i in self.participants}
        print time_pointer_on_participants

        #a couneter on XML childeren that indicates where we are during the dialogue transcription
        counter_on_segment_xml = {i:0 for i in self.participants}

        for key,value in time_pointer_on_participants.iteritems():
             if value < total_time_pointer:
                total_time_pointer = value
                total_speaker_pointer = key

        #update time poniter on total time pointer
        time_pointer_on_participants[total_speaker_pointer] = float(segment_roots[total_speaker_pointer][0].attrib['transcriber_end'])

        print total_speaker_pointer, total_time_pointer
        print counter_on_segment_xml

        tempo = segment_roots[total_speaker_pointer][counter_on_segment_xml[total_speaker_pointer]][0].attrib['href']
        (start_word, stop_word) = self.get_words_interval_for_speaker(tempo)

        print start_word
        print stop_word

        print word_roots['C'].attrib

        return

    #takes the href in xml segmentation and separates the start and finish words
    def get_words_interval_for_speaker(self, tempo):

        start_word = tempo[(tempo.index('(') + len('(')):tempo.index(')')]
        tempo = tempo[tempo.index(')') + 1:]
        finish_word = tempo[(tempo.index('..id(') + len('..id(')):tempo.index(')')]

        return (start_word, finish_word)


ex = manage_meeting("MAN", "meet_1")
ex.initializations()
ex.get_meeting_list()
#ex.get_participants('meet_1')

ex.generate_text()




