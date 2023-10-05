This method uses the fast tortoise generation.
https://github.com/152334H/tortoise-tts-fast

In order to run you must clone and install tortoise as their github page says, 


git clone https://github.com/152334H/tortoise-tts-fast
cd tortoise-tts-fast
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
python3 -m pip install -e .
pip3 install git+https://github.com/152334H/BigVGAN.git

-Once thats done then you want to put these files into the tortoise-tts-fast folder you cloned from them

run the run_gui.py file and it should work fine

If you run into errors when running the gui, its probably a dependency issue or something like that
Every time I've run into that I just copy and paste the code from the run_gui.py file into chatgpt
And then give chatgpt the error code you got
Itll give you solutions, usually install dependency commands, and you just keep on doing that and eventually itll just work!

If not report an issue on the VoxNovel Github and I'll try my best to respond.


**Tortoise generate audio gui**

![image](https://github.com/DrewThomasson/VoxNovel/assets/126999465/8585818d-d0b0-4012-9fea-458929ffc5cb)
