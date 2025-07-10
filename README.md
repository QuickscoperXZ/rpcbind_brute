Простенький тестовый инструмент для проверки UUID-ов торчащих наружу RPC-портов без 135 порта 

Адекватных тестов не проводилось, так что работает крайне не стабильно)

Зависимости: impacket

Использование: `python3 rpc_uuid_brute.py <ip> <timeout>`

UUID-ы взяты с https://ru.scribd.com/document/538595019/MS-RPC-UUID-Mappings-Juniper-Networks

---

Little tool to brute UUID of exposed RPC ports, without port mapper exposed

No test were made, so it might (and will lmao) work unstable

Dependencies: impacket

Usage: `python3 rpc_uuid_brute.py <ip> <timeout>` 

UUIDs taken from https://ru.scribd.com/document/538595019/MS-RPC-UUID-Mappings-Juniper-Networks
