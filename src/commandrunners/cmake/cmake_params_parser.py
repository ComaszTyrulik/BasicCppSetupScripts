import re


class CMakeParamsParser:
    @staticmethod
    def parse(parameters):
        # Find all parameters that look like CMake parameters `-DNAME_OF_PARAM=VALUE`
        found_parameters = re.findall('-D[A-Za-z0-9_-]+=[A-Za-z0-9_-]+', ' '.join(parameters))
        parsed_parameters = ' '.join(found_parameters)

        return parsed_parameters
