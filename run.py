import gradio as gr
import os
import shutil
import subprocess
from file_manager import filemanager
import sys
sys.path.append('..')
from Generate_book import extract_image_by_srt
from EPRReaderPY.src.epr_reader import read_epr # for development mode only
# from epr_reader import read_epr # for install mode
import time
from ChatGLM.web_demo_module import chat_module
from show_markdown import show_md
def readepr(epr_file, read_header_only):
    eprreader = read_epr()
    # time.sleep(5) # eprreader has problem, this is a bug to fix
    json_file = eprreader.read(epr_file, read_header_only)
    return json_file

with gr.Blocks() as toolbox:
    gr.Markdown("# Toolbox")
    gr.Markdown("## Generate Book by a Part List json file")
    with gr.Accordion(label="Generate Book by a Part List json file", open=False):
        fm = filemanager("Please choose the record folder")
        proj_name = gr.Textbox(label="your project name")
        with gr.Row():
            genbook_button = gr.Button(value="Generate book by part list")
            genpartlist_button = gr.Button(value="Generate part list by ChatGPT")
        genbook_button.click(extract_image_by_srt.gen_book, [fm.choosed_item, proj_name])
    gr.Markdown("### Generate Part List json file by ChatGPT")
    gr.Markdown("### Generate Part List json file by other LLMs")
    gr.Markdown("## EPR reader")
    with gr.Accordion(label="EPR reader", open=False):
        epr_fs = filemanager("Please choose the epr file")
        read_header_only_switch = gr.Checkbox(label="read head", value=True)
        read_epr_button = gr.Button(value="start read")
        epr_json = gr.JSON()
        read_epr_button.click(readepr, [epr_fs.choosed_item, read_header_only_switch], epr_json)
    gr.Markdown("## LLM delete junk word in srt file")
    gr.Markdown("## ChatGLM-6B")
    with gr.Accordion(label="ChatGLM-6B", open=False):
        chatbot = chat_module()
    gr.Markdown("## VisualGLM-6B")
    gr.Markdown("## Show MarkDown file")
    with gr.Accordion(label="Show MarkDown file", open=False):
        md_fs = filemanager("Please choose the markdown file")
        md_helper = show_md()
        md_helper.show_button.click(md_helper.show_button_click, md_fs.choosed_item, md_helper.html_box)
toolbox.queue().launch()