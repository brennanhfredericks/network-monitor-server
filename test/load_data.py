import json
import os


def get_submitter_service_data():
    """
    - post process data that was stored locally by the submission service
    """
    base_path = "./test/data/submitter_service"
    data_files = os.listdir(base_path)

    for f in data_files:
        file_path = os.path.join(base_path, f)
        with open(file_path, "r") as fin:
            for line in fin:
                yield json.loads(line)