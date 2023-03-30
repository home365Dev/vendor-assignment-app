from dotenv import find_dotenv, load_dotenv
import uvicorn
from threading import Thread
from fastapi import Request, FastAPI, APIRouter
from src.app import execute

import threading
import json

import src.db_handler as dbh
from logger import logger


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = FastAPI()

def hello_world():
    return 'hi hi hi!'


# @app.get("/healthcheck")
# def healthcheck():
#     return {"status": "ok"}
#
#
# @app.post("/vendor-assignment")
# async def vendor_assignment(request: Request):
#     body = await request.json()
#     response, json_vendors, state = execute(body)
#     if json_vendors:
#         thread = threading.Thread(target=dbh.execute_to_db, kwargs={
#             'jsono': response, 'jsoni': body, 'output_vendors': json_vendors, 'state': state})
#         thread.start()
#     return response
#
#
# # app.include_router(app, prefix="/vendor-assignment")
# #
# # logger.info("Starting up")
#
# def run_test():
#     #
#     # jst = {'category': 'Appliance Installer / Repair', 'location_id': 'E17467CD-780C-4067-AC07-AB35B48EC22E',
#     #        'incident_id': '915844AB-6B46-4D4B-A359-F6B7CA84A8F8', 'possible_vendors': (
#     #     '5392B43C-0741-4958-B144-A677AA1F907F', '7366BD64-5679-4C36-9133-AFDCA934DCD1',
#     #     '2BB23931-652A-44AD-AD18-B4B09FE4916E', 'C3E72AA4-1D2C-426A-B0D1-F3AD78DDEB21',
#     #     '19BA08DE-7509-4AA0-AB53-37447CA91D98')}
#
#     # jst = {'category': 'Appliance Installer / Repair', 'location_id': 'E17467CD-780C-4067-AC07-AB35B48EC22E',
#     #        'incident_id': '915844AB-6B46-4D4B-A359-F6B7CA84A8F8', 'possible_vendors': (
#     #         '5392B43C-0741-4958-B144-A677AA1F907F', '7366BD64-5679-4C36-9133-AFDCA934DCD1',
#     #         '2BB23931-652A-44AD-AD18-B4B09FE4916E', 'C3E72AA4-1D2C-426A-B0D1-F3AD78DDEB21',
#     #         '19BA08DE-7509-4AA0-AB53-37447CA91D98'),
#     #        'last_assigned_vendor_id': 'C3E72AA4-1D2C-426A-B0D1-F3AD78DDEB21'}
#     #        #  'last_assigned_vendor_id': '5392B43C-0741-4958-B144-A677AA1F907F'}
#
#     # jst = {
#     #           "category":"Appliance Installer / Repair",
#     #           "location_id":"E17467CD-780C-4067-AC07-AB35B48EC22E",
#     #           "incident_id":"915844AB-6B46-4D4B-A359-F6B7CA84A8F8",
#     #           "possible_vendors":["5392B43C-0741-4958-B144-A677AA1F907F",
#     #           "7366BD64-5679-4C36-9133-AFDCA934DCD1",
#     #           "2BB23931-652A-44AD-AD18-B4B09FE4916E",
#     #           "C3E72AA4-1D2C-426A-B0D1-F3AD78DDEB21",
#     #           "19BA08DE-7509-4AA0-AB53-37447CA91D98"]
#     #         }
#
#     # jst = {"category": "Garage Door Installer / Repair", "location_id": "96850294-39FB-4B7C-AB0A-20A815431CFF", "incident_id": "F9E1F50B-03E3-48EB-B673-9C1149B4B39B", "possible_vendors": ["2868ADF1-E7EE-47DD-9488-76A06EE2E6C3", "A90CC026-BC6B-4E49-BF84-29135F95AB63"]}
#     # jst = {"category": "Handyman", "location_id": "99D30DE8-DAD0-426F-A77E-755292D7DAC8", "incident_id": "19D3A6A5-1AB4-433C-B130-63FC34A3B89D", "possible_vendors": ["3CE27307-3458-4EFC-9BED-4879C7E379E0", "F95A65AA-9F21-4AA9-A97E-4C55EB38D45C", "7507DFE4-2590-48C2-B959-8B5759DC3B16", "E77BC833-0F63-4563-A972-55BF4A7515B3", "B1059EF5-DC56-4B32-84EC-90ACE8280C19", "6F0D3FF1-54E3-45C4-8AF0-9ED9F3DD4370", "04E1AC54-5639-4D63-B889-A85CCE0DC4C0", "CB486AFD-3425-4693-8632-6F619B0417B9", "2868ADF1-E7EE-47DD-9488-76A06EE2E6C3", "CDCC9D72-E3B9-4ED1-99FD-DBBD027B16C7", "17471CBD-CDAC-43B4-8716-DD7E8ED5DBBF", "B6F53A36-4370-4D66-AA43-E42640C27EDC", "33AF8625-E2C9-4B17-A81D-EB4CDD782FEF", "1428B43D-798B-4DD0-A37E-F9FA699ED868", "535DD0D8-04B4-47F4-87BE-FA2AEB28AD08", "970938BB-919D-445E-BBEB-FCAF51CF962C", "21C71D69-4621-4ADD-851F-19DF00D7A5EB", "AD8A8B52-9807-45DC-9F4E-C8AF5DBF2CAD", "26ADF3A7-4CFC-4462-9DD3-C9A71F5884FF", "A438F641-BA20-4F2D-8C75-CDEB08E7D57B", "64056CD3-A49B-4EC4-8FF3-D7782EAE077D", "EC62ED7E-4211-4743-B7FE-2C18F49F9CF8", "1852A6DC-F0D9-4337-B45A-2F62EDE9C83F", "8BAA6BD3-C408-4DA2-B8D2-3584485F76B4", "6A729443-1320-4869-87D2-380EEB79142F"]}
#     # jst = {"category": "Handyman", "location_id": "96850294-39FB-4B7C-AB0A-20A815431CFF", "incident_id": "B895A323-ABA5-4F6B-B141-42BEE6587C8F", "possible_vendors": ["7DBC288E-FFC3-4FF3-88E5-613F4B90EEBB", "19BA08DE-7509-4AA0-AB53-37447CA91D98", "D3DD9E8D-F64E-4575-A6E9-3AB7FFC1D83C", "1D16BF8C-C2B9-4256-A073-57AAE84C89E5", "8234A43A-8CBA-41FC-AF21-DB18D33902B3"]}
#     jst = {
#         "category": "Plumber",
#         "location_id": "99D30DE8-DAD0-426F-A77E-755292D7DAC8",
#         "incident_id": "FB30DC3D-A4E2-4B89-969D-2293DB20C6FF",
#         "possible_vendors": [
#             "3CE27307-3458-4EFC-9BED-4879C7E379E0",
#             "F8207A84-E782-4CD9-A005-4A18BE14CD4C",
#             "6F0D3FF1-54E3-45C4-8AF0-9ED9F3DD4370",
#             "04E1AC54-5639-4D63-B889-A85CCE0DC4C0",
#             "CB486AFD-3425-4693-8632-6F619B0417B9",
#             "17471CBD-CDAC-43B4-8716-DD7E8ED5DBBF",
#             "B106576D-3A10-4086-A4FC-1354C51680B0",
#             "1428B43D-798B-4DD0-A37E-F9FA699ED868",
#             "535DD0D8-04B4-47F4-87BE-FA2AEB28AD08",
#             "21C71D69-4621-4ADD-851F-19DF00D7A5EB",
#             "2BF29362-DA2D-4766-AE9A-2066B405250F",
#             "0529DFE6-16B3-4AD2-8377-B5601B24A7E5",
#             "4B35F51B-6DDC-4CCB-8B7D-2C9F02A97B2F",
#             "1852A6DC-F0D9-4337-B45A-2F62EDE9C83F",
#             "4228EF7B-CB3E-4D4E-9E66-4242F08279BD",
#             "AD8A8B52-9807-45DC-9F4E-C8AF5DBF2CAD",
#             "26ADF3A7-4CFC-4462-9DD3-C9A71F5884FF"
#         ]
#     }
#     body_json = json.dumps(jst)
#
#     response, json_vendors, state = execute(jst)
#     thread = threading.Thread(target=dbh.execute_to_db, kwargs={
#         'jsono': response, 'jsoni': jst, 'output_vendors': json_vendors, 'state': state})
#     thread.start()


if __name__ == "__main__":
    Thread(target=hello_world, daemon=True).start()
    uvicorn.run(app, host='0.0.0.0', port=8080)

    # run_test()
