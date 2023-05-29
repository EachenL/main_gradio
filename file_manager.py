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
    def __init__(self, text):
        '''
        
        '''  
        self.file_list = filelist()
        # with gr.Blocks() as self.file_manager: # use it as a block
        with gr.Box() as self.file_manager:  # if use this as a component
            gr.Markdown(f"{text}")
            with gr.Row():
                visible_button = gr.Button(value="Select file or folder")
                self.choosed_item = gr.Textbox(label="Choosed item")
            def change_visible():
                    file_box.visible = not file_box.visible
                    return gr.update(visible=file_box.visible)
            
            # under this is the File Manager module code
            with gr.Box(visible=False) as file_box:
                # file manager status bar
                with gr.Row() as status_bar:
                    with gr.Column(scale=4) as address_bar:
                        curdir = gr.Textbox(label="current path, you can edit it to your wanted path then click forward button",
                                            value=self.file_list.cur_path,
                                            interactive=True,
                                            visible=True)
                    with gr.Column(scale=1) as operation_bar:
                        refresh_button = gr.Button(value="Refresh")
                        back_button = gr.Button(value="Back")
                # file window        
                dataframe = gr.Dataframe(col_count=1, type="array", value=self.file_list.get_cur_path_items())
                # binding functions
                def update_list(curdir):
                    '''
                    binding refresh button, refresh the file manager
                    '''
                    self.file_list.cur_path = curdir
                    return self.file_list.get_cur_path_items(), self.file_list.cur_path
                
                def back_list():
                    '''
                    back to lower level menu
                    '''
                    self.file_list.cur_path = os.path.dirname(self.file_list.cur_path)
                    return self.file_list.get_cur_path_items(), self.file_list.cur_path
                
                def choose_dir(choose_item: gr.SelectData):
                    curpath = os.path.join(self.file_list.cur_path, choose_item.value)
                    if os.path.isdir(curpath):
                        self.file_list.choose_file = ''
                        self.file_list.choose_dir = curpath
                        self.file_list.cur_path = curpath
                        return self.file_list.get_cur_path_items(), self.file_list.cur_path, self.file_list.choose_dir
                    else:
                        self.file_list.choose_dir = ''
                        self.file_list.choose_file = curpath
                        return self.file_list.get_cur_path_items(), self.file_list.cur_path, self.file_list.choose_file
                
                # event functions
                refresh_button.click(update_list, curdir, [dataframe, curdir])
                back_button.click(back_list, None, [dataframe, curdir])
                dataframe.select(choose_dir, None, [dataframe, curdir, self.choosed_item])
                visible_button.click(change_visible, None, file_box)

# with gr.Blocks() as files:
#     file_manager = filemanager()
# files.launch()

