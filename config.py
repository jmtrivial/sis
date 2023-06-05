import os

configs = {
    "crdv": {
        "host" : "192.168.0.10",
        "folder_path" : "\\\\CRDV-DS418\\Biblio_sonore\\SIS\\",
        "input_device": 8,
        "output_device": 8
    },
    "linux.jm": {
        "host" : "127.0.0.1",
        "folder_path" : os.path.realpath(os.path.dirname(__file__)),
        "input_device": 0,
        "output_device": 0
    }
}

config = configs["linux.jm"]
    