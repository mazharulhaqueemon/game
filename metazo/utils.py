import os
import shutil
import subprocess
#For Image Compression
from io import BytesIO
from PIL import Image
from django.core.files import File

""" Deletes file from filesystem. """
def delete_file(path):
   if os.path.isfile(path):
      os.remove(path) 
   elif os.path.isdir(path):
      shutil.rmtree(path)

def delete_video_files_or_directories(instance):
    if instance.video:
        instance.video.delete(False)
    if instance.hls_path:
        subprocess.call(['chmod', '-R', '+w', instance.hls_path])
        delete_file(instance.hls_path)
    if instance.hls_keys_path:
        subprocess.call(['chmod', '-R', '+w', instance.hls_keys_path])
        delete_file(instance.hls_keys_path)

#image compression method
def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    ext = image.name.split('.')[-1]
    # if im.mode in ("RGBA", "P"):
    #     im = im.convert("RGB")
    if ext == 'png':
        #Convert mode RGBA as JPEG
        # rgb_im = im.convert('RGB')
        # rgb_im.save(im_io, 'JPEG', quality=60) 
        im.save(im_io, 'PNG', quality=60) 
    else:
        im.save(im_io, 'JPEG', quality=60) 
   
    new_image = File(im_io, name=image.name)
    return new_image
