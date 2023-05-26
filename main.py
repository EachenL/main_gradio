import gradio as gr
import numpy as np
def greet(name, is_morning, temperature):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

# demo = gr.Interface(fn=greet, inputs=["text", "checkbox", gr.Slider(0,100)], outputs=["text", "number"])
demo = gr.Interface(fn=sepia, inputs=gr.Image(type="filepath"), outputs="image")

demo.launch() # server_name="0.0.0.0" share=True