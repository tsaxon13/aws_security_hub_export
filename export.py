import boto3
import xlsxwriter

profiles = None
session = None
workbook_file = None


def get_profile_list():
    """
    Get list of AWS profiles.
    """
    return boto3.session.Session().available_profiles


def set_profile_list():
    """
    Set the list of AWS profiles to use.
    """
    all_profiles = get_profile_list()

    import inquirer
    questions = [inquirer.List('profiles', message="Select profile to use", choices=all_profiles), ]
    answers = inquirer.prompt(questions)
    return answers


def get_findings(session):
    client = session.client('securityhub')
    paginator = client.get_paginator('get_findings')
    page_iterator = paginator.paginate(Filters={"ComplianceStatus": [{"Value": "FAILED", "Comparison": "EQUALS"}]})

    findings = []
    for page in page_iterator:
        for finding in page["Findings"]:
            if len(finding["Resources"]) > 1:
                print("More than 1 resource!")
            resource_id = finding["Resources"][0]["Id"]
            account_id = finding["AwsAccountId"]
            title = finding["Title"]
            description = finding["Description"]
            severity = finding["Severity"]["Label"]
            record_state = finding["RecordState"]

            findings.append([title, description, record_state, account_id, severity, resource_id])

    return findings


def init():
    """
    Initialize logic.
    """
    # Set global variables
    global profiles, session, workbook_file
    # Set the list of profiles to use.
    profile = set_profile_list()['profiles']
    # get a file to write data to
    workbook_file = (input("Enter a file name to write data to ('security_hub_findings.xlsx'): ") or
                     "security_hub_findings.xlsx")
    # Create a list of boto3 sessions.
    session = boto3.session.Session(profile_name=profile)


def write_worksheet(workbook, worksheet_name, data):
    """
    Write data to the worksheet.
    """
    worksheet = workbook.add_worksheet(worksheet_name)

    for row_num, row_data in enumerate(data):
        for col_num, cell_data in enumerate(row_data):
            worksheet.write(row_num, col_num, cell_data)

    worksheet.autofilter(0, 0, len(data), len(data[0]) - 1)
    max_col_sizes = [max([len(str(data[row][col])) for row in range(len(data))]) for col in range(len(data[0]))]

    col = 0
    for max_col_size in max_col_sizes:
        worksheet.set_column(col, col, max_col_size * 1.2)
        col += 1


def main():
    init()

    workbook = xlsxwriter.Workbook(workbook_file)

    findings = get_findings(session)
    findings.insert(0, ["Title", "Description", "Record Stat", "Account ID", "Severity", "Resource Id"])
    write_worksheet(workbook, "Security Hub Findings", findings)

    workbook.close()


if __name__ == "__main__":
    main()
