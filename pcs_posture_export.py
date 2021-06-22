""" Prisma Cloud Configuration Snapshot Exporter """

from json import dumps
from os import isatty
from sys import exit as sys_exit, stderr, stdout
from time import time
from pc_lib import pc_api, pc_utility

# --Configuration-- #

parser = pc_utility.get_arg_parser()

parser.add_argument(
    'export_file_name',
    type=str,
    help='Export file name')

parser.add_argument(
    '--pretty',
    action='store_true',
    help='(Optional) Specify pretty JSON output.')

args = parser.parse_args()

if not args.pretty:
    args.pretty = False

# --Initialize-- #

settings = pc_utility.get_settings(args)
pc_api.configure(settings)

# --Main-- #

# Prompt for warning if interactive
if isatty(stdout.fileno()):
    pc_utility.prompt_for_verification_to_continue(args)

# Set initial data structures for data model
export_object = {}
export_object['timestamp'] = int(time())
export_object['rules'] = {}
export_object['policies'] = {}
export_object['searches'] = {}
export_object['standards'] = {}
export_object['requirements'] = {}
export_object['sections'] = {}
export_object['groups'] = {}
export_object['accounts'] = {}
export_object['access_keys'] = {}
export_object['anomaly_settings'] = {}
export_object['anomaly_settings']['network'] = {}
export_object['anomaly_settings']['ueba'] = {}
export_object['anomaly_settings']['trusted'] = {}
'''
TODO
export_object['anomaly_settings']['trusted']['ip'] = {}
export_object['anomaly_settings']['trusted']['resource'] = {}
export_object['anomaly_settings']['trusted']['image'] = {}
export_object['anomaly_settings']['trusted']['tag'] = {}
export_object['anomaly_settings']['trusted']['service'] = {}
export_object['anomaly_settings']['trusted']['port'] = {}
'''
export_object['ip_allow'] = {}
export_object['notification_templates'] = {}
export_object['report_configs'] = {}
export_object['settings'] = {}
export_object['users'] = {}
export_object['roles'] = {}

# Populate data model
try:
    print("Exporting users...", file=stderr)
    export_object['users'] = pc_api.user_list_read()
    print("Users returned...", file=stderr)
    for user in export_object['users']:
        print("  %s %s" % ( user['email'], user['displayName']), file=stderr)

    print("Exporting user roles...", file=stderr)
    export_object['roles'] = pc_api.user_role_list_read()
    print(dumps(export_object['roles']))

    print("User roles returned...", file=stderr)
    for role in export_object['roles']:
        print("  %s %s" % ( role['id'], role['name']), file=stderr)

    print("Exporting access keys...", file=stderr)
    export_object['access_keys'] = pc_api.access_keys_list_read()

    print("Access keys returned...", file=stderr)
    for access_key in export_object['access_keys']:
        print("  %s %s" % (access_key['id'], access_key['name']), file=stderr)

    print("Exporting anomaly settings for network...", file=stderr)
    export_object['anomaly_settings']['network'] = pc_api.anomaly_settings_list_read('network')

    print("Anomaly settings for 'network' returned...", file=stderr)
    for anomaly_setting in export_object['anomaly_settings']['network']:
        print("  %s %s" % (anomaly_setting, export_object['anomaly_settings']['network'][anomaly_setting]['policyName']), file=stderr)

    print("Exporting anomaly settings for ueba...", file=stderr)
    export_object['anomaly_settings']['ueba'] = pc_api.anomaly_settings_list_read('ueba')

    print("Anomaly settings for 'ueba' returned...", file=stderr)
    for anomaly_setting in export_object['anomaly_settings']['ueba']:
        print("  %s %s" % (anomaly_setting, export_object['anomaly_settings']['ueba'][anomaly_setting]['policyName']), file=stderr)

    print("Exporting anomaly settings for trusted list ...", file=stderr)
    export_object['anomaly_settings']['trusted'] = pc_api.anomaly_trusted_list_read()

    print("Anomaly settings for 'trusted' returned...", file=stderr)
    for anomaly_setting in export_object['anomaly_settings']['trusted']:
        print("  %s %s" % (anomaly_setting, export_object['anomaly_settings']['trusted'][anomaly_setting]['policyName']), file=stderr)

    # There is more to the above trusted lists ***TODO***
    print("Exporting ip allow list...", file=stderr)
    export_object['ip_allow'] = pc_api.ip_allow_list_read()

    print("IP allow list returned...", file=stderr)
    for ip_address in export_object['ip_allow']:
        print("  %s %s" % (ip_address, export_object['ip_allow'][ip_address]), file=stderr)

    print("Exporting integrations...", file=stderr)
    export_object['integrations'] = pc_api.integration_list_read()

    print("Integrations returned...", file=stderr)
    for integration in export_object['integrations']:
        print("  %s %s" % ( integration['id'], integration['name']), file=stderr)

    print("Exporting notification templates...", file=stderr)
    export_object['notification_templates'] = pc_api.notification_template_list_read()

    print("Notification templates returned...", file=stderr)
    for notification_template in export_object['notification_templates']:
        print("  %s %s" % ( notification_template['id'], notification_template['name']), file=stderr)

    print("Exporting report configurations...", file=stderr)
    export_object['report_configs'] = pc_api.compliance_report_list_read()

    print("Report configurations returned...", file=stderr)
    for report_config in export_object['report_configs']:
        print("  %s %s" % ( report_config['id'], report_config['name']), file=stderr)

    print("Exporting enterprise settings...", file=stderr)
    export_object['settings'] = pc_api.enterprise_settings_list_read()

    print("Enterprise settings returned...", file=stderr)
    print(dumps(export_object['settings']), file=stderr)

    print("Exporting accounts...", file=stderr)
    export_object['accounts'] = pc_api.cloud_accounts_list_read()

    print("Accounts returned...", file=stderr)
    for account in export_object['accounts']:
        print("  %s %s" % (account['accountId'], account['name']), file=stderr)

    print("Exporting account groups...", file=stderr)
    export_object['groups'] = pc_api.cloud_account_group_list_read()

    print("Account groups returned...", file=stderr)
    for group in export_object['groups']:
        print("  %s %s" % (group['id'], group['name']), file=stderr)
        for accountId in group['accountIds']:
            print("    %s" %accountId, file=stderr)

    print("Exporting alert rules...", file=stderr)
    export_object['rules'] = pc_api.alert_rule_list_read()

    print("Alert rules returned...", file=stderr)
    for rule in export_object['rules']:
       print("  %s %s" % (rule['policyScanConfigId'], rule['name']), file=stderr)

    print("Exporting policies...", file=stderr)
    export_object['policies'] = pc_api.policy_v2_list_read()

    print("Policies returned...", file=stderr)
    for policy in export_object['policies']:
        print("  %s %s" % (policy['policyId'], policy['name']), file=stderr)

    print("Exporting saved searches...", file=stderr)
    export_object['searches'] = pc_api.saved_search_list_read()

    print("Saved searches returned...", file=stderr)
    for search in export_object['searches']:
        print("  %s %s" % ( search['id'], search['searchName']), file=stderr)

    print("Exporting compliance standards...", file=stderr)
    export_object['standards'] = pc_api.compliance_standard_list_read()

    print("Compliance standards returned...", file=stderr)
    for standard in export_object['standards']:
        print("  %s %s" % ( standard['id'], standard['name']), file=stderr)

    print("Exporting compliance standard requirements...", file=stderr)
    for standard in export_object['standards']:
        print("Exporting compliance standard requirements for standard %s %s..." % (standard['id'], standard['name']), file=stderr)
        export_object['requirements'] = pc_api.compliance_standard_requirement_list_read(standard['id'])

        for requirement in export_object['requirements']:
            print("Exporting compliance standard requirement sections for requirement %s/%s %s" % (standard['id'], requirement['id'], requirement['name']), file=stderr)
            export_object['sections'] = pc_api.compliance_standard_requirement_section_list_read(requirement['id'])

            for section in export_object['sections']:
                print("Exported compliance standard requirement section %s/%s/%s %s" % ( standard['id'], requirement['id'], section['id'], section['sectionId']), file=stderr)

except:
    print("Something went wrong talking to the API", file=stderr)
    sys_exit(2)

try:
    if args.export_file_name == '-':
        print(dumps(export_object), file=stdout)
    else:
        pc_utility.write_json_file(args.export_file_name,export_object,pretty=bool(args.pretty))
        print("Export written to %s" % args.export_file_name, file=stderr)
except:
    print("Something went wrong writing output %s" % args.export_file_name, file=stderr)
    sys_exit(1)
