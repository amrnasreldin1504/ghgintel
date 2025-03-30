# scada_client.py
import json
import os

def get_scada_data():
    """
    Retrieve SCADA data.
    For simulation, we load the data from 'sample_data/scada_data.json'.
    In a live deployment, this function could connect to an OPC UA server.
    """
    file_path = os.path.join("sample_data", "scada_data.json")
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        # If reading fails, return an empty SCADA structure.
        data = {"timestamp": "", "scope": {}}
    return data