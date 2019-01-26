import os
 
path = '../data/'
for filename in os.listdir(path):
    filename_without_ext = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    if extension == '.jpg':
      new_file_name = 'frame-' + filename_without_ext[5:len(filename_without_ext) - 1]
      new_file_name_with_ext = new_file_name+extension
      print(new_file_name_with_ext)
      os.rename(os.path.join(path,filename),os.path.join(path,new_file_name_with_ext))