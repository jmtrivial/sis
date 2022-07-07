from webdav3.client import Client
import lxml.etree as etree
import os
import shutil
from pydub import AudioSegment

class AudioLibrary:

    def __init__(self, options):
        self.client = Client(options)
        self.audio_library = options["audio_library"]
        self.mime_types = ["audio/mpeg", "audio/wav"]
        

    def list_audio_files_recursive(self, dir=None):
        directory_url = self.audio_library if dir == None else dir
        result = []

        response = self.client.list(directory_url, get_info=True)
        for e in response:
            if e["isdir"]:
                result += self.list_audio_files_recursive(e["path"])
            else:
                if e["content_type"] in self.mime_types:
                    result.append(e["path"].replace(self.audio_library, ""))

        return result


    def get_audio_files_recursive(self, local_directory):
        files = self.list_audio_files_recursive()
        os.makedirs(local_directory, exist_ok=True)
        os.makedirs(local_directory + "/tmp", exist_ok=True)
        
        for f in files:
            os.makedirs(os.path.dirname(local_directory + f), exist_ok=True)
            print("Téléchargement de " + f)
            if "wav" in f:
                self.client.download(self.audio_library + f, local_directory + f)
            else :
                # convert wav to mp3    
                self.client.download(self.audio_library + f, local_directory + "/tmp/" + os.path.basename(f).split('.')[0])                                                        
                sound = AudioSegment.from_mp3(local_directory + "/tmp/" + os.path.basename(f).split('.')[0])
                sound.export(os.path.dirname(local_directory + f) + "/" +os.path.basename(f).split('.')[0] + ".wav", format="wav")
        shutil.rmtree(local_directory + "/tmp")   

    