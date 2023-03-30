import datetime
import json
import math

import pandas as pd
import configuration as config
import src.db_handler as db_handler
from logger import logger
import src.new_vendors_handler as new_vendors_handler
import src.old_vendors_handler as old_vendors_handler

INPUT_PATH = "C:\\Users\\noam\\PycharmProjects\\vendor-chooser\\vendors.csv"

def _retrieve_vendors(category, possible_vendors):
    orig_df = db_handler.read_from_db(category, "', '".join(possible_vendors))
    orig_df.columns = [config.VENDOR_ID, config.VENDOR_NAME, config.EMAIL,config.CATEGORY_ID, config.CATEGORY_NAME, config.DATE_ADDED,
                       config.TOTAL_NUMBER_OF_PROJECTS, config.AVG_RATING, config.AVG_RESPONSE_TIME,
                       config.NUMBER_OF_REJECTED, config.NUMBER_OF_ACTIVE, config.NUMBER_OF_REASSIGNED]
    return orig_df


def _retrieve_vendors_from_csv():
    orig_df = pd.read_csv(INPUT_PATH, encoding='ISO-8859-1', skipinitialspace=True, error_bad_lines=False)
    orig_df.columns = [config.VENDOR_ID, config.VENDOR_NAME, config.CATEGORY_ID, config.CATEGORY_NAME, config.DATE_ADDED,
                       config.TOTAL_NUMBER_OF_PROJECTS, config.AVG_RATING, config.AVG_RESPONSE_TIME,
                       config.NUMBER_OF_REJECTED, config.NUMBER_OF_ACTIVE, config.NUMBER_OF_REASSIGNED]
    return orig_df


## calc the average values
def _retrieve_avg_values_from_df(df_vendors_all):
    df_vendors_filled = df_vendors_all.fillna(value=0)
    avg_response_time_all = df_vendors_filled[df_vendors_filled[config.AVG_RESPONSE_TIME] > 0][config.AVG_RESPONSE_TIME].mean()
    avg_rating_all = df_vendors_filled[df_vendors_filled[config.AVG_RATING] > 0][config.AVG_RATING].mean()
    rejected_all = 0
    reassigned_all = 0
    active_all = 0
    return avg_response_time_all, avg_rating_all, rejected_all, reassigned_all, active_all


## filter only the relevant vendors
def _filter_only_possible_vendors(df_vendors_all, possible_vendors):
    df_possible_vendors = df_vendors_all[df_vendors_all[config.VENDOR_ID].isin(possible_vendors)]
    return df_possible_vendors


## set average values instead of Nan / Null values
def _fix_data(df_vendors_all:pd.DataFrame, possible_vendors):
    avg_response_time_all, avg_rating_all, rejected_all, reassigned_all, active_all = _retrieve_avg_values_from_df(df_vendors_all)
    df_vendors = _filter_only_possible_vendors(df_vendors_all, possible_vendors)
    df_vendors[[config.AVG_RESPONSE_TIME]] = df_vendors[[config.AVG_RESPONSE_TIME]].fillna(value=avg_response_time_all)
    df_vendors[[config.AVG_RATING]] = df_vendors[[config.AVG_RATING]].fillna(value=avg_rating_all)
    df_vendors[[config.NUMBER_OF_REJECTED]] = df_vendors[[config.NUMBER_OF_REJECTED]].fillna(value=rejected_all)
    df_vendors[[config.NUMBER_OF_REASSIGNED]] = df_vendors[[config.NUMBER_OF_REASSIGNED]].fillna(value=reassigned_all)
    df_vendors[[config.NUMBER_OF_ACTIVE]] = df_vendors[[config.NUMBER_OF_ACTIVE]].fillna(value=active_all)

    return df_vendors


def dev_answer(possible_vendors, category):
    resp = list([])
    poss_ven = list([])
    for x in range(0, len(possible_vendors)):
        a = {
               "index": x,
               "Vendor_ID": possible_vendors[x],
               "Vendor": 'test',
               "Email": 'test@test.co',
               "Category ID": 'test',
               "category_name": category,
               "date_added": str(datetime.datetime.now()),
               "num_of_projects": x+10,
               "avg_rating": 3.5,
               "avg_response_time": 450.7142857143+(x*10),
               "number_of_rejected": x,
               "number_of_active": 1.0,
               "number_of_reassigned": 5.0+x,
               "fixed_avg_response_time": 1.0,
               "fixed_avg_rating": 1.0,
               "fixed_number_of_active": 0.9166666667,
               "fixed_rejected": 1.0,
               "fixed_reassigned": 0.4166666667,
               "value": 23.4166666667
            }
        resp.append(a)

        if 0 < x < 4:
            poss_ven.append(possible_vendors[x])
    temp = resp[0]
    temp["list_of_vendors"] = poss_ven
    return resp, temp


### main src ###
def run_flow(body:dict):
    test = False
    if 'test' in body.keys():
        if body['test']:
            test = True
    category = body[config.JSON_CATEGORY]
    if config.JSON_LAST_ASSIGNED in body:
        last_assigned_vendor_id = body[config.JSON_LAST_ASSIGNED]
    else:
        last_assigned_vendor_id = config.NO_VENDOR_ID
    possible_vendors = body[config.JSON_POSSIBLE_VENDORS]
    # df_vendors = _retrieve_vendors_from_csv()
    df_vendors_all = _retrieve_vendors(category, possible_vendors)
    if len(df_vendors_all) == 0:
        logger.log("no vendors found")
        return {'1': 'no pro_auto_assign vendors found'}, json.dumps({}), None
    if test:
        resp, a_resp = dev_answer(possible_vendors, body['category'])
        a = {'1': a_resp}
        b = json.dumps({'dev': resp})
        c = 'old'
        return a, b, c

    df_vendors = _fix_data(df_vendors_all, possible_vendors)

    new_vendor, new_vendors_df_sorted, chosen_vendor_state, list_of_new_vendors = new_vendors_handler.handle_new_vendors(df_vendors, last_assigned_vendor_id)
    old_vendor, old_vendors_df_sorted, chosen_vendor_state, list_of_old_vendors = old_vendors_handler.handler_old_vendors(df_vendors,
                                                                                                        last_assigned_vendor_id)

    chosen_vendor = new_vendor
    if chosen_vendor is None:
        chosen_vendor = old_vendor

    ## combine two df into one and convert to json
    df_all_vendor_sorted = pd.concat([new_vendors_df_sorted, old_vendors_df_sorted])
    df_all_vendor_sorted = df_all_vendor_sorted.fillna('')
    vendor_df_sorted_for_js = df_all_vendor_sorted
    vendor_df_sorted_for_js[config.DATE_ADDED] = vendor_df_sorted_for_js[config.DATE_ADDED].astype(str)
    df_all_vendors_js = vendor_df_sorted_for_js.to_json(orient='records')

    if config.IS_TEST:
        logger.log('and the winning vendor is {}'.format(chosen_vendor))

    vendor_to_dict = pd.Series.to_dict(chosen_vendor)
    vendor_to_dict['date_added'] = str(vendor_to_dict["date_added"])
    # list_of_vendors is set from the best vendor to the worst
    list_of_vendors = list_of_new_vendors + list_of_old_vendors
    vendor_to_dict['list_of_vendors'] = list_of_vendors
    vendor_to_dict_ext = {'1': vendor_to_dict}
    # vendor_json = json.dumps(vendor_to_dict_ext, indent=3)
    # return vendor_json, output_json, chosen_vendor_state
    for key, val in vendor_to_dict_ext['1'].items():
        if val != val:
            vendor_to_dict_ext['1'][key] = ''
    return vendor_to_dict_ext, df_all_vendors_js, chosen_vendor_state

if __name__ == '__main__':
#     # run_flow()
#     # run_flow(last_assigned_vendor_id=1)
#
#
#     jst = {'category': 'Appliance Installer / Repair', 'location_id': 'E17467CD-780C-4067-AC07-AB35B48EC22E', 'incident_id': '915844AB-6B46-4D4B-A359-F6B7CA84A8F8', 'possible_vendors': ('5392B43C-0741-4958-B144-A677AA1F907F', '7366BD64-5679-4C36-9133-AFDCA934DCD1', '2BB23931-652A-44AD-AD18-B4B09FE4916E', 'C3E72AA4-1D2C-426A-B0D1-F3AD78DDEB21', '19BA08DE-7509-4AA0-AB53-37447CA91D98'),'test':False}
    jsr = {
  "category": "Property onboarding Inspection",
  "location_id": "F90E128A-CD00-4DF7-B0D0-0F40F80D623A",
  "incident_id": "1D97B2D0-DB01-420E-A8F1-8CDA2AEA4CBC",
  "possible_vendors": [
    "645202C1-C33A-4E3B-A51E-8184F1AA84F7",
    "B366F057-C1BD-4C73-B2E4-F823EE8434AB",
    "37754174-2E40-446E-9D26-29E8F66DDDAE"
  ]
}
#     ## from vendor classification lambda
#     # jst = {"category": "Handyman","location_id": "96850294-39FB-4B7C-AB0A-20A815431CFF","incident_id": "3E9EBEFF-EA20-4048-8E6D-AEF33BDA4103","possible_vendors": ["1D16BF8C-C2B9-4256-A073-57AAE84C89E5","7DBC288E-FFC3-4FF3-88E5-613F4B90EEBB","2868ADF1-E7EE-47DD-9488-76A06EE2E6C3","6B4A5AFD-96A6-4B28-91E3-0AA444FD55B0","8234A43A-8CBA-41FC-AF21-DB18D33902B3"], "last_assigned_vendor_id":"3E9EBEFF-EA20-4048-8E6D-AEF33BDA4103"}
#     # jst = {'category': 'Handyman', 'location_id': '96850294-39FB-4B7C-AB0A-20A815431CFF', 'incident_id': '3E9EBEFF-EA20-4048-8E6D-AEF33BDA4103', 'possible_vendors': ['1D16BF8C-C2B9-4256-A073-57AAE84C89E5', '7DBC288E-FFC3-4FF3-88E5-613F4B90EEBB', '2868ADF1-E7EE-47DD-9488-76A06EE2E6C3', '6B4A5AFD-96A6-4B28-91E3-0AA444FD55B0', '8234A43A-8CBA-41FC-AF21-DB18D33902B3', 'EC62ED7E-4211-4743-B7FE-2C18F49F9CF8']}
#     # jst = {"category": "Garage Door Installer / Repair", "location_id": "96850294-39FB-4B7C-AB0A-20A815431CFF", "incident_id": "F9E1F50B-03E3-48EB-B673-9C1149B4B39B", "possible_vendors": ["2868ADF1-E7EE-47DD-9488-76A06EE2E6C3", "A90CC026-BC6B-4E49-BF84-29135F95AB63"]}
#     # jst = {"category": "Handyman", "location_id": "99D30DE8-DAD0-426F-A77E-755292D7DAC8", "incident_id": "19D3A6A5-1AB4-433C-B130-63FC34A3B89D", "possible_vendors": ["3CE27307-3458-4EFC-9BED-4879C7E379E0", "F95A65AA-9F21-4AA9-A97E-4C55EB38D45C", "7507DFE4-2590-48C2-B959-8B5759DC3B16", "E77BC833-0F63-4563-A972-55BF4A7515B3", "B1059EF5-DC56-4B32-84EC-90ACE8280C19", "6F0D3FF1-54E3-45C4-8AF0-9ED9F3DD4370", "04E1AC54-5639-4D63-B889-A85CCE0DC4C0", "CB486AFD-3425-4693-8632-6F619B0417B9", "2868ADF1-E7EE-47DD-9488-76A06EE2E6C3", "CDCC9D72-E3B9-4ED1-99FD-DBBD027B16C7", "17471CBD-CDAC-43B4-8716-DD7E8ED5DBBF", "B6F53A36-4370-4D66-AA43-E42640C27EDC", "33AF8625-E2C9-4B17-A81D-EB4CDD782FEF", "1428B43D-798B-4DD0-A37E-F9FA699ED868", "535DD0D8-04B4-47F4-87BE-FA2AEB28AD08", "970938BB-919D-445E-BBEB-FCAF51CF962C", "21C71D69-4621-4ADD-851F-19DF00D7A5EB", "AD8A8B52-9807-45DC-9F4E-C8AF5DBF2CAD", "26ADF3A7-4CFC-4462-9DD3-C9A71F5884FF", "A438F641-BA20-4F2D-8C75-CDEB08E7D57B", "64056CD3-A49B-4EC4-8FF3-D7782EAE077D", "EC62ED7E-4211-4743-B7FE-2C18F49F9CF8", "1852A6DC-F0D9-4337-B45A-2F62EDE9C83F", "8BAA6BD3-C408-4DA2-B8D2-3584485F76B4", "6A729443-1320-4869-87D2-380EEB79142F"]}
#     # jsr = json.dumps(jst)
#
#     # jst = {
#     #     "category": "Appliance Installer / Repair",
#     #     "location_id": "96850294-39FB-4B7C-AB0A-20A815431CFF",
#     #     "incident_id": "B895A323-ABA5-4F6B-B141-42BEE6587C8F",
#     #     "possible_vendors": [
#     #         "19BA08DE-7509-4AA0-AB53-37447CA91D98",
#     #         "D3DD9E8D-F64E-4575-A6E9-3AB7FFC1D83C",
#     #         "1D16BF8C-C2B9-4256-A073-57AAE84C89E5",
#     #         "8234A43A-8CBA-41FC-AF21-DB18D33902B3"
#     #     ]
#     # }
#     # a, b, c = run_flow(jst)
    w, e, r = run_flow(jsr)
    print("list of sorted vendors:")
    print(str(e))
#
