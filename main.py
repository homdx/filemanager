from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import os
import shutil
import psutil
import zlib



class PopUps(BoxLayout):
    cancel = ObjectProperty(None)



class MyWidget(BoxLayout):



    def dismiss_popup(self):
        self._popup.dismiss()

    def finish_popup(self, operation_type):
        content = PopUps(cancel=self.dismiss_popup)
        self._popup = Popup(title=operation_type, content=content, size_hint=(0.3, 0.3))
        self._popup.open()




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




    def paste_file(self, path, filename, symlinks=False, ignore=None):
        source = self.copy_file(path, filename)
        destination = self.get_selected_directory(path)

        if os.path.isdir(source):
            shutil.copytree(source, destination, symlinks, ignore)
            self.finish_popup("Copy Operation")
            print("Folder Copied!!")
        else:
            shutil.copy2(source, destination)
            self.finish_popup("Copy Operation")
            print("File Copied!!")





    def delete_file(self, path, filename):                               #deleting file
        sfile = self.get_selected_file(path, filename)
        print(sfile)
        if os.path.isdir(sfile):
            shutil.rmtree(sfile)                                                 
            self.finish_popup("Deletion Operation")

            print('Folder Deleted!!')
        else:
            os.remove(sfile)
            self.finish_popup("Deletion Operation")

            print("File Deleted!!")

    def compress_file(self, path, filename):                             #Fuction for file compression using zlib module
        cfile = self.get_selected_file(path, filename)                   #call the get_selected_file methode
        f_Name, f_Extension = os.path.splitext(cfile)
        normal_File = open(cfile, 'rb').read()
        comp_File = open(f_Name + '(compressed)' + f_Extension, 'wb')
        comp_File.write(zlib.compress(normal_File,9))
        comp_File.close()
        self.finish_popup("Compression Operation")
        print("Compression Complete!!!")

    def decompress_file(self, path, filename):                            #Fuction for file Decompression using zlib module
        cfile = self.get_selected_file(path, filename)                    #call the get_selected_file methode
        f_Extension = os.path.splitext(cfile)[1]
        f_Name = cfile.split('(')[0]
        comp_File = open(cfile, 'rb').read()
        decomp_File = open(f_Name + f_Extension, 'wb')
        decomp_File.write(zlib.decompress(comp_File))
        decomp_File.close()
        self.finish_popup("Decompression Operation")
        print("decompression Complete!!!")


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()
