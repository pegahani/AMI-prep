import xml.etree.ElementTree as ET
from collections import Counter

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

        return word_roots

    def get_roots_segments(self):

        tempo = self.get_files()
        segment_roots = dict.fromkeys(self.participants)

        segment_list = tempo[1]

        for item in range(len(self.participants)):
            tree = ET.parse(segment_list[item])
            segment_roots[self.participants[item]] = tree.getroot()

        return segment_roots

    def generate_text(self):

        # write dialogue on txt file
        file = open(self.meeting+'.txt', 'w')

        # a minimum timer among all participants
        total_time_pointer = 10000000.0
        total_speaker_pointer = None

        word_roots = self.get_roots_words()
        segment_roots = self.get_roots_segments()

        segment_xml_length = {i:self.count_segment_length(segment_roots[i]) for i in self.participants}

        #timer on each participants that shows which time of speaker we are analysing at the moment
        time_pointer_on_participants = {i: float(segment_roots[i][0].attrib['transcriber_start']) for i in self.participants}

        #a couneter on XML childeren that indicates where we are during the dialogue transcription
        counter_on_segment_xml = {i:0 for i in self.participants}

        #for i in range(20):
        # if we get at the end of all speaker segments xml file
        while cmp(segment_xml_length,counter_on_segment_xml):

            total_time_pointer = 10000000.0

            for key,value in time_pointer_on_participants.iteritems():
                 if counter_on_segment_xml[key]<segment_xml_length[key] and value < total_time_pointer:
                    total_time_pointer = value
                    total_speaker_pointer = key

            tempo = segment_roots[total_speaker_pointer][counter_on_segment_xml[total_speaker_pointer]][0].attrib['href']
            if Counter(tempo)['('] == 2:

                (start_word, stop_word) = self.get_words_interval_for_speaker(tempo)
                _phrase = self.get_word_interval(start_word,stop_word, word_roots[total_speaker_pointer])

                file.write(total_speaker_pointer+' : ' + _phrase+ '\n')

            #update time poniter on total time pointer
            counter_on_segment_xml[total_speaker_pointer] += 1

            if counter_on_segment_xml[total_speaker_pointer] < segment_xml_length[total_speaker_pointer]:
                time_pointer_on_participants[total_speaker_pointer] = float(segment_roots[total_speaker_pointer][counter_on_segment_xml[total_speaker_pointer]].attrib[
                'transcriber_start'])

        file.close()
        return

    #takes the href in xml segmentation and separates the start and finish words
    def get_words_interval_for_speaker(self, tempo):

        start_word = tempo[(tempo.index('(') + len('(')):tempo.index(')')]
        tempo = tempo[tempo.index(')') + 1:]
        finish_word = tempo[(tempo.index('..id(') + len('..id(')):tempo.index(')')]

        return (start_word, finish_word)

    def get_word_interval(self, start_word, stop_word, word_root_speaker):
        """
        take start word and stop word in word xml file and returns back the generated phrase
        :param start_word:
        :param stop_word:
        :param word_root_speaker:
        :return:
        """

        _phrase = ''

        for word in word_root_speaker.iter('w'):


            if self.compare_word_id(word.attrib['{http://nite.sourceforge.net/}id'], stop_word) and \
                    self.compare_word_id( start_word, word.attrib['{http://nite.sourceforge.net/}id'] ):
                _phrase = _phrase + ' ' + word.text

            if self.compare_word_id(stop_word, word.attrib['{http://nite.sourceforge.net/}id']) :
                break

        return _phrase

    def compare_word_id(self, param1, param2):

        if len(param1) > len(param2):
            return False
        elif len(param1) < len(param2):
            return True
        else:
            #if they have the same size
            if param1 == param2:
                return True

        return param1 < param2

    def count_segment_length(self, speaker_segment_root):
        """
        it counts the total number of children in xml tree
        :param param:
        :return:
        """
        length = 0
        for it in speaker_segment_root.findall('segment'):
            length += 1

        return length


ex = manage_meeting("MAN", "meet_2")
ex.initializations()
ex.get_meeting_list()
#ex.get_participants('meet_1')

#print ex.compare_word_id('IS1000a.C.words1', 'IS1000a.C.words2')
ex.generate_text()




