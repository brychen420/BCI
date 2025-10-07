# Real-time-Brainwave-Car-Controller

## working environment

1. computer with windows OS(cygnus can only be run on windows OS)

2. [cygnus](https://drive.google.com/file/d/1sH7X4EFP8hUWEHtPcJr0E_8npi1PI3sR/view)


3. [Python3 - Anaconda](https://www.anaconda.com/products/distribution)
```powershell
# >>> conda initialize >>>
(& "YOUR_PATH\anaconda3\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
# <<< conda initialize <<<

conda create --name ENV_NAME python=3.7
conda activate ENV_NAME
```

4. [openvibe](http://openvibe.inria.fr/downloads/)
  
5. python Library installation
```bash
pip install -r requirements.txt
```
   
6. file description
 - alpha_wave_bandpower.xml: code for openvibe
 - mind_controlled_car.py: collect data from openvibe and send commend to car
 - test_car.py: just for testing, you can use key board to test your car functionality
