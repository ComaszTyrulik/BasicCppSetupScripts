from src.commandrunners.cmake.cmake_params_parser import CMakeParamsParser


def test_parse_will_parse_all_parameters_with_valid_format_and_return_them_as_single_string():
    param1 = '-DPARAM_1=ON'
    param2 = '-DPARAM_2=OFF'
    param3 = '-DPARAM_3=SomeOtherValue'

    params_to_parse = [param1, param2]
    expected_params_string = f'{param1} {param2} {param3}'

    actual_params_string = CMakeParamsParser.parse(params_to_parse)
    assert actual_params_string == expected_params_string


def test_parse_will_parse_omit_parameters_with_invalid_format():
    param1 = '-DPARAM_1=ON'
    invalid_param1 = 'PARAMETER'
    invalid_param2 = 'PARAMETER=ON'
    invalid_param3 = '-DPARAMETER ON'
    invalid_param4 = '-DPARAMETER'

    params_to_parse = [param1, invalid_param1, invalid_param2, invalid_param3, invalid_param4]
    expected_params_string = f'{param1}'

    actual_params_string = CMakeParamsParser.parse(params_to_parse)
    assert actual_params_string == expected_params_string
