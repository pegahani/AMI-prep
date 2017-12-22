import xml.etree.ElementTree as ET

class meeting(object):

    def __init__(self,_corpus_type, _metting ):
        self.meeting = _metting
        self.corpus_type = _corpus_type

    def initializations(self):
        """if corpus type is manual"""
        if self.corpus_type == "MAN":
            self.file = "../../AMI/ami_public_manual"
        #if corpus type is automatic
        elif self.corpus_type == "AUT":
            self.file = "../../AMI/ami_public_auto"

        schema = self.file + "/corpusResources/meetings.xml"

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

    def get_file_name(self):
        _meeting_id = self.get_meeting_id_by_name()
        return  self.root_resources[_meeting_id].attrib["observation"]

    def get_meeting_name_byFile(self, file_name):

        for child in self.root_resources:
           if child.attrib["observation"] == file_name:
                return  child.attrib["{http://nite.sourceforge.net/}id"]

        return

    def get_segments_files(self):

        segments_file = []
        file_name = self.get_file_name()

        if self.corpus_type == 'MAN':
            for key in self.get_participants().iterkeys():
                segments_file.append(self.file + "/segments/" + file_name + '.' + key + '.segments.xml')
        elif self.corpus_type == 'AUT':
            for key in self.get_participants().iterkeys():
                segments_file.append(self.file + "/ASR/ASR_AS_CTM_v1.0_feb07/" + file_name + '.' + key + '.segments.xml')

        return segments_file

    def get_word_files(self):

        words_files = []
        file_name = self.get_file_name()

        if self.corpus_type == 'MAN':
            for key in self.get_participants().iterkeys():
                words_files.append(self.file + "/words/" + file_name + '.' + key + '.words.xml')
        elif self.corpus_type == 'AUT':
            for key in self.get_participants().iterkeys():
                words_files.append(self.file + "/ASR/ASR_AS_CTM_v1.0_feb07/" + file_name + '.' + key + '.words.xml')

        return words_files


    # def get_files(self):
    #
    #     words_files = []
    #     segments_file = []
    #
    #     # _meeting_id = self.get_meeting_id_by_name()
    #     # file_name = self.root_resources[_meeting_id].attrib["observation"]
    #
    #     file_name = self.get_file_name()
    #
    #     if self.corpus_type == 'MAN':
    #         for key in self.get_participants().iterkeys():
    #             words_files.append(self.file + "/words/" + file_name + '.' + key + '.words.xml')
    #             segments_file.append(self.file + "/segments/" + file_name + '.' + key + '.segments.xml')
    #
    #     elif self.corpus_type == 'AUT':
    #         for key in self.get_participants().iterkeys():
    #             words_files.append(self.file + "/ASR/ASR_AS_CTM_v1.0_feb07/" + file_name + '.' + key + '.words.xml')
    #             segments_file.append(
    #                 self.file + "/ASR/ASR_AS_CTM_v1.0_feb07/" + file_name + '.' + key + '.segments.xml')
    #
    #     return (words_files, segments_file)

    def get_roots_words(self):

        #tempo = self.get_files()
        word_list = self.get_word_files()

        self.participants = [item for item in self.get_participants().iterkeys()]
        word_roots = dict.fromkeys(self.participants)

        for item in range(len(self.participants)):
            tree_ = ET.parse(word_list[item])
            word_roots[self.participants[item]] = tree_.getroot()

        return word_roots

    #takes the href in xml segmentation and separates the start and finish words
    def get_words_interval_for_speaker(self, tempo):

        finish_word = None

        start_word = tempo[(tempo.index('(') + len('(')):tempo.index(')')]
        if tempo.count('(') ==2:
            tempo = tempo[tempo.index(')') + 1:]
            finish_word = tempo[(tempo.index('..id(') + len('..id(')):tempo.index(')')]
        else:
            finish_word = None

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

    def get_Word(self, start, word_root_speaker, speaker):

        for word in word_root_speaker:
            if word.attrib['{http://nite.sourceforge.net/}id'] == start:
                return word.text

        raise ValueError(start + ' not exist' + ' in ' + self.get_file_name() + '.' + speaker + '.words.xml')

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

