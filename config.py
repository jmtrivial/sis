import os

configs = {
    "crdv": {
        "host" : "192.168.0.10",
        "server_port": 14000,
        "folder_path" : "\\\\CRDV-DS418\\Biblio_sonore\\SIS\\",
        "input_device": 8,
        "output_device": 8,
        "library_dir": "bibliotheque"
    },
    "linux.jm": {
        "server_host" : "127.0.0.1",
        "server_port": 14000,
        "folder_path" : os.path.realpath(os.path.dirname(__file__)),
        "input_device": 0,
        "output_device": 0,
        "library_dir": "bibliotheque"
    }
}

config = configs["linux.jm"]
    