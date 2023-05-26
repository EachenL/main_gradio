import numpy as np
import gradio as gr
import os

class filelist():
    
    def __init__(self):
        self.cur_items = []
        self.cur_path = os.path.expanduser('~') # get home directory
        self.choose_dir = ''
        self.choose_file = ''
        
        self.checkbox_items = []
        
    def get_cur_path_items(self):
        self.cur_items = os.listdir(self.cur_path)
        cur_items = []
        for item in self.cur_items:
            if os.path.isdir(os.path.join(self.cur_path, item)):
                item = item + '/'
                # if encode occur error, use 'replace' to replace the error
                # please use convmv tool to convert the encoding of the file
                item = item.encode('utf-8', 'replace').decode()
                cur_items.append([item])
            else:
                item = item.encode('utf-8', 'replace').decode()
                cur_items.append([item])
        self.cur_items = sorted(cur_items, key=lambda x: x[0])
        return self.cur_items

class filemanager():   
    def __init__(self):     
        file_list = filelist()
        checkbox_list = []
        with gr.Blocks() as file_manager:
            gr.Markdown("# File Manager")
            # under this is the File Manager module code
            with gr.Box():
                with gr.Row():
                    with gr.Column(scale=4):
                        curdir = gr.Textbox(label="current path, you can edit it to your wanted path then click forward button",
                                            value=file_list.cur_path,
                                            interactive=True)
                    with gr.Column(scale=1):
                        forward_button = gr.Button(value="Forward")
                        back_button = gr.Button(value="Back")
                dataframe = gr.Dataframe(col_count=1, type="array", value=file_list.get_cur_path_items())

                def update_list(curdir):
                    file_list.cur_path = curdir
                    return file_list.get_cur_path_items(), file_list.cur_path
                def back_list():
                    file_list.cur_path = os.path.dirname(file_list.cur_path)
                    return file_list.get_cur_path_items(), file_list.cur_path
                forward_button.click(update_list, curdir, [dataframe, curdir])
                back_button.click(back_list, None, [dataframe, curdir])
                def choose_dir(choose_item: gr.SelectData):
                    curpath = os.path.join(file_list.cur_path, choose_item.value)
                    if os.path.isdir(curpath):
                        file_list.choose_file = ''
                        file_list.choose_dir = curpath
                        file_list.cur_path = curpath
                        return file_list.get_cur_path_items(), file_list.cur_path
                    else:
                        file_list.choose_dir = ''
                        file_list.choose_file = curpath
                        return file_list.get_cur_path_items(), file_list.cur_path
                dataframe.select(choose_dir, None, [dataframe, curdir])

        file_manager.launch()


file_manager = filemanager()


