import gradio as gr
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, EulerAncestralDiscreteScheduler
import torch
from diffusers.utils import load_image
import numpy as np
from controlnet_aux import HEDdetector
from PIL import Image

negative_prompt = ""
device = torch.device('cuda')
controlnet = ControlNetModel.from_pretrained("vsanimator/sketch-a-sketch", torch_dtype=torch.float16).to(device)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", 
    controlnet=controlnet, torch_dtype=torch.float16
).to(device)
pipe.safety_checker = None
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
threshold = 250
hed = HEDdetector.from_pretrained('lllyasviel/Annotators') # ControlNet

num_images = 3

with gr.Blocks() as demo:
    start_state = []
    for k in range(num_images):
        start_state.append([None, None])
    sketch_states = gr.State(start_state)
    checkbox_state = gr.State(False)
    with gr.Row():
        with gr.Column(scale = 1):
            with gr.Tabs(shape=(768, 768),min_width=512):
                with gr.TabItem("Draw", shape=(512, 512),min_width=512):
                    i = gr.Image(source="canvas", shape=(512, 512), tool="color-sketch",
                                min_width=512, brush_radius = 2).style(width=600, height=600)
                with gr.TabItem("ShadowDraw", shape=(512, 512),min_width=512):
                    i_sketch = gr.Image(shape=(512, 512),min_width=512).style(width=600, height=600)
            prompt_box = gr.Textbox(label="Prompt")
            with gr.Row():
                btn = gr.Button("Render").style(width=100, height=80)
                checkbox = gr.Checkbox(label = "ShadowDraw", value=False)
                btn2 = gr.Button("Reset").style(width=100, height=80)
            i_prev = gr.Image(shape=(512, 512),
                              min_width=512).style(width=768, height=768)
        with gr.Column(scale = 1):
            o_list = [gr.Image().style(width=512, height=512) for _ in range(num_images)]
    
    def sketch(curr_sketch, prev_sketch, prompt, negative_prompt, seed, num_steps):
        print("Sketching")
        if curr_sketch is None:
            return None, None
        if prev_sketch is None:
            prev_sketch = curr_sketch
        generator = torch.Generator(device=device)
        generator.manual_seed(seed)
        curr_sketch_image = Image.fromarray(curr_sketch.astype(np.uint8)).convert("L")

        # Run function call
        images = pipe(prompt, curr_sketch_image.convert("RGB").point( lambda p: 256 if p > 128 else 0), negative_prompt = negative_prompt, num_inference_steps=num_steps, generator=generator, controlnet_conditioning_scale = 1.0).images
        
        return images[0]

    def run_sketching(prompt, curr_sketch, prev_sketch, sketch_states, shadow_draw):
        to_return = []
        for k in range(num_images):
            seed = sketch_states[k][1]
            if seed is None:
                seed = np.random.randint(1000)
                sketch_states[k][1] = seed
            new_image = sketch(curr_sketch, prev_sketch, prompt, 
                                            negative_prompt, seed = seed, num_steps = 20)
            to_return.append(new_image)
        prev_sketch = curr_sketch
        if shadow_draw:
            hed_images = []
            for image in to_return:
                hed_images.append(hed(image, scribble=False))
            avg_hed = np.mean([np.array(image) for image in hed_images], axis = 0)
            curr_sketch = np.array(curr_sketch).astype(float) / 255.
            curr_sketch = Image.fromarray(np.uint8(1.0*((0.0*curr_sketch + 1. - 1.*(avg_hed / 255.))) * 255.))
        else:
            curr_sketch = None
        return to_return + [curr_sketch, prev_sketch, sketch_states]
    
    def reset(sketch_states):
        for k in range(num_images):
            sketch_states[k] = [None, None]
        return None, None, sketch_states

    btn.click(run_sketching, [prompt_box, i, i_prev, sketch_states, checkbox_state], o_list + [i_sketch, i_prev, sketch_states])
    btn2.click(reset, sketch_states, [i, i_prev, sketch_states])
    checkbox.change(lambda i: i, inputs=[checkbox], outputs=[checkbox_state])

demo.launch(share = True)

