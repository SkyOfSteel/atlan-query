import os, json
from dotenv import load_dotenv
from pyatlan.client.atlan import AtlanClient

load_dotenv()

ATLAN_BASE_URL = os.getenv("ATLAN_BASE_URL")
ATLAN_API_KEY = os.getenv("ATLAN_API_KEY")

CONNECTION_QN = "default/redshift/1712865454"
DATABASE_QN = "default/redshift/1712865454/nfl-dna-gridiron-prd"
CONNECTION_LABEL = "nfl-redshift-gridiron-datapump-prd"

DEC_KEY = "WCBh7f0JK8naMz3FBMWFly"
ASSET_TYPES = ['Table', 'View', 'Column']

def hierarchy_row(schema_qns):
    """Build the connection/database/schema row from a list of schema qualified names."""
    
    if schema_qns:
        attribute_name = "schemaQualifiedName"
        attribute_value = ";".join([DATABASE_QN] + schema_qns)
    
    else:
        attribute_name = "databaseQualifiedName"
        attribute_value = DATABASE_QN

    return {"key": "hierarchy", 
            "operator": "eq", 
            "value":
            {"connectionQualifiedName": CONNECTION_QN, 
             "attributeValue": attribute_value,
             "attributeName": attribute_name},
             "isLocked": False,
             "isMuted": False,
             "label": CONNECTION_LABEL}

def name_row(code):
    """Build the 'Qualified name contains <code>_' row."""

    return {'key': 'qualifiedName', 
            'operator': 'contains', 
            'value': [code.lower() + "_"], 
            'isLocked': False, 
            'isMuted': False, 
            'label': 'Qualified name'}

def type_row():
    """Build the 'Asset type is Table, View or Column' row."""
    return {'key': '__typeName.keyword', 
            'operator': 'eq', 
            'value': ASSET_TYPES, 
            'isLocked': False, 
            'isMuted': False, 
            'label': 'Asset type'}

def dec_row(code):
    """Build the 'Related DEC is <CODE>' row."""
    return {'key': DEC_KEY, 
            'operator': 'eqAnd', 
            'value': [code.upper()], 
            'isLocked': False, 
            'isMuted': False, 
            'label': 'Related DEC'}

client = AtlanClient()

client.user.get_current()

acx = client.asset.get_by_guid("b4d44fd5-16e3-4b2a-b344-cab3da3224ea")
dyc = client.asset.get_by_guid("1a90e9f2-60fc-4c0c-b2be-c11060bef402")

filter_text = dyc.data_product_assets_playbook_filter
rules = json.loads(filter_text)
print(json.dumps(rules, indent=2, sort_keys=True))

dsl_text = dyc.data_product_assets_d_s_l
dsl_rules = json.loads(dsl_text)
print(dsl_rules.keys())
print(dsl_rules["query"].keys())
print(json.dumps(dsl_rules["query"]["dsl"], indent=2, sort_keys=True))

acx_filter = json.loads(acx.data_product_assets_playbook_filter)
target = acx_filter["rules"][0]["rules"][0]
print(json.dumps(target, indent=2))

built = hierarchy_row([DATABASE_QN + "/raw_reference_population"])
print("============================")
print(json.dumps(built, indent=2))
print(built == target)

target_all = acx_filter["rules"][1]["rules"][0]
print("****************************")
print(json.dumps(target_all, indent=2))

print(hierarchy_row([DATABASE_QN + "/raw_reference_population"]) == acx_filter["rules"][0]["rules"][0])
print(hierarchy_row([]) == acx_filter["rules"][1]["rules"][0])

dyc_filter = json.loads(dyc.data_product_assets_playbook_filter)

print("^^^^^^^^^^^^^^^^^^^^^^^^^^^")

print(name_row("ACX") == acx_filter["rules"][0]["rules"][1])
print(type_row() == acx_filter["rules"][0]["rules"][2])
print(dec_row("acx") == acx_filter["rules"][1]["rules"][1])
print(name_row("DYC") == dyc_filter["rules"][0]["rules"][1])
print(dec_row("dyc") == dyc_filter["rules"][1]["rules"][1])

print(acx_filter["rules"][0]["rules"][2])
print(type_row())