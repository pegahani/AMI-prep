from meeting import meeting
import xml.etree.ElementTree as ET
import tools

class abstractive(meeting):

    def __init__(self, _file_name):
        super(abstractive, self).__init__('MAN', None)
        self.file_name = _file_name[0:_file_name.find('.')]
        self.path = '../../AMI/ami_public_manual/abstractive/' + _file_name

    def get_root(self):

        tree = ET.parse(self.path)
        # a root for abstractive resume
        self.root_abstract = tree.getroot()

        return

    def get_abstractive_resume(self):
        #this part has several children: abstract, actions, decisions, problems

        self.initializations()
        self.meeting = self.get_meeting_name_byFile(self.file_name)
        self.get_root()

        file = open('./manual_resume_abstractive/' + self.meeting + '.txt', 'w')

        for child in self.root_abstract:
            file.write('\n' + child.tag + ' : \n')
            for sententce in child:
                file.write(sententce.text + '\n')

        file.close()

        return


tool = tools.tools('abstractive')

for file in tool.get_list():
    print file
    d = abstractive(file)
    d.get_abstractive_resume()