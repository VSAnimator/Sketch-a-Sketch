# GuideLines: Controllable diffusion-based image generation with just a few strokes

**[Demo](https://colab.research.google.com/drive/1Biw7s0BD_NtV3wC2lIjVaeg6qXj0KOTv?usp=sharing) | [Blog](vsanimator.github.io/guidelines)**

| **Input Sketch** | **Generated Image** | **Guiding Sketch**
|:--:| :--: | :--: |
| ![](GuideLines/castle_s.gif) | ![](GuideLines/castle_o1.gif) | ![](GuideLines/castle_p.gif) |

It’s really fun playing with generative AI tools, but its incredibly hard to engineer text prompts that get them to create the image you want. You’ve probably seen sketch-to-image tools that aim to make it "easier" to control generative AI, but to get a good image, you typically need to start with a fairly complete sketch. Since most of us aren’t great sketchers, that’s prevented most of us from using sketch to image. 

*GuideLines* makes it much easier to control the output of generative AI from sketches, because it works using simple sketches that only have a few strokes -- sketches that most of us can draw.
To give you an idea of how it works, think about the game of Pictionary, where your teammates must guess the object you are trying to draw as quickly as possible. If you’re good at the game, your teammates will guess what you’re trying to depict after just a few strokes (a partial sketch). If your team can’t guess what you’re trying to draw, you just keep sketching to add detail in order to make the concept more clear.

With *GuideLines*, controlling generative AI is lot like playing Pictionary: just sketch a few strokes, and the AI will guess what you are trying to draw and give you suggestions for high-quality final images.
If the AI isn’t giving you the images you want, don’t worry. Just draw a few more strokes to make your desired image more clear, and repeat until the AI creates the images you hoped for.
Even better, *GuideLines* will help you create "winning" sketches. As you sketch, the *GuideLines* system will show you a "guiding sketch" with possibilities for future lines that will be most helpful in helping the AI guess what final image you want.

Check out our [blog](vsanimator.github.io/guidelines), try out our [demo](https://colab.research.google.com/drive/1Biw7s0BD_NtV3wC2lIjVaeg6qXj0KOTv?usp=sharing) to make your own sketches, or run the Gradio app locally by cloning this repo, installing requirements from requirements.txt, and running demo.py.
