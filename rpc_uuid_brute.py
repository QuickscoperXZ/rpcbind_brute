from impacket.dcerpc.v5.rpcrt import DCERPC_v5
from impacket.dcerpc.v5 import transport
import sys
import time

common_uuids = {
    'LSAD': '12345778-1234-ABCD-EF00-0123456789AB',
    'SAMR': '12345778-1234-ABCD-EF00-0123456789AC',
    'SRVSVC': '4B324FC8-1670-01D3-1278-5A47BF6EE188',
    'SPOOLSS': '12345678-1234-ABCD-EF00-0123456789AB',
    'NRPC': '12345678-1234-ABCD-EF00-01234567CFFB',
    'WINREG': '338CD001-2244-31F1-AAAA-900038001003',
    'ATSVC': '1FF70682-0A51-30E8-076D-740BE8CEE98B',
    'WMI': '8BC3F05E-D86B-11D0-A075-00C04FB68820',
    'LOGS': '82273FDC-E32A-18C3-3F78-827929DC23EA',
    'DRSUAPI': 'e3514235-4b06-11d1-ab04-00c04fc2dcd2',
    'DPAPI': '7c44d7d4-31d5-424c-bd5e-2b3e1f323d22',
    'EPM': 'e1af8308-5d1f-11c9-91a4-08002b14a0fa',
    'AD-BR': 'ecec0d70-a603-11d0-96b1-00a0c91ece30',
    'AD-BR_1': '16e0cf3a-a604-11d0-96b1-00a0c91ece30',
    'MS-AD-DRSUAPI': 'e3514235-4b06-11d1-ab04-00c04fc2dcd2',
    'DSROLE': '1cbcad78-df0b-4934-b558-87839ea501c9',
    'DSSETUP': '3919286a-b10c-11d0-9ba8-00c04fd92ef5',
    'DTC': '906b0ce0-c70b-1067-b317-00dd010662da',
    'MS-EXCHANGE-DATABASE': '1a190310-bb9c-11cd-90f8-00aa00466520',
    'MS-EXCHANGE-DIRECTORY': 'f5cc5a18-4264-101a-8c59-08002b2f8426',
    'MS-EXCHANGE-DIRECTORY_1': 'f5cc5a7c-4264-101a-8c59-08002b2f8426',
    'MS-EXCHANGE-DIRECTORY_2': 'f5cc59b4-4264-101a-8c59-08002b2f8426',
    'MS-EXCHANGE-INFO-STORE': '0e4a0156-dd5d-11d2-8c2f-00c04fb6bcde',
    'MS-EXCHANGE-INFO-STORE_1': '1453c42c-0fa6-11d2-a910-00c04f990f3b',
    'MS-EXCHANGE-INFO-STORE_2': '10f24e8e-0fa6-11d2-a910-00c04f990f3b',
    'MS-EXCHANGE-INFO-STORE_3': '1544f5e0-613c-11d1-93df-00c04fd7bd09',
    'MS-EXCHANGE-MTA': '9e8ee830-4459-11ce-979b-00aa005ffebe',
    'MS-EXCHANGE-MTA_1': '38a94e72-a9bc-11d2-8faf-00c04fa378ff',
    'MS-EXCHANGE-STORE': '99e66040-b032-11d0-97a4-00c04fd6551d',
    'MS-EXCHANGE-STORE_1': '89742ace-a9ed-11cf-9c0c-08002be7ae86',
    'MS-EXCHANGE-STORE_2': 'a4f1db00-ca47-1067-b31e-00dd010662da',
    'MS-EXCHANGE-STORE_3': 'a4f1db00-ca47-1067-b31f-00dd010662da',
    'MS-EXCHANGE-SYSATD': '67df7c70-0f04-11ce-b13f-00aa003bac6c',
    'MS-EXCHANGE-SYSATD_1': 'f930c514-1215-11d3-99a5-00a0c9b61b04',
    'MS-EXCHANGE-SYSATD_2': '469d6ec0-0d87-11ce-b13f-00aa003bac6c',
    'MS-EXCHANGE-SYSATD_3': '06ed1d30-d3d3-11cd-b80e-00aa004b9c30',
    'MS-EXCHANGE-SYSATD_4': '83d72bf0-0d89-11ce-b13f-00aa003bac6c',
    'MS-FRS': 'f5cc59b4-4264-101a-8c59-08002b2f8426',
    'MS-FRS_1': 'd049b186-814f-11d1-9a3c-00c04fc9b232',
    'MS-FRS_2': 'a00c021c-2be2-11d2-b678-0000f87a8f8e',
    'MS-IIS-COM': '70b51430-b6ca-11d0-b9b9-00a0c922e750',
    'MS-IIS-IMAP4': '2465e9e0-a873-11d0-930b-00a0c90ab17c',
    'MS-IIS-INETINFO': '82ad4280-036b-11cf-972c-00aa006887b0',
    'MS-IIS-NNTP': '4f82f460-0e21-11cf-909e-00805f48a135',
    'MS-IIS-POP3': '1be617c0-31a5-11cf-a7d8-00805f48a135',
    'MS-IIS-SMTP': '8cfb5d70-31a4-11cf-a7d8-00805f48a135',
    'MS-ISMSERV': '68dcd486-669e-11d1-ab0c-00c04fc2dcd2',
    'MS-ISMSERV_1': '130ceefb-e466-11d1-b78b-00c04fa32883',
    'MS-MESSENGER': '17fdd703-1827-4e34-79d4-24a55c53bb37',
    'MS-MESSENGER_1': '5a7b91f8-ff00-11d0-a9b2-00c04fb6e6fc',
    'MS-MQQM': 'fdb3a030-065f-11d1-bb9b-00a024ea5525',
    'MS-MQQM_1': '76d12b80-3467-11d3-91ff-0090272f9ea3',
    'MS-MQQM_1': '1088a980-eae5-11d0-8d9b-00a02453c337',
    'MS-MQQM_2': '5b5b3580-b0e0-11d1-b92d-0060081e87f0',
    'MS-MQQM_3': '41208ee0-e970-11d1-9b9e-00e02c064c39',
    'MS-NETLOGON': '12345678-1234-abcd-ef00-01234567cffb',
    'MS-SCHEDULER': '1ff70682-0a51-30e8-076d-740be8cee98b',
    'MS-SCHEDULER_1': '378e52b0-c0a9-11cf-822d-00aa0051e40f',
    'MS-SCHEDULER_2': '0a74ef1c-41a4-4e06-83ae-dc74fb1cdd53',
    'MS-WIN-DNS ': '50abc2a4-574d-40b3-9d66-ee4fd5fba076',
    'MS-WINS': '45f52c28-7f9f-101a-b52b-08002b2efabe',
    'MS-WINS': '811109bf-a4e1-11d1-ab54-00a0c91e9b45'
}

target_ip = sys.argv[1]
timeout = sys.argv[2]

if (timeout == None):
    timeout = 0
print(timeout)

target_ports = [49664, 49665, 49666, 49669, 49672, 49702, 49703, 49708, 62499]
for target_port in target_ports:
    print("\033[36mTrying "+str(target_port)+"\033[!p")
    for name, uuid in common_uuids.items():
        try:
            trans = transport.DCERPCTransportFactory(f"ncacn_ip_tcp:{target_ip}[{target_port}]")
            dce = trans.get_dce_rpc()
            dce.connect()
            dce.bind(uuid)
            print(f"Connected: {name} - {uuid}")
            dce.disconnect()
        except Exception as e:
            print(f"Failed {name}: {str(e)}")
    time.sleep(timeout) #optional