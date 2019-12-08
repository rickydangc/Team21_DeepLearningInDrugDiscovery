#!/bin/bash

export PATH=/usr/bin/anaconda/bin:$PATH;
sudo rm -rf /usr/bin/anaconda/lib/python2.7/site-packages/conda/core/subdir*;
sudo wget https://gregorysfixes.blob.core.windows.net/public/subdir_data.py -P /usr/bin/anaconda/lib/python2.7/site-packages/conda/core/;
conda init bash;
source ~/.bashrc;
conda update -y --all;
conda install -y -c anaconda numpy
conda install -y -c anaconda scipy
conda install -y -c pytorch pytorch;
conda install -y -c rdkit rdkit;
echo 'export PATH=/usr/bin/anaconda/bin:$PATH' > ~/.bash_profile

su - jing -c "
echo 'export PATH=/usr/bin/anaconda/bin:$PATH' > ~/.bash_profile
"