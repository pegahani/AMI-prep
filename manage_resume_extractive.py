import tools
from meeting import meeting
import xml.etree.ElementTree as ET

class extractive(meeting):

    def __init__(self, _file_name):
        super(extractive, self).__init__('MAN', None)
        self.file_name = _file_name[0:_file_name.find('.')]
        tempo = _file_name[_file_name.find('.')+1:]
        self.suffix = tempo[0:_file_name.find('.')]
        self.path = '../../AMI/ami_public_manual/extractive/' + _file_name

    def get_root(self):

        tree = ET.parse(self.path)
        # a root for extractive resume
        self.root_abstract = tree.getroot()

    def get_extractive_resume(self):

        self.initializations()
        self.meeting = self.get_meeting_name_byFile(self.file_name)

        print self.meeting

        file = open('./manual_resume_extractive/extsumm/' + self.meeting + '.txt', 'w')

        if self.suffix == 'extsumm':
            file.write(self.handel_extsumm())

        file.close()

        return

    def handel_extsumm(self):

        string_output = ''

        self.get_root()
        # For extsumm suffixes
        for child in self.root_abstract:
            for grandchild in child:
                tempo = grandchild.attrib['href']
                dialogue_act_name = tempo[0:tempo.find('#')]

                ids = tempo[tempo.find('#'):]
                id_1 = ids[4:ids.find(')')]

                if ids.count('id') < 2:
                    id_2 = None
                else:
                    id_2 = ids[ids.find(')..id(')+6:-1]

                last_index_1 = id_1.rindex('.')
                _index_1 = id_1[last_index_1 + 1:]

                previous_part = id_1[0:last_index_1+1]
                counter = int(_index_1) + 1

                string_output += self.get_dact(dialogue_act_name, id_1)

                if id_2 != None:
                    last_index_2 = id_2.rindex('.')
                    _index_2 = id_2[last_index_2+1:]
                    while(counter <= int(_index_2)):
                        _next = str(previous_part + str(counter))
                        string_output += self.get_dact(dialogue_act_name, _next)
                        counter += 1

                string_output += '\n'

        return string_output

    def get_dact(self, d_act_name, d_act_id):

        string_output = ''

        dact_file = '../../AMI/ami_public_manual/dialogueActs/'+ d_act_name

        tree = ET.parse(dact_file)
        root = tree.getroot()

        self.get_meeting_list()
        word_roots = self.get_roots_words()

        adresto = 'to --> '

        for dact in root.iter('dact'):

            if dact.attrib['{http://nite.sourceforge.net/}id'] == d_act_id:
                pointer = d_act_name.find('.')

                if 'addressee' in dact.attrib:
                    adresto += dact.attrib['addressee']
                if 'reflexivity' in dact.attrib:
                    if dact.attrib['reflexivity'] == 'true':
                        adresto += ','+ d_act_name[pointer+1: pointer + 2]

                string_output += adresto + '\n'

                for t in dact:
                    if t.tag == '{http://nite.sourceforge.net/}pointer':
                        string_output +=  'dialogue type : ' + self.get_da_types(t.attrib['href']) + '\n'
                    elif t.tag == '{http://nite.sourceforge.net/}child':
                        (start_word, stop_word) = self.get_words_interval_for_speaker(t.attrib['href'])
                        speaker = d_act_name[pointer+1: pointer + 2]
                        if stop_word != None:
                            _phrase = self.get_word_interval(start_word, stop_word, word_roots[speaker])
                        else:
                            _phrase = self.get_Word(start_word,word_roots[speaker], speaker)
                        string_output += speaker + ' :' + _phrase + '\n'

        return string_output

    def get_da_types(self, param):

        da_types_file = '../../AMI/ami_public_manual/ontologies/da-types.xml'

        tree = ET.parse(da_types_file)
        root = tree.getroot()

        tempo = param.find('#')
        da_type = param[tempo+4:-1]

        for d_type in root.iter('da-type'):
            if d_type.attrib['{http://nite.sourceforge.net/}id'] == da_type:
                return d_type.attrib['gloss']

        return

tool = tools.tools('extractive')
meeting_list = []

# for file in tool.get_list():
#     print file
#     d = extractive(file)
#     d.get_extractive_resume()


#lists = list(set(meeting_list))
#print lists

file = 'TS3012a.extsumm.xml'
print file
d = extractive(file)
d.get_extractive_resume()


