import xml.etree.ElementTree as ET
from meeting import meeting

class manage_name_enity(meeting):

    def get_entities_type(self):

        if self.corpus_type == 'MAN':
            schema = "../../AMI/ami_public_manual/ontologies/ne-types.xml"
            tree = ET.parse(schema)
            #a root for entity types
            self.root_entity_types = tree.getroot()

        return

    def get_entities_roots(self):

        file_name = self.get_file_name()
        entities_files = []

        participants = [i for i in self.get_participants().keys()]
        entities_roots = dict.fromkeys(participants)

        if self.corpus_type == 'MAN':
            for key in participants:
               entities_files.append(self.file + "/namedEntities/" + file_name + '.' + key + ".ne.xml")

        for item in range(len(participants)):
            tree_ = ET.parse(entities_files[item])
            entities_roots[participants[item]] = tree_.getroot()

        return entities_roots

    def find_entity_type(self, entity_id):
        """
        this function get the entity id and finds its name in ne-types.xml file
        :param entity_id:
        :return:
        """

        #TODO we can get other information from entity type files. it depends what we need exactly

        for child in self.root_entity_types.findall('ne-type'):
            if child.attrib['{http://nite.sourceforge.net/}id'] == entity_id:
                return child.attrib['name']
            else:
                for grand_child in child.findall('ne-type'):
                    if grand_child.attrib['{http://nite.sourceforge.net/}id'] == entity_id:
                        return grand_child.attrib['name']
                    else:
                        for grand_grand_child in grand_child.findall('ne-type'):
                            if grand_grand_child.attrib['{http://nite.sourceforge.net/}id'] == entity_id:
                                return grand_grand_child.attrib['name']
                            else:
                                for descendant in grand_grand_child.findall('ne-type'):
                                    if descendant.attrib['{http://nite.sourceforge.net/}id'] == entity_id:
                                        return descendant.attrib['name']



        return

    def get_entity_list(self, speaker):

        file = open('./manuel_corpus_name_entities/' + self.meeting + '.' + speaker + '.txt', 'w')

        root_entities_speaker = self.get_entities_roots()[speaker]
        root_words_speaker = self.get_roots_words()[speaker]

        for child in root_entities_speaker:

            tempo = child[0].attrib['href']
            founded = tempo.find('(')
            entity_type = tempo[founded+1:-1]
            words_included = child[1].attrib['href']

            (start, stop) = self.get_words_interval_for_speaker(words_included)

            if stop != None:
                file.write(self.get_word_interval(start, stop, root_words_speaker) + ' : ' + self.find_entity_type(entity_type)+ '\n')
            else:
                file.write(self.get_Word(start, root_words_speaker, speaker) + ' : ' + self.find_entity_type(entity_type) + '\n')

        file.close()
        return


# ex = manage_name_enity('MAN', 'meet_2')
# ex.initializations()
# ex.get_meeting_list()
#
meeting_list = ['meet_1', 'meet_2', 'meet_3', 'meet_4', 'meet_5', 'meet_6', 'meet_7', 'meet_8', 'meet_10', 'meet_11', 'meet_12', 'meet_13', 'meet_14', 'meet_15', 'meet_16', 'meet_17', 'meet_18', 'meet_19', 'meet_20', 'meet_21', 'meet_22', 'meet_23', 'meet_25', 'meet_26', 'meet_27', 'meet_28', 'meet_29', 'meet_30', 'meet_31', 'meet_32', 'meet_33', 'meet_34', 'meet_35', 'meet_36', 'meet_37', 'meet_38', 'meet_39', 'meet_40', 'meet_41', 'meet_42', 'meet_43', 'meet_44', 'meet_45', 'meet_46', 'meet_47', 'meet_48', 'meet_49', 'meet_50', 'meet_51', 'meet_51b', 'meet_52', 'meet_53', 'meet_54', 'meet_55', 'meet_56', 'meet_57', 'meet_58', 'meet_59', 'meet_60', 'meet_61', 'meet_62', 'meet_63', 'meet_64', 'meet_65', 'meet_66', 'meet_67', 'meet_68', 'meet_69', 'meet_70', 'meet_71', 'meet_72', 'meet_73', 'meet_74', 'meet_75', 'meet_76', 'meet_77', 'meet_78', 'meet_79', 'meet_80', 'meet_81', 'meet_82', 'meet_83', 'meet_84', 'meet_85', 'meet_86', 'meet_87', 'meet_88', 'meet_89', 'meet_90', 'meet_91', 'meet_92', 'meet_93', 'meet_94', 'meet_95', 'meet_96', 'meet_97', 'meet_98', 'meet_99', 'meet_112', 'meet_113', 'meet_114', 'meet_115', 'meet_116', 'meet_117', 'meet_118', 'meet_119', 'meet_120', 'meet_121', 'meet_122', 'meet_123', 'meet_124', 'meet_125', 'meet_126', 'meet_127', 'meet_128', 'meet_129', 'meet_130', 'meet_131', 'meet_132', 'meet_133', 'meet_134', 'meet_135', 'meet_136', 'meet_137', 'meet_138', 'meet_139', 'meet_140', 'meet_141', 'meet_142', 'meet_143', 'meet_144', 'meet_145', 'meet_146', 'meet_147', 'meet_148', 'meet_149', 'meet_150', 'meet_151', 'meet_156', 'meet_157', 'meet_158', 'meet_159', 'meet_160', 'meet_161', 'meet_162', 'meet_163', 'meet_164', 'meet_165', 'meet_166', 'meet_167', 'meet_168', 'meet_169', 'meet_170', 'meet_171', 'meet_172', 'meet_188', 'meet_173', 'meet_174', 'meet_175', 'meet_176', 'meet_177', 'meet_178', 'meet_179', 'meet_180', 'meet_181', 'meet_182', 'meet_183', 'meet_184', 'meet_185', 'meet_186', 'meet_187']

t = meeting_list.index('meet_187')

# print meeting_list[0]

for meeting in meeting_list[t+1:]:
    print meeting
    ex = manage_name_enity("MAN", meeting)
    ex.get_entities_type()
    ex.initializations()
    ex.get_meeting_list()
    ex.get_participants()
    ex.get_entities_roots()
    for speaker in ex.get_participants().keys():
        ex.get_entity_list(speaker)