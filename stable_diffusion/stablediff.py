###################################################import#########################################################
import tkinter as tk
import customtkinter as ctk 
from PIL import ImageTk
from authtoken import authtoken
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline 
############################################GUI Component ######################################################
app = tk.Tk()
app.geometry("532x632")
app.title("Stable Bud") 
ctk.set_appearance_mode("dark") 
prompt = ctk.CTkEntry(master=app,height=40, width=512, text_color="black", fg_color="white") 
prompt.place(x=10, y=10)
lmain = ctk.CTkLabel(master=app,height=512, width=512)
lmain.place(x=10, y=110)
################################################model#############################################################
modelid = "CompVis/stable-diffusion-v1-4"
device = "cuda:0" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(modelid, revision="fp16", torch_dtype=torch.float32, use_auth_token=authtoken) 
pipe.to(device) 
def generate(): 
    with autocast(device): 
        image = pipe(prompt.get(), guidance_scale=8.5)["sample"][0]
    
    image.save('generatedimage.png')
    img = ImageTk.PhotoImage(image)
    lmain.configure(image=img) 

trigger = ctk.CTkButton(master=app,height=40, width=120, text_color="white", fg_color="blue", command=generate) 
trigger.configure(text="Generate") 
trigger.place(x=206, y=60) 
app.mainloop()