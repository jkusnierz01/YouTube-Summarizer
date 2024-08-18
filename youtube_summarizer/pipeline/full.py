from .download import download
import tempfile

def pipeline(url:str):
    with tempfile.TemporaryFile as fp:
        fp.write(download(url))
        
        
    
