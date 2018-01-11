from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET

import tools
from meeting import meeting

# this is just for automatic corpus

# def get_decisions_list():
#     path = '../../AMI/ami_public_manual/decision/manual'
#     files = [f for f in listdir(path) if isfile(join(path, f))]
#
#     return files

class decision(meeting):

    def __init__(self, _file_name):

        super(decision, self).__init__('MAN', None)
        self.file_name = _file_name[0:_file_name.find('.')]
        self.path = '../../AMI/ami_public_manual/decision/manual/' + _file_name

    def get_root_decision(self):

        tree = ET.parse(self.path)
        # a root forecision
        self.root_entity_types = tree.getroot()

        return


    def get_decisions(self):

        self.initializations()
        self.meeting = self.get_meeting_name_byFile(self.file_name)

        file = open('./manuel_decisions/' + self.meeting + '.txt', 'w')

        self.get_root_decision()
        self.get_meeting_list()
        word_roots = self.get_roots_words()

        decision_counter = 1

        for decision in self.root_entity_types:
            file.write('Decision'+ str(decision_counter)+ '\n'+'\n')
            for grand_child in decision:
                words = grand_child.attrib['href']
                (start, stop) = self.get_words_interval_for_speaker(words)

                speaker = start[start.find('.')+len('.'):start.rfind('.')]
                file.write(speaker + ' : ')
                if stop != None:
                    phrase = self.get_word_interval(start, stop, word_roots[speaker])
                else:
                    phrase = self.get_Word(start, word_roots[speaker], speaker)
                if phrase != None:
                    file.write(phrase + '\n')

            file.write('\n')
            decision_counter += 1

        file.close()

        return

tool = tools.tools('decision/manual')

for file in tool.get_list()[0:1]:
    print file
    d = decision(file)
    d.get_decisions()