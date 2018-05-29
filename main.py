from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import psutil

class MyWidget(BoxLayout):



    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.drives_list.adapter.bind(on_selection_change=self.drive_selection_changed)

    def get_sys_drives(self):
        drives = []
        getDrives = psutil.disk_partitions()
        for i in range(len(getDrives)):
            drives.append(getDrives[i][1])
        return drives


    def drive_selection_changed(self, *args):
        selected_item = args[0].selection[0].text
        self.file_chooser.path = selected_item

    def copy_file(self,path):
        pass


    def paste_file(self):
        pass

    def delete_file(self):
        pass


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()
