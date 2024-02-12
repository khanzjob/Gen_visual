from langchain.document_loaders import ImageCaptionLoader
from langchain.indexes import VectorstoreIndexCreator
from PIL import Image
import requests

from genVisual.utils import capture_image

def get_image_captions(*image_urls):
    # Create the image caption loader
    loader = ImageCaptionLoader(path_images=list(image_urls))
    list_docs = loader.load()
    
    # Create the index
    index = VectorstoreIndexCreator().from_loaders([loader])
    
    # For the purpose of this function, I'm assuming you want to query 
    # "What kind of images are there?" and get the result
    query = "What kind of images are there?"
    return index.query(query)

# Example usage
path = capture_image()
captions = get_image_captions(*path)
print(captions)


my_list = [1, 2, 3, 4, 5]
del my_list[0:2]
print(my_list)