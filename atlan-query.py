import os, json
from dotenv import load_dotenv
from pyatlan.client.atlan import AtlanClient

load_dotenv()

ATLAN_BASE_URL = os.getenv("ATLAN_BASE_URL")
ATLAN_API_KEY = os.getenv("ATLAN_API_KEY")

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