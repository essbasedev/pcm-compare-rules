ignore_list = ['Ruleset Name', 'Rule Name', 'Rule No', 'Dimension']


class ExtractXML:
    def __init__(self, path, name):
        self.ruleset_summary = []
        self.rule_summary = []
        self.rule_detail = []
        self.csv_export = []
        self.ruleset_name = None
        self.rule_name = None
        self.rule_no = None
        self.dimension = None
        self.ruleset_id = None
        self.ruleset_enabled = None
        self.global_context = None
        self.ruleset_sequence = None
        self.iterations = None
        self.execution_mode = None
        self.rule_id = None
        self.rule_name = None
        self.rule_enabled = None
        self.rule_no = None
        self.rule_sequence = None
        self.ruleset_context = None
        self.rule_type = None
        self.driver_selection = None
        self.allocation_amount = None
        self.name = name
        self.path = path
        self.application_name = None

    def find_dimension_members(self, find_tag, component_name_key, component_name_val, item):
        tag_to_search = item.findChildren(find_tag)
        if tag_to_search:
            for child in tag_to_search:
                entry_list = child.findChildren('entry')
                for entry in entry_list:
                    key = entry.find('key').text
                    self.add_to_rule_detail(component_name_key, key)
                    if entry.find('value').text:
                        val = key + entry.find('value').text
                        self.add_to_rule_detail(component_name_val, val)

    def add_to_rule_detail(self, component, value):
        self.rule_detail.append({
            'Rule Name': self.rule_name,
            'Rule No': self.rule_no,
            'Dimension': self.dimension,
            'Ruleset Name': self.ruleset_name,
            component: value,
        })

    # This function adds the values into dictionaries inside a list,
    # This can be easily exported as table or csv
    def add_to_csv_export(self, source_list, application_name, sheet_name, job_type):
        for item in source_list:
            for component in item:
                if component not in ignore_list:
                    self.ruleset_name = item.get('Ruleset Name') if item.get('Ruleset Name') else ""
                    self.rule_name = item.get('Rule Name') if item.get('Rule Name') else ""
                    self.rule_no = item.get('Rule No') if item.get('Rule No') else ""
                    self.dimension = item.get('Dimension') if item.get('Dimension') else ""
                    self.csv_export.append({
                        'Application Name': application_name,
                        'Sheet Name': sheet_name,
                        'Check': job_type,
                        'Ruleset Name': self.ruleset_name,
                        'Rule Name': self.rule_name,
                        'Rule No': self.rule_no,
                        'Dimension': self.dimension,
                        'Component': component,
                        'Value': item[component],
                    })
