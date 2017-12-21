import xml.etree.ElementTree as ET
from collections import Counter

from meeting import meeting

class manage_meeting(meeting):

    def get_roots_segments(self):

        #tempo = self.get_files()
        segment_roots = dict.fromkeys(self.participants)

        #segment_list = tempo[1]
        segment_list = self.get_segments_files()

        for item in range(len(self.participants)):
            tree = ET.parse(segment_list[item])
            segment_roots[self.participants[item]] = tree.getroot()

        return segment_roots

    def generate_text(self):

        file = None

        # write dialogue on txt file
        if self.corpus_type == 'MAN':
            file = open('./manuel_corpus/'+ self.meeting+'.txt', 'w')
            #file = open('./test_corpus/' + self.meeting + '.txt', 'w')
        elif self.corpus_type == 'AUT':
            file = open('./automatic_corpus/' + self.meeting + '.txt', 'w')


        # a minimum timer among all participants
        total_time_pointer = 10000000.0
        total_speaker_pointer = None

        word_roots = self.get_roots_words()
        segment_roots = self.get_roots_segments()

        segment_xml_length = {i:self.count_segment_length(segment_roots[i]) for i in self.participants}

        if self.corpus_type == 'MAN':

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
        # if the corpus are automatic
        elif self.corpus_type == 'AUT':

            # timer on each participants that shows which time of speaker we are analysing at the moment*******
            time_pointer_on_participants = {i: float(word_roots[i][0].attrib['starttime']) for i in self.participants}

            #a couneter on XML childeren that indicates where we are during the dialogue transcription
            counter_on_segment_xml = {i:0 for i in self.participants}
            #a couneter on XML childeren that indicates where we are during the dialogue transcription
            counter_on_word_xml = {i:0 for i in self.participants}

            #for i in range(20):
            while cmp(segment_xml_length, counter_on_segment_xml):

                total_time_pointer = 10000000.0

                for key, value in time_pointer_on_participants.iteritems():
                    if counter_on_segment_xml[key] < segment_xml_length[key] and value < total_time_pointer:
                        total_time_pointer = value
                        total_speaker_pointer = key

                tempo = segment_roots[total_speaker_pointer][counter_on_segment_xml[total_speaker_pointer]][0].attrib['href']

                if Counter(tempo)['('] == 2:
                    (start_word, stop_word) = self.get_words_interval_for_speaker(tempo)

                    #******
                    start_word = start_word.replace("sil", "aw")
                    stop_word = stop_word.replace("sil", "aw")

                    _phrase = self.get_word_interval(start_word, stop_word, word_roots[total_speaker_pointer])

                    file.write(total_speaker_pointer + ' : ' + _phrase + '\n')

                    #update time poniter on total time pointer***
                    counter_on_segment_xml[total_speaker_pointer] += 1
                    counter_on_word_xml[total_speaker_pointer] += 2 + len(_phrase.split())

                    if counter_on_segment_xml[total_speaker_pointer] < segment_xml_length[total_speaker_pointer]:
                        time_pointer_on_participants[total_speaker_pointer] = float(word_roots[total_speaker_pointer][counter_on_word_xml[total_speaker_pointer]].attrib[
                        'starttime'])

            file.close()
        return

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

    def generate_all_texts(self):
        if self.meeting == None:

            self.initializations()
            self.meeting_list = self.get_meeting_list()
            ex.get_meeting_list()
            ex.get_participants()


            for meeting in self.meeting_list:
                self.meeting = meeting
                self.generate_text()
        return

# ex = manage_meeting("AUT", None)
# ex.generate_all_texts()

#TODO add speakers roles to text files


#TODO change your code for AUTOMATIC part w.r.t some other xml fomrs such as: meet_30, meet_31, meet_51, meet_59
#TODO meet_112 ...  meet_135 and the rest

#TODO meet_10 and meet_59 return error not found ....
#TODO meet_14 says that IS1003b.words.xml not exist

ex = manage_meeting("AUT", "meet_1")
ex.initializations()
ex.get_meeting_list()
print ex.meeting_list
ex.get_participants()
ex.generate_text()


# #
# # #ex.generate_text()
# #
# # ex.generate_text()
#
# #print ex.compare_word_id('IS1000a.C.words1', 'IS1000a.C.words2')
# for meeting in ex.meeting_list[-1]:
#    print meeting
#    ex2 = manage_meeting("AUT", meeting)
#    ex2.initializations()
#    ex2.get_meeting_list()
#    ex2.generate_text()




