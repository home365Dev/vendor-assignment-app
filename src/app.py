import logging
import src.flow_runner as fr
from logger import logger

import json

def execute(data:dict):
    my_json_str = json.dumps(data)
    logger.info('event parameter: {}'.format(my_json_str))
    # print("Received event: " + json.dumps(event, indent=2))
    body_check = data
    body = body_check
    if isinstance(body_check, str):
        body = json.loads(body_check)
    logger.info("Received body:  " + str(my_json_str))
    try:
        vendor_dict, output_json, chosen_vendor_state = fr.run_flow(body)
        output_json = output_json.replace("'", "''")
        return vendor_dict, output_json, chosen_vendor_state
    except Exception as e:
        logger.error(e)
        logger.error(json.dumps({'error': str(e)}))
        json_dict = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        return json_dict, None, None


if __name__ == '__main__':
    # jst = {'category': 'Appliance Installer / Repair', 'location_id': 'E17467CD-780C-4067-AC07-AB35B48EC22E',
    #        'incident_id': '915844AB-6B46-4D4B-A359-F6B7CA84A8F8', 'possible_vendors': (
    #     '5392B43C-0741-4958-B144-A677AA1F907F', '7366BD64-5679-4C36-9133-AFDCA934DCD1',
    #     '2BB23931-652A-44AD-AD18-B4B09FE4916E', 'C3E72AA4-1D2C-426A-B0D1-F3AD78DDEB21',
    #     '19BA08DE-7509-4AA0-AB53-37447CA91D98')}

    # jst = {
    #   "category": "Plumber",
    #   "location_id": "99D30DE8-DAD0-426F-A77E-755292D7DAC8",
    #   "incident_id": "FB30DC3D-A4E2-4B89-969D-2293DB20C6FF",
    #   "possible_vendors": [
    #     "3CE27307-3458-4EFC-9BED-4879C7E379E0",
    #     "F8207A84-E782-4CD9-A005-4A18BE14CD4C",
    #     "6F0D3FF1-54E3-45C4-8AF0-9ED9F3DD4370",
    #     "04E1AC54-5639-4D63-B889-A85CCE0DC4C0",
    #     "CB486AFD-3425-4693-8632-6F619B0417B9",
    #     "17471CBD-CDAC-43B4-8716-DD7E8ED5DBBF",
    #     "B106576D-3A10-4086-A4FC-1354C51680B0",
    #     "1428B43D-798B-4DD0-A37E-F9FA699ED868",
    #     "535DD0D8-04B4-47F4-87BE-FA2AEB28AD08",
    #     "21C71D69-4621-4ADD-851F-19DF00D7A5EB",
    #     "2BF29362-DA2D-4766-AE9A-2066B405250F",
    #     "0529DFE6-16B3-4AD2-8377-B5601B24A7E5",
    #     "4B35F51B-6DDC-4CCB-8B7D-2C9F02A97B2F",
    #     "1852A6DC-F0D9-4337-B45A-2F62EDE9C83F",
    #     "4228EF7B-CB3E-4D4E-9E66-4242F08279BD",
    #     "AD8A8B52-9807-45DC-9F4E-C8AF5DBF2CAD",
    #     "26ADF3A7-4CFC-4462-9DD3-C9A71F5884FF"
    #   ]
    # }

    # jst = {
    #   'category': 'Gardener and Landscape Architect',
    #   'location_id': '99D30DE8-DAD0-426F-A77E-755292D7DAC8',
    #   'incident_id': 'A4318C9B-CA62-483E-8C49-1E2ABE77B4C0',
    #   'possible_vendors': [
    #     'CB486AFD-3425-4693-8632-6F619B0417B9',
    #     '2A70AE2E-329F-47B2-AF20-7439379983F9',
    #     '21C71D69-4621-4ADD-851F-19DF00D7A5EB',
    #     '64056CD3-A49B-4EC4-8FF3-D7782EAE077D',
    #     'D3DD9E8D-F64E-4575-A6E9-3AB7FFC1D83C',
    #     '89888CC1-9186-41DD-A528-E0D8D229E8EE',
    #     'B6F53A36-4370-4D66-AA43-E42640C27EDC'
    #   ]
    # }

    jst = {
      "category": "Property onboarding Inspection",
      "location_id": "F90E128A-CD00-4DF7-B0D0-0F40F80D623A",
      "incident_id": "1D97B2D0-DB01-420E-A8F1-8CDA2AEA4CBC",
      "possible_vendors": [
        "8F00C0AF-710D-4B3D-AF35-5BB2B902CDD3",
        "645202C1-C33A-4E3B-A51E-8184F1AA84F7",
        "B366F057-C1BD-4C73-B2E4-F823EE8434AB",
        "37754174-2E40-446E-9D26-29E8F66DDDAE"
      ]
    }

    # jst = {'category': 'Appliance Installer / Repair', 'location_id': 'E17467CD-780C-4067-AC07-AB35B48EC22E',
    #        'incident_id': '915844AB-6B46-4D4B-A359-F6B7CA84A8F8', 'possible_vendors': (
    #         '5392B43C-0741-4958-B144-A677AA1F907F', '7366BD64-5679-4C36-9133-AFDCA934DCD1',
    #         '2BB23931-652A-44AD-AD18-B4B09FE4916E', 'C3E72AA4-1D2C-426A-B0D1-F3AD78DDEB21',
    #         '19BA08DE-7509-4AA0-AB53-37447CA91D98'),
    #        'last_assigned_vendor_id': 'C3E72AA4-1D2C-426A-B0D1-F3AD78DDEB21'}
    #        #  'last_assigned_vendor_id': '5392B43C-0741-4958-B144-A677AA1F907F'}

    jsr = json.dumps(jst)
    resp = execute(jsr)
    noam = "noam"

