from os import listdir
from os.path import isfile, join

class tools:

    def __init__(self, _part_path):

        self.part_path = _part_path

    def get_list(self):
        path = '../../AMI/ami_public_manual/' + self.part_path +  '/' #abstractive
        files = [f for f in listdir(path) if isfile(join(path, f))]

        return files