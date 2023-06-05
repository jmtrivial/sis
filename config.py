import os

config = {
        "server_port": 14000,
        "library_dir": "bibliotheque",
        "virtual_speaker_distance": 5,
        "global_volume": 0.15
}

configs = {
    "crdv": {
        "server_host" : "192.168.0.10",
        "folder_path" : "\\\\CRDV-DS418\\Biblio_sonore\\SIS\\",
        "input_device": 8,
        "output_device": 8
    },
    "linux.jm": {
        "server_host" : "127.0.0.1",
        "folder_path" : os.path.realpath(os.path.dirname(__file__)),
        "input_device": 7,
        "output_device": 7
    }
}

config.update(configs["linux.jm"])
    