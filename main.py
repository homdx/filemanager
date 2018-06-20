from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import os
from os.path import basename, isfile
import shutil
import psutil
import zlib






class MyWidget(BoxLayout):

    path_way = ObjectProperty(None)




    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.drives_list.adapter.bind(on_selection_change=self.drive_selection_changed)  #Display contents of selected  Drive

    def get_sys_drives(self):                                           #Get a list of Drives Locations that are currently mounted
        drives = []
        getDrives = psutil.disk_partitions()
        for i in range(len(getDrives)):
            drives.append(getDrives[i][1])
        return drives


    def drive_selection_changed(self, *args):                           #Setting fileSytem path based on Drive selected to view contents
        selected_item = args[0].selection[0].text
        self.file_chooser.path = selected_item

    def get_selected_file(self, path, filename):
        stream = os.path.join(path, filename[0])                         # get file selected
        print(stream)
        return stream

    def get_selected_directory (self,path):
        selected_directory = path
        return selected_directory


    def copy_file(self, path, filename):
        selected_file = self.get_selected_file(path, filename)
        return selected_file




    def paste_file(self, path, filename):
        source = self.copy_file(path, filename)
        destination = self.get_selected_directory(path)
        shutil.copy2(source, destination)
        print("Done Copying!!")



        pass

    def delete_file(self, path, filename):                               #deleting file
        sfile = self.get_selected_file(path, filename)
        print(sfile)
        os.remove(sfile)                                                 #it finally works #delete the matching  item
        print('Deletion Complete!!!!')

    def compress_file(self, path, filename):                             #Fuction for file compression using zlib module
        cfile = self.get_selected_file(path, filename)                   #call the get_selected_file methode
        f_Name, f_Extension = os.path.splitext(cfile)
        normal_File = open(cfile, 'rb').read()
        comp_File = open(f_Name + '(compressed)' + f_Extension, 'wb')
        comp_File.write(zlib.compress(normal_File,9))
        comp_File.close()
        print("Compression Complete!!!")

    def decompress_file(self, path, filename):                            #Fuction for file Decompression using zlib module
        cfile = self.get_selected_file(path, filename)                    #call the get_selected_file methode
        f_Extension = os.path.splitext(cfile)[1]
        f_Name = cfile.split('(')[0]
        comp_File = open(cfile, 'rb').read()
        decomp_File = open(f_Name + f_Extension, 'wb')
        decomp_File.write(zlib.decompress(comp_File))
        decomp_File.close()
        print("decompression Complete!!!")



class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()
