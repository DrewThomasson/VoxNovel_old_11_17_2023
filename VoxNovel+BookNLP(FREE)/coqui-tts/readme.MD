**SetUp install**
run in this order:

conda create --name VoxNovel python=3.10
conda activate VoxNovel
git clone https://github.com/DrewThomasson/VoxNovel.git
cd VoxNovel/
pip install tts
pip install booknlp
pip install -r requirements.txt

**To Run the program**
python gui_run.py

**To run the version here all you do is select the book and nothing else**

python auto_noGui_run.py

**folders**

Final_combined_output_audio:
-This is where all of your final audio files will be put in order of chapter num
