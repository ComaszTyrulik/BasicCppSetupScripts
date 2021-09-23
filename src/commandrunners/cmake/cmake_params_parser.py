import re


class CMakeParamsParser:
    @staticmethod
    def parse(parameters):
        found_parameters = re.findall('-D[A-Za-z0-9_-]+=[A-Za-z_-]+', ' '.join(parameters))
        parsed_parameters = ' '.join(found_parameters)

        return parsed_parameters
