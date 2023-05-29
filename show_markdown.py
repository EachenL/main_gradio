import gradio as gr
import markdown
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os


class show_md():
    '''
    has bugs, can not show image
    '''
    def __init__(self):
        self.choosed_item = ''
        with gr.Box() as show_box:
            self.show_button = gr.Button(value="Show")
            self.show_box = []
            self.show_box.append(gr.Markdown())
            
    def show_button_click(self, choosed_item):
        
        context = open(choosed_item, 'r').read()
        html_context = markdown.markdown(context)
        soup = BeautifulSoup(html_context, 'html.parser')
        img_tags = soup.find_all('img')
        md_dir = os.path.dirname(choosed_item)
        for img in img_tags:
            img['src'] = "file://" + os.path.join(md_dir, img['src'])
        soup = str(soup)
        return soup