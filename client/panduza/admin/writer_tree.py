import os
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass


@dataclass
class TreeWriter:
    filepath: str

    def write(self):
        tree = {
            "machine": "rename_this_machine",
            "brokers": {
                "rename_this_broker": {
                    "addr": "localhost",
                    "port": 1883,
                    "interfaces": [
                        {
                            "name": "fake_bps",
                            "driver": "py.bps.fake"
                        }
                    ]
                }
            }
        }
        with open(self.filepath, 'w') as f:
            print(f" + Write file '{self.filepath}'")
            f.write(json.dumps(tree, indent=4))



