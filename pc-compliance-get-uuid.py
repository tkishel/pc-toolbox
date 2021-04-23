from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
parser.add_argument(
    'compliance_standard_name',
    type=str,
    help='Name of the Compliance Standard to look up.')
parser.add_argument(
    '-rid',
    '--requirementId',
    type=str,
    help='(Optional) - Only required to find the UUID of a Requirement or a Section. This will be the "REQUIREMENT" from the UI. '
         'Note: This requirement must exist in the specified Compliance Standard. If it is in another standard, the lookup will fail.')
parser.add_argument(
    '-sid',
    '--sectionId',
    type=str,
    help='(Optional) - Only required to find the UUID of a Section. This will be the "SECTION" from the UI. '
         'Note: This section must exist in the specified Standard and the specified Compliance Requirement. '
         'If it is in another standard, or another Requirement, the lookup will fail.')
args = parser.parse_args()

# --Main-- #

if args.sectionId is not None:
    if args.requirementId is None:
        pc_lib_general.pc_exit_error(400, 'A Requirement is required if you want to get the UUID of a Section. '
            'Please enter the correct Requirement for the desired Section. Exiting ...')

pc_lib_general.prompt_for_verification_to_continue(args.yes)

print('API - Getting login ...', end='')
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print(' done.')
print()

# API Queries

print('API - Getting the Compliance Standards list ... ', end='')
pc_settings, response_package = pc_lib_api.api_compliance_standard_list_get(pc_settings)
compliance_standard_list = response_package['data']
compliance_standard = pc_lib_general.search_list_object_lower(compliance_standard_list, 'name', args.compliance_standard_name)
print('done.')

if compliance_standard is None:
    pc_lib_general.pc_exit_error(400, 'Compliance Standard not found. Please check the Compliance Standard name and try again.')

print()
print('Compliance Standard Name: ' + compliance_standard['name'] + "\nUUID: " + compliance_standard['id'])
print()

if args.requirementId is not None:
    print('API - Getting Requirements List for Compliance Standard ... ', end='')
    pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_list_get(pc_settings, compliance_standard['id'])
    compliance_requirement_list = response_package['data']
    print('done.')

    compliance_requirement = pc_lib_general.search_list_object_lower(compliance_requirement_list, 'requirementId', args.requirementId)
    if compliance_requirement is None:
        pc_lib_general.pc_exit_error(400, 'Requirement not found in the specified Compliance Standard. '
        'Please check the Compliance Standard and Requirement names and try again.')

    print()
    print('Requirement Name: ' + compliance_requirement['requirementId'] + "\nUUID: " + compliance_requirement['id'])
    print()

    if args.sectionId is not None:
        print('API - Getting Sections for Requirement ... ', end='')
        pc_settings, response_package = pc_lib_api.api_compliance_standard_requirement_section_list_get(pc_settings, compliance_requirement['id'])
        compliance_section_list = response_package['data']
        print('done.')

        compliance_section = pc_lib_general.search_list_object_lower(compliance_section_list, 'sectionId', args.sectionId)
        if compliance_section is None:
            pc_lib_general.pc_exit_error(400, 'Section not found in the specified Requirement.  '
            'Please check the Compliance Standard, Requirement, and Section names and try again.')

        print()
        print('Section Name: ' + compliance_section['sectionId'] + "\nUUID: " + compliance_section['id'])
        print()