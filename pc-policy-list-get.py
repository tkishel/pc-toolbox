from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
import pc_lib_api
import pc_lib_general

# --Execution Block-- #
# --Parse command line arguments-- #
parser = pc_lib_general.pc_arg_parser_defaults()

parser.add_argument(
    'export_file_name',
    type=str,
    help='Name of the ouput file being exported to.')

args = parser.parse_args()
# --End parse command line arguments-- #

# --Main-- #
# Get login details worked out
pc_settings = pc_lib_general.pc_login_get(args.username, args.password, args.uiurl, args.config_file)

# Verification (override with -y)
pc_lib_general.prompt_for_verification_to_continue(args.yes)

# Sort out API Login
print('API - Getting authentication token...', end='')
pc_settings = pc_lib_api.pc_jwt_get(pc_settings)
print('Done.')
print()

# Call the API and capture the output
print('API - Calling API function...', end='')
pc_response = pc_lib_api.api_policy_list_get(pc_settings)
print('Done.')
print()

# Write the output to file
print('Exporting JSON output to file '+args.export_file_name+'...', end='')
pc_lib_general.pc_file_write_json(args.export_file_name, pc_response)
print('Done.')

