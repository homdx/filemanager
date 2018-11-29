from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import os
import shutil
import psutil
import stat
import zipfile



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

    def get_selected_directory (self, path):
        selected_directory = path
        return selected_directory

    def copy_file(self, path, filename):
        selected_file = self.get_selected_file(path, filename)
        return selected_file



    def paste_file(self, path, filename, symlinks=False, ignore=None):
        source = self.copy_file(path, filename)
        destination = self.get_selected_directory(path)
        print(destination)

        if os.path.isdir(source):

            print("Yes a Directory was passed!!!")

            def copytreex(srce, dst, symlinks=False, ignore=None):

                if not os.path.exists(dst):
                    os.makedirs(dst)
                    shutil.copystat(srce, dst)
                lst = os.listdir(srce)
                if ignore:
                    excl = ignore(srce, lst)
                    lst = [x for x in lst if x not in excl]
                for item in lst:

                    s = os.path.join(srce, item)
                    d = os.path.join(dst, item)
                    if symlinks and os.path.islink(s):
                        if os.path.lexists(d):
                            os.remove(d)
                        os.symlink(os.readlink(s), d)
                        try:
                            st = os.lstat(s)
                            mode = stat.S_IMODE(st.st_mode)
                            os.lchmod(d, mode)
                        except:
                            pass  # lchmod not available
                    elif os.path.isdir(s):
                        copytreex(s, d, symlinks, ignore)
                    else:
                        shutil.copy2(s, d)

                        print("Operation complete")

                copytreex(source,destination)
                self.finish_popup("Copy Operation")

            '''shutil.copytree(source, destination, symlinks, ignore)
            self.finish_popup("Copy Operation")
            print("Folder Copied!!")'''

        else:
            StartTime = time.time()
            shutil.copy2(source, destination)

            self.finish_popup("Copy Operation")
            StopTime = time.time()
            TimeElapsed = StopTime - StartTime
            print("File Copied!!")
            print(TimeElapsed)





    def delete_file(self, path, filename):                               #deleting file
        sfile = self.get_selected_file(path, filename)
        print(sfile)
        if os.path.isdir(sfile):
            shutil.rmtree(sfile)                                                 #it finally works #delete the matching  item
            self.finish_popup("Deletion Operation")

            print('Folder Deleted!!')
        else:
            os.remove(sfile)
            self.finish_popup("Deletion Operation")

            print("File Deleted!!")

    def compress_file(self, path, filename):                             #Fuction for file compression using zlib module
        folder_name = filename
        folder_path = path
        cfile = self.get_selected_file(path, filename)                   #call the get_selected_file methode

        if os.path.isdir(cfile):
            f_Name = cfile.split('/')
            new_file = folder_path+ '/' + f_Name[-1] + ".zip"
            new_zip = zipfile.ZipFile(new_file, 'a')
            lst = os.listdir(cfile)


            for item in lst:

                s = os.path.join(cfile, item)
                new_zip.write(s, compress_type=zipfile.ZIP_DEFLATED)

            new_zip.close()
            self.finish_popup("Compression Operation")
            print("Done")


        else:
            scrap = cfile.split('/')[-1]
            f_Name =scrap.split(".")[0]
            new_file = folder_path + '/' + f_Name + ".zip"
            new_zip = zipfile.ZipFile(new_file, 'w')
            new_zip.write(cfile, compress_type=zipfile.ZIP_DEFLATED)
            new_zip.close()
            self.finish_popup("Compression Operation")

    def decompress_file(self, path, filename):                            #Fuction for file Decompression using zlib module
        folder_path = path
        cfile = self.get_selected_file(path, filename)                    #call the get_selected_file methode

        scrap = cfile.split(".")[0]
        new_file_name = scrap.split("/")[-1]
        current_directory = folder_path + "/" + new_file_name

        print(cfile)
        print(folder_path)
        print(new_file_name)
        print(current_directory)

        decompZip = zipfile.ZipFile(cfile)

        decompZip.extractall(current_directory)
        decompZip.close()
        self.finish_popup("Decompression Operation")

class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()
