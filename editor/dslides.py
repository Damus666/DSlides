"""Simple language to create a presentation. Use the produce() method."""
from .converter import Converter

def produce(filename:str,outputfolder:str="output")->bool:
    "Parses the file written in ds language, creates the elements, \
renders them and saves them to a folder as a list of png images for each slide."
    print("### Welcome to DSlides! ###")
    content = ""
    with open(filename,"r",encoding="UTF-8") as myfile:
        content = myfile.read()
    converter = Converter(content,outputfolder)
    print(f"=== Starting to parse {filename} ===")
    converter.convert()
    print("=== Parsing finished, rendering the elements ===")
    converter.renderer.render()
    converter.renderer.save()
    print("### Your presentation has been rendered and saved ###")
    return True
