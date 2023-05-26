import gradio as gr
import os
import shutil
import subprocess

with gr.Blocks() as toolbox:
    gr.Markdown("# Toolbox")
    gr.Markdown("## Generate Book by a Part List json file")
    gr.Markdown("### Generate Part List json file by ChatGPT")
    gr.Markdown("### Generate Part List json file by other LLMs")
    gr.Markdown("## EPR reader")
    gr.Markdown("## ")