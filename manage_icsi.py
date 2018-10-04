"""
this code is for geenrating the original ICSI corpus from their supported XML version.
"""

import os
import random
import string
import xml.etree.ElementTree as ET

meeting_list = ['Bdb001'] + ['Bed00'+str(k) for k in range(2,10) if k != 7] +\
               ['Bed0'+str(k) for k in range(10,18) ]+\
               ['Bmr00' + str(j) for j in range(1,10) if j != 4]+['Bmr0' + str(j) for j in range(10,31) if j != 17]+\
               ['Bns00' + str(j) for j in range(1,4)]+\
               ['Bro00' + str(j) for j in range(3,10) if (j != 6 and j!= 9)]+['Bro0' + str(j) for j in range(10,29) if j != 20]+\
               ['Bsr001', 'Btr001', 'Btr002', 'Buw001']


class manage_meet_icsi:
    def __init__(self, corpus_name):
        self.corpus_name = corpus_name
        self.file = None

    def initialization(self):
        if self.corpus_name == "ICSI":
            self.file = "../../ICSI/ICSI_original_transcripts/transcripts/"
        pass

    def get_participants(self, root_resources):

        participants_list = []
        participants = root_resources[0].getchildren()[-1].getchildren()
        for participant in participants:
            participants_list.append(participant.attrib['Name'])

        """assign A B C D .. to the participants names to make them coherent with AMI corpora"""
        alaphabetical_participants = {participants_list[i]: string.uppercase[i] for i in range(len(participants_list))}

        return alaphabetical_participants

    def generate_text(self, meet):

        generate_file = open('./ICSI_corpus/'+ meet+'.txt', 'w')
        schema = self.file + meet + '.mrt'

        if self.file != None:
            tree_resource = ET.parse(schema)
            root_resources = tree_resource.getroot()
            participants = self.get_participants(root_resources)

            texts = root_resources[1].getchildren()
            generate_file.write('\t')

            for segment in texts:
                str = ''
                if segment.text not in [None, '\n']:
                    str += segment.text.strip()
                children = segment.getchildren()
                if children != []:
                    tempo = segment.getchildren()
                    for child in tempo:
                        if child.text not in [None, '\n    ']:
                            str += child.text
                        last = child
                    if (last.tail) is not None:
                        str += last.tail
                if str not in ['\n    ', None, ' ', '\n']:
                    if str[-5:] == '\n    ':
                        if 'Participant' in segment.attrib:
                            generate_file.write(participants[segment.attrib['Participant']] + ' : ' + str[0:-5] + '\n')
                        else:
                            generate_file.write(random.choice(participants.values()) + ' : ' + str[0:-5] + '\n')

            #num_meetings = len(root_resources.getchildren())

        return


if __name__ == '__main__':

    ex = manage_meet_icsi("ICSI")
    ex.initialization()
    for meet in meeting_list:
        ex.generate_text(meet)
