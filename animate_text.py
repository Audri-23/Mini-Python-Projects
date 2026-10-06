import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "manim"])

from manim import *

class TextWrite(Scene):
    def construct(self):
        text = Text(input("Enter text to animate: "), font_size=50, color=RED)

        self.play(Write(text), run_time=2)
        self.wait(1)

if __name__ == "__main__":
    subprocess.check_call([
        sys.executable,
        "-m",
        "manim",
        "-pqh",             
        __file__,           
        "TextWrite"
    ])