import pandas as pd
import xml.etree.ElementTree as ET

def parse_appdynamics_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    data = []

    for call in root.findall(".//business-transaction"):
        row = {
            "Transaction Name": call.findtext("name"),
            "Summary": call.findtext("summary"),
            "Response Time (ms)": call.findtext("response-time-ms"),
            "Calls / min": call.findtext("calls-per-minute"),
            "Errors / min": call.findtext("errors-per-minute"),
        }
        data.append(row)

    return pd.DataFrame(data)
