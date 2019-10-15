import subprocess
from stegtest.types.embeddor import Embeddor
from stegtest.utils.filesystem import file_exists

class Openstego(Embeddor):

    def __init__(self, secret_txt:str, password:str):
        super().__init__()
        self.secret_txt = secret_txt
        self.password = password

    def embed(self, path_to_input, path_to_output):
        assert(file_exists(path_to_input))

        # assert(file_type(path_to_input, [".pmg"]))
        # assert(file_type(path_to_output, [".pmg"]))

        commands = ['openstego', 'embed', '-mf', self.secret_txt, '-cf', path_to_input, '-p', self.password, '-sf', path_to_output]
        subprocess.run(commands)