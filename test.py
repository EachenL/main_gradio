import gradio as gr
def button_click():
    text1 = gr.Textbox(lines=5, label="Text 1")
    img1 = gr.Image(shape=(224, 224), label="Image 1")
    text2 = gr.Textbox(lines=5, label="Text 2")
    return [text1, img1, text2]

with gr.Blocks() as app:
    button = gr.Button("Click me!")
    box = gr.Box()
    button.click(button_click, None, box)
    
app.launch()