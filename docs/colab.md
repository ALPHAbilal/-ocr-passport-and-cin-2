--2026-02-25 19:35:25--  https://repo.anaconda.com/miniconda/Miniconda3-py310_23.5.2-0-Linux-x86_64.sh
Resolving repo.anaconda.com (repo.anaconda.com)... 104.16.191.158, 104.16.32.241, 2606:4700::6810:bf9e, ...
Connecting to repo.anaconda.com (repo.anaconda.com)|104.16.191.158|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 95826076 (91M) [application/x-sh]
Saving to: ‘Miniconda3-py310_23.5.2-0-Linux-x86_64.sh’

Miniconda3-py310_23 100%[===================>]  91.39M  97.0MB/s    in 0.9s    

2026-02-25 19:35:26 (97.0 MB/s) - ‘Miniconda3-py310_23.5.2-0-Linux-x86_64.sh’ saved [95826076/95826076]

PREFIX=/usr/local
Unpacking payload ...

Installing base environment...


Downloading and Extracting Packages


Downloading and Extracting Packages

Preparing transaction: done
Executing transaction: done
installation finished.
WARNING:
    You currently have a PYTHONPATH environment variable set. This may cause
    unexpected behavior when running the Python interpreter in Miniconda3.
    For best results, please verify that your PYTHONPATH only points to
    directories of packages that are compatible with the Python interpreter
    in Miniconda3: /usr/local
Collecting package metadata (current_repodata.json): done
Solving environment: done


==> WARNING: A newer version of conda exists. <==
  current version: 23.5.2
  latest version: 26.1.1

Please update conda by running

    $ conda update -n base -c defaults conda

Or to minimize the number of packages updated during conda update use

     conda install conda=26.1.1



## Package Plan ##

  environment location: /usr/local

  added / updated specs:
    - python=3.10


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    ca-certificates-2025.12.2  |       h06a4308_0         125 KB
    certifi-2026.01.04         |  py310h06a4308_0         148 KB
    openssl-3.0.18             |       hd6dcaed_0         4.5 MB
    ------------------------------------------------------------
                                           Total:         4.8 MB

The following packages will be UPDATED:

  ca-certificates                     2023.05.30-h06a4308_0 --> 2025.12.2-h06a4308_0 
  certifi                          2023.5.7-py310h06a4308_0 --> 2026.01.04-py310h06a4308_0 
  openssl                                  3.0.9-h7f8727e_0 --> 3.0.18-hd6dcaed_0 



Downloading and Extracting Packages
certifi-2026.01.04   | 148 KB    | :   0% 0/1 [00:00<?, ?it/s]
ca-certificates-2025 | 125 KB    | :   0% 0/1 [00:00<?, ?it/s]

openssl-3.0.18       | 4.5 MB    | :   0% 0/1 [00:00<?, ?it/s]
certifi-2026.01.04   | 148 KB    | :  11% 0.1083339945515618/1 [00:00<00:02,  2.60s/it]

openssl-3.0.18       | 4.5 MB    | :   0% 0.003483453807029756/1 [00:00<01:21, 81.31s/it]
certifi-2026.01.04   | 148 KB    | : 100% 1.0/1 [00:00<00:00,  2.60s/it]               

openssl-3.0.18       | 4.5 MB    | : 100% 1.0/1 [00:00<00:00,  2.19it/s]                 

                                                                        
                                                                        

                                                                        
Preparing transaction: done
Verifying transaction: done
Executing transaction: done


____________________

WARNING: Skipping paddlepaddle as it is not installed.
WARNING: Skipping paddleocr as it is not installed.
WARNING: Skipping paddlex as it is not installed.

----------------------------------
Collecting paddlepaddle==2.6.2
  Downloading paddlepaddle-2.6.2-cp310-cp310-manylinux1_x86_64.whl (126.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 126.0/126.0 MB 5.2 MB/s eta 0:00:00
Collecting paddleocr==2.7.0
  Downloading paddleocr-2.7.0.0-py3-none-any.whl (74.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 74.1/74.1 MB 7.0 MB/s eta 0:00:00
Collecting httpx (from paddlepaddle==2.6.2)
  Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 73.5/73.5 kB 7.8 MB/s eta 0:00:00
Collecting numpy>=1.13 (from paddlepaddle==2.6.2)
  Downloading numpy-2.2.6-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.8/16.8 MB 69.7 MB/s eta 0:00:00
Collecting Pillow (from paddlepaddle==2.6.2)
  Downloading pillow-12.1.1-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (7.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.0/7.0 MB 79.6 MB/s eta 0:00:00
Collecting decorator (from paddlepaddle==2.6.2)
  Downloading decorator-5.2.1-py3-none-any.whl (9.2 kB)
Collecting astor (from paddlepaddle==2.6.2)
  Downloading astor-0.8.1-py2.py3-none-any.whl (27 kB)
Collecting opt-einsum==3.3.0 (from paddlepaddle==2.6.2)
  Downloading opt_einsum-3.3.0-py3-none-any.whl (65 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65.5/65.5 kB 7.7 MB/s eta 0:00:00
Collecting protobuf>=3.20.2 (from paddlepaddle==2.6.2)
  Downloading protobuf-6.33.5-cp39-abi3-manylinux2014_x86_64.whl (323 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 323.5/323.5 kB 32.0 MB/s eta 0:00:00
Collecting shapely (from paddleocr==2.7.0)
  Downloading shapely-2.1.2-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (3.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.1/3.1 MB 40.2 MB/s eta 0:00:00
Collecting scikit-image (from paddleocr==2.7.0)
  Downloading scikit_image-0.25.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (14.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14.8/14.8 MB 27.2 MB/s eta 0:00:00
Collecting imgaug (from paddleocr==2.7.0)
  Downloading imgaug-0.4.0-py2.py3-none-any.whl (948 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 948.0/948.0 kB 43.3 MB/s eta 0:00:00
Collecting pyclipper (from paddleocr==2.7.0)
  Downloading pyclipper-1.4.0-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (970 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 971.0/971.0 kB 33.9 MB/s eta 0:00:00
Collecting lmdb (from paddleocr==2.7.0)
  Downloading lmdb-1.7.5-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (292 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 292.4/292.4 kB 23.9 MB/s eta 0:00:00
Requirement already satisfied: tqdm in /usr/local/lib/python3.10/site-packages (from paddleocr==2.7.0) (4.65.0)
Collecting visualdl (from paddleocr==2.7.0)
  Downloading visualdl-2.5.3-py3-none-any.whl (6.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.3/6.3 MB 24.1 MB/s eta 0:00:00
Collecting rapidfuzz (from paddleocr==2.7.0)
  Downloading rapidfuzz-3.14.3-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (3.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.2/3.2 MB 17.4 MB/s eta 0:00:00
Collecting opencv-python<=4.6.0.66 (from paddleocr==2.7.0)
  Downloading opencv_python-4.6.0.66-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (60.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.9/60.9 MB 7.5 MB/s eta 0:00:00
Collecting opencv-contrib-python<=4.6.0.66 (from paddleocr==2.7.0)
  Downloading opencv_contrib_python-4.6.0.66-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (67.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 67.1/67.1 MB 7.1 MB/s eta 0:00:00
Collecting cython (from paddleocr==2.7.0)
  Downloading cython-3.2.4-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (3.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.5/3.5 MB 95.4 MB/s eta 0:00:00
Collecting lxml (from paddleocr==2.7.0)
  Downloading lxml-6.0.2-cp310-cp310-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl (5.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.3/5.3 MB 99.0 MB/s eta 0:00:00
Collecting premailer (from paddleocr==2.7.0)
  Downloading premailer-3.10.0-py2.py3-none-any.whl (19 kB)
Collecting openpyxl (from paddleocr==2.7.0)
  Downloading openpyxl-3.1.5-py2.py3-none-any.whl (250 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 250.9/250.9 kB 25.2 MB/s eta 0:00:00
Collecting attrdict (from paddleocr==2.7.0)
  Downloading attrdict-2.0.1-py2.py3-none-any.whl (9.9 kB)
Collecting PyMuPDF<1.21.0 (from paddleocr==2.7.0)
  Downloading PyMuPDF-1.20.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (8.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.9/8.9 MB 78.8 MB/s eta 0:00:00
Collecting python-docx (from paddleocr==2.7.0)
  Downloading python_docx-1.2.0-py3-none-any.whl (252 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 253.0/253.0 kB 23.3 MB/s eta 0:00:00
Collecting beautifulsoup4 (from paddleocr==2.7.0)
  Downloading beautifulsoup4-4.14.3-py3-none-any.whl (107 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 107.7/107.7 kB 12.9 MB/s eta 0:00:00
Collecting fonttools>=4.24.0 (from paddleocr==2.7.0)
  Downloading fonttools-4.61.1-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.9/4.9 MB 68.0 MB/s eta 0:00:00
Collecting fire>=0.3.0 (from paddleocr==2.7.0)
  Downloading fire-0.7.1-py3-none-any.whl (115 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 115.9/115.9 kB 10.7 MB/s eta 0:00:00
Collecting pdf2docx (from paddleocr==2.7.0)
  Downloading pdf2docx-0.5.10-py3-none-any.whl (134 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.3/134.3 kB 9.4 MB/s eta 0:00:00
Collecting termcolor (from fire>=0.3.0->paddleocr==2.7.0)
  Downloading termcolor-3.3.0-py3-none-any.whl (7.7 kB)
Requirement already satisfied: six in /usr/local/lib/python3.10/site-packages (from attrdict->paddleocr==2.7.0) (1.16.0)
Collecting soupsieve>=1.6.1 (from beautifulsoup4->paddleocr==2.7.0)
  Downloading soupsieve-2.8.3-py3-none-any.whl (37 kB)
Collecting typing-extensions>=4.0.0 (from beautifulsoup4->paddleocr==2.7.0)
  Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.6/44.6 kB 4.9 MB/s eta 0:00:00
Collecting anyio (from httpx->paddlepaddle==2.6.2)
  Downloading anyio-4.12.1-py3-none-any.whl (113 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 113.6/113.6 kB 10.7 MB/s eta 0:00:00
Requirement already satisfied: certifi in /usr/local/lib/python3.10/site-packages (from httpx->paddlepaddle==2.6.2) (2026.1.4)
Collecting httpcore==1.* (from httpx->paddlepaddle==2.6.2)
  Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.8/78.8 kB 9.5 MB/s eta 0:00:00
Requirement already satisfied: idna in /usr/local/lib/python3.10/site-packages (from httpx->paddlepaddle==2.6.2) (3.4)
Collecting h11>=0.16 (from httpcore==1.*->httpx->paddlepaddle==2.6.2)
  Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Collecting scipy (from imgaug->paddleocr==2.7.0)
  Downloading scipy-1.15.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (37.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 37.7/37.7 MB 12.9 MB/s eta 0:00:00
Collecting matplotlib (from imgaug->paddleocr==2.7.0)
  Downloading matplotlib-3.10.8-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (8.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.7/8.7 MB 106.4 MB/s eta 0:00:00
Collecting imageio (from imgaug->paddleocr==2.7.0)
  Downloading imageio-2.37.2-py3-none-any.whl (317 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 317.6/317.6 kB 32.6 MB/s eta 0:00:00
Collecting networkx>=3.0 (from scikit-image->paddleocr==2.7.0)
  Downloading networkx-3.4.2-py3-none-any.whl (1.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 66.4 MB/s eta 0:00:00
Collecting tifffile>=2022.8.12 (from scikit-image->paddleocr==2.7.0)
  Downloading tifffile-2025.5.10-py3-none-any.whl (226 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 226.5/226.5 kB 26.8 MB/s eta 0:00:00
Requirement already satisfied: packaging>=21 in /usr/local/lib/python3.10/site-packages (from scikit-image->paddleocr==2.7.0) (23.0)
Collecting lazy-loader>=0.4 (from scikit-image->paddleocr==2.7.0)
  Downloading lazy_loader-0.4-py3-none-any.whl (12 kB)
Collecting et-xmlfile (from openpyxl->paddleocr==2.7.0)
  Downloading et_xmlfile-2.0.0-py3-none-any.whl (18 kB)
INFO: pip is looking at multiple versions of pdf2docx to determine which version is compatible with other requirements. This could take a while.
Collecting pdf2docx (from paddleocr==2.7.0)
  Downloading pdf2docx-0.5.9-py3-none-any.whl (133 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 133.8/133.8 kB 14.4 MB/s eta 0:00:00
  Downloading pdf2docx-0.5.8-py3-none-any.whl (132 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 132.0/132.0 kB 14.7 MB/s eta 0:00:00
Collecting opencv-python-headless>=4.5 (from pdf2docx->paddleocr==2.7.0)
  Downloading opencv_python_headless-4.13.0.92-cp37-abi3-manylinux_2_28_x86_64.whl (60.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.4/60.4 MB 7.5 MB/s eta 0:00:00
Collecting cssselect (from premailer->paddleocr==2.7.0)
  Downloading cssselect-1.4.0-py3-none-any.whl (18 kB)
Collecting cssutils (from premailer->paddleocr==2.7.0)
  Downloading cssutils-2.11.1-py3-none-any.whl (385 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 385.7/385.7 kB 27.0 MB/s eta 0:00:00
Requirement already satisfied: requests in /usr/local/lib/python3.10/site-packages (from premailer->paddleocr==2.7.0) (2.29.0)
Collecting cachetools (from premailer->paddleocr==2.7.0)
  Downloading cachetools-7.0.1-py3-none-any.whl (13 kB)
Collecting bce-python-sdk (from visualdl->paddleocr==2.7.0)
  Downloading bce_python_sdk-0.9.60-py3-none-any.whl (395 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 395.4/395.4 kB 36.1 MB/s eta 0:00:00
Collecting flask>=1.1.1 (from visualdl->paddleocr==2.7.0)
  Downloading flask-3.1.3-py3-none-any.whl (103 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 103.4/103.4 kB 12.1 MB/s eta 0:00:00
Collecting Flask-Babel>=3.0.0 (from visualdl->paddleocr==2.7.0)
  Downloading flask_babel-4.0.0-py3-none-any.whl (9.6 kB)
Collecting pandas (from visualdl->paddleocr==2.7.0)
  Downloading pandas-2.3.3-cp310-cp310-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (12.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.8/12.8 MB 68.1 MB/s eta 0:00:00
Collecting rarfile (from visualdl->paddleocr==2.7.0)
  Downloading rarfile-4.2-py3-none-any.whl (29 kB)
Collecting psutil (from visualdl->paddleocr==2.7.0)
  Downloading psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl (155 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 155.6/155.6 kB 13.4 MB/s eta 0:00:00
Collecting blinker>=1.9.0 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
Collecting click>=8.1.3 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading click-8.3.1-py3-none-any.whl (108 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 108.3/108.3 kB 12.1 MB/s eta 0:00:00
Collecting itsdangerous>=2.2.0 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Collecting jinja2>=3.1.2 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.9/134.9 kB 9.8 MB/s eta 0:00:00
Collecting markupsafe>=2.1.1 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading markupsafe-3.0.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (20 kB)
Collecting werkzeug>=3.1.0 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading werkzeug-3.1.6-py3-none-any.whl (225 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 225.2/225.2 kB 17.5 MB/s eta 0:00:00
Collecting Babel>=2.12 (from Flask-Babel>=3.0.0->visualdl->paddleocr==2.7.0)
  Downloading babel-2.18.0-py3-none-any.whl (10.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.2/10.2 MB 62.5 MB/s eta 0:00:00
Collecting pytz>=2022.7 (from Flask-Babel>=3.0.0->visualdl->paddleocr==2.7.0)
  Downloading pytz-2025.2-py2.py3-none-any.whl (509 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 509.2/509.2 kB 32.6 MB/s eta 0:00:00
Collecting exceptiongroup>=1.0.2 (from anyio->httpx->paddlepaddle==2.6.2)
  Downloading exceptiongroup-1.3.1-py3-none-any.whl (16 kB)
Collecting pycryptodome>=3.8.0 (from bce-python-sdk->visualdl->paddleocr==2.7.0)
  Downloading pycryptodome-3.23.0-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 35.3 MB/s eta 0:00:00
Collecting future>=0.6.0 (from bce-python-sdk->visualdl->paddleocr==2.7.0)
  Downloading future-1.0.0-py3-none-any.whl (491 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 491.3/491.3 kB 37.8 MB/s eta 0:00:00
Collecting more-itertools (from cssutils->premailer->paddleocr==2.7.0)
  Downloading more_itertools-10.8.0-py3-none-any.whl (69 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 69.7/69.7 kB 8.3 MB/s eta 0:00:00
Collecting contourpy>=1.0.1 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading contourpy-1.3.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (325 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 325.0/325.0 kB 26.1 MB/s eta 0:00:00
Collecting cycler>=0.10 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading cycler-0.12.1-py3-none-any.whl (8.3 kB)
Collecting kiwisolver>=1.3.1 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading kiwisolver-1.4.9-cp310-cp310-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (1.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 66.6 MB/s eta 0:00:00
Collecting pyparsing>=3 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading pyparsing-3.3.2-py3-none-any.whl (122 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 122.8/122.8 kB 13.8 MB/s eta 0:00:00
Collecting python-dateutil>=2.7 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 229.9/229.9 kB 21.4 MB/s eta 0:00:00
Collecting tzdata>=2022.7 (from pandas->visualdl->paddleocr==2.7.0)
  Downloading tzdata-2025.3-py2.py3-none-any.whl (348 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 348.5/348.5 kB 31.4 MB/s eta 0:00:00
Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/site-packages (from requests->premailer->paddleocr==2.7.0) (2.0.4)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.10/site-packages (from requests->premailer->paddleocr==2.7.0) (1.26.16)
Installing collected packages: pytz, lmdb, tzdata, typing-extensions, termcolor, soupsieve, rarfile, rapidfuzz, python-dateutil, pyparsing, PyMuPDF, pycryptodome, pyclipper, psutil, protobuf, Pillow, numpy, networkx, more-itertools, markupsafe, lxml, lazy-loader, kiwisolver, itsdangerous, h11, future, fonttools, et-xmlfile, decorator, cython, cycler, cssselect, click, cachetools, blinker, Babel, attrdict, astor, werkzeug, tifffile, shapely, scipy, python-docx, pandas, opt-einsum, openpyxl, opencv-python-headless, opencv-python, opencv-contrib-python, jinja2, imageio, httpcore, fire, exceptiongroup, cssutils, contourpy, beautifulsoup4, bce-python-sdk, scikit-image, premailer, pdf2docx, matplotlib, flask, anyio, imgaug, httpx, Flask-Babel, visualdl, paddlepaddle, paddleocr

----------------------------------------------------------
Collecting paddlepaddle==2.6.2
  Downloading paddlepaddle-2.6.2-cp310-cp310-manylinux1_x86_64.whl (126.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 126.0/126.0 MB 5.2 MB/s eta 0:00:00
Collecting paddleocr==2.7.0
  Downloading paddleocr-2.7.0.0-py3-none-any.whl (74.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 74.1/74.1 MB 7.0 MB/s eta 0:00:00
Collecting httpx (from paddlepaddle==2.6.2)
  Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 73.5/73.5 kB 7.8 MB/s eta 0:00:00
Collecting numpy>=1.13 (from paddlepaddle==2.6.2)
  Downloading numpy-2.2.6-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (16.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.8/16.8 MB 69.7 MB/s eta 0:00:00
Collecting Pillow (from paddlepaddle==2.6.2)
  Downloading pillow-12.1.1-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (7.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.0/7.0 MB 79.6 MB/s eta 0:00:00
Collecting decorator (from paddlepaddle==2.6.2)
  Downloading decorator-5.2.1-py3-none-any.whl (9.2 kB)
Collecting astor (from paddlepaddle==2.6.2)
  Downloading astor-0.8.1-py2.py3-none-any.whl (27 kB)
Collecting opt-einsum==3.3.0 (from paddlepaddle==2.6.2)
  Downloading opt_einsum-3.3.0-py3-none-any.whl (65 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65.5/65.5 kB 7.7 MB/s eta 0:00:00
Collecting protobuf>=3.20.2 (from paddlepaddle==2.6.2)
  Downloading protobuf-6.33.5-cp39-abi3-manylinux2014_x86_64.whl (323 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 323.5/323.5 kB 32.0 MB/s eta 0:00:00
Collecting shapely (from paddleocr==2.7.0)
  Downloading shapely-2.1.2-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (3.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.1/3.1 MB 40.2 MB/s eta 0:00:00
Collecting scikit-image (from paddleocr==2.7.0)
  Downloading scikit_image-0.25.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (14.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14.8/14.8 MB 27.2 MB/s eta 0:00:00
Collecting imgaug (from paddleocr==2.7.0)
  Downloading imgaug-0.4.0-py2.py3-none-any.whl (948 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 948.0/948.0 kB 43.3 MB/s eta 0:00:00
Collecting pyclipper (from paddleocr==2.7.0)
  Downloading pyclipper-1.4.0-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (970 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 971.0/971.0 kB 33.9 MB/s eta 0:00:00
Collecting lmdb (from paddleocr==2.7.0)
  Downloading lmdb-1.7.5-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (292 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 292.4/292.4 kB 23.9 MB/s eta 0:00:00
Requirement already satisfied: tqdm in /usr/local/lib/python3.10/site-packages (from paddleocr==2.7.0) (4.65.0)
Collecting visualdl (from paddleocr==2.7.0)
  Downloading visualdl-2.5.3-py3-none-any.whl (6.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.3/6.3 MB 24.1 MB/s eta 0:00:00
Collecting rapidfuzz (from paddleocr==2.7.0)
  Downloading rapidfuzz-3.14.3-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (3.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.2/3.2 MB 17.4 MB/s eta 0:00:00
Collecting opencv-python<=4.6.0.66 (from paddleocr==2.7.0)
  Downloading opencv_python-4.6.0.66-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (60.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.9/60.9 MB 7.5 MB/s eta 0:00:00
Collecting opencv-contrib-python<=4.6.0.66 (from paddleocr==2.7.0)
  Downloading opencv_contrib_python-4.6.0.66-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (67.1 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 67.1/67.1 MB 7.1 MB/s eta 0:00:00
Collecting cython (from paddleocr==2.7.0)
  Downloading cython-3.2.4-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (3.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.5/3.5 MB 95.4 MB/s eta 0:00:00
Collecting lxml (from paddleocr==2.7.0)
  Downloading lxml-6.0.2-cp310-cp310-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl (5.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.3/5.3 MB 99.0 MB/s eta 0:00:00
Collecting premailer (from paddleocr==2.7.0)
  Downloading premailer-3.10.0-py2.py3-none-any.whl (19 kB)
Collecting openpyxl (from paddleocr==2.7.0)
  Downloading openpyxl-3.1.5-py2.py3-none-any.whl (250 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 250.9/250.9 kB 25.2 MB/s eta 0:00:00
Collecting attrdict (from paddleocr==2.7.0)
  Downloading attrdict-2.0.1-py2.py3-none-any.whl (9.9 kB)
Collecting PyMuPDF<1.21.0 (from paddleocr==2.7.0)
  Downloading PyMuPDF-1.20.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (8.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.9/8.9 MB 78.8 MB/s eta 0:00:00
Collecting python-docx (from paddleocr==2.7.0)
  Downloading python_docx-1.2.0-py3-none-any.whl (252 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 253.0/253.0 kB 23.3 MB/s eta 0:00:00
Collecting beautifulsoup4 (from paddleocr==2.7.0)
  Downloading beautifulsoup4-4.14.3-py3-none-any.whl (107 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 107.7/107.7 kB 12.9 MB/s eta 0:00:00
Collecting fonttools>=4.24.0 (from paddleocr==2.7.0)
  Downloading fonttools-4.61.1-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.9/4.9 MB 68.0 MB/s eta 0:00:00
Collecting fire>=0.3.0 (from paddleocr==2.7.0)
  Downloading fire-0.7.1-py3-none-any.whl (115 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 115.9/115.9 kB 10.7 MB/s eta 0:00:00
Collecting pdf2docx (from paddleocr==2.7.0)
  Downloading pdf2docx-0.5.10-py3-none-any.whl (134 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.3/134.3 kB 9.4 MB/s eta 0:00:00
Collecting termcolor (from fire>=0.3.0->paddleocr==2.7.0)
  Downloading termcolor-3.3.0-py3-none-any.whl (7.7 kB)
Requirement already satisfied: six in /usr/local/lib/python3.10/site-packages (from attrdict->paddleocr==2.7.0) (1.16.0)
Collecting soupsieve>=1.6.1 (from beautifulsoup4->paddleocr==2.7.0)
  Downloading soupsieve-2.8.3-py3-none-any.whl (37 kB)
Collecting typing-extensions>=4.0.0 (from beautifulsoup4->paddleocr==2.7.0)
  Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.6/44.6 kB 4.9 MB/s eta 0:00:00
Collecting anyio (from httpx->paddlepaddle==2.6.2)
  Downloading anyio-4.12.1-py3-none-any.whl (113 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 113.6/113.6 kB 10.7 MB/s eta 0:00:00
Requirement already satisfied: certifi in /usr/local/lib/python3.10/site-packages (from httpx->paddlepaddle==2.6.2) (2026.1.4)
Collecting httpcore==1.* (from httpx->paddlepaddle==2.6.2)
  Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.8/78.8 kB 9.5 MB/s eta 0:00:00
Requirement already satisfied: idna in /usr/local/lib/python3.10/site-packages (from httpx->paddlepaddle==2.6.2) (3.4)
Collecting h11>=0.16 (from httpcore==1.*->httpx->paddlepaddle==2.6.2)
  Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Collecting scipy (from imgaug->paddleocr==2.7.0)
  Downloading scipy-1.15.3-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (37.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 37.7/37.7 MB 12.9 MB/s eta 0:00:00
Collecting matplotlib (from imgaug->paddleocr==2.7.0)
  Downloading matplotlib-3.10.8-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (8.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.7/8.7 MB 106.4 MB/s eta 0:00:00
Collecting imageio (from imgaug->paddleocr==2.7.0)
  Downloading imageio-2.37.2-py3-none-any.whl (317 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 317.6/317.6 kB 32.6 MB/s eta 0:00:00
Collecting networkx>=3.0 (from scikit-image->paddleocr==2.7.0)
  Downloading networkx-3.4.2-py3-none-any.whl (1.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.7/1.7 MB 66.4 MB/s eta 0:00:00
Collecting tifffile>=2022.8.12 (from scikit-image->paddleocr==2.7.0)
  Downloading tifffile-2025.5.10-py3-none-any.whl (226 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 226.5/226.5 kB 26.8 MB/s eta 0:00:00
Requirement already satisfied: packaging>=21 in /usr/local/lib/python3.10/site-packages (from scikit-image->paddleocr==2.7.0) (23.0)
Collecting lazy-loader>=0.4 (from scikit-image->paddleocr==2.7.0)
  Downloading lazy_loader-0.4-py3-none-any.whl (12 kB)
Collecting et-xmlfile (from openpyxl->paddleocr==2.7.0)
  Downloading et_xmlfile-2.0.0-py3-none-any.whl (18 kB)
INFO: pip is looking at multiple versions of pdf2docx to determine which version is compatible with other requirements. This could take a while.
Collecting pdf2docx (from paddleocr==2.7.0)
  Downloading pdf2docx-0.5.9-py3-none-any.whl (133 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 133.8/133.8 kB 14.4 MB/s eta 0:00:00
  Downloading pdf2docx-0.5.8-py3-none-any.whl (132 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 132.0/132.0 kB 14.7 MB/s eta 0:00:00
Collecting opencv-python-headless>=4.5 (from pdf2docx->paddleocr==2.7.0)
  Downloading opencv_python_headless-4.13.0.92-cp37-abi3-manylinux_2_28_x86_64.whl (60.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.4/60.4 MB 7.5 MB/s eta 0:00:00
Collecting cssselect (from premailer->paddleocr==2.7.0)
  Downloading cssselect-1.4.0-py3-none-any.whl (18 kB)
Collecting cssutils (from premailer->paddleocr==2.7.0)
  Downloading cssutils-2.11.1-py3-none-any.whl (385 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 385.7/385.7 kB 27.0 MB/s eta 0:00:00
Requirement already satisfied: requests in /usr/local/lib/python3.10/site-packages (from premailer->paddleocr==2.7.0) (2.29.0)
Collecting cachetools (from premailer->paddleocr==2.7.0)
  Downloading cachetools-7.0.1-py3-none-any.whl (13 kB)
Collecting bce-python-sdk (from visualdl->paddleocr==2.7.0)
  Downloading bce_python_sdk-0.9.60-py3-none-any.whl (395 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 395.4/395.4 kB 36.1 MB/s eta 0:00:00
Collecting flask>=1.1.1 (from visualdl->paddleocr==2.7.0)
  Downloading flask-3.1.3-py3-none-any.whl (103 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 103.4/103.4 kB 12.1 MB/s eta 0:00:00
Collecting Flask-Babel>=3.0.0 (from visualdl->paddleocr==2.7.0)
  Downloading flask_babel-4.0.0-py3-none-any.whl (9.6 kB)
Collecting pandas (from visualdl->paddleocr==2.7.0)
  Downloading pandas-2.3.3-cp310-cp310-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (12.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.8/12.8 MB 68.1 MB/s eta 0:00:00
Collecting rarfile (from visualdl->paddleocr==2.7.0)
  Downloading rarfile-4.2-py3-none-any.whl (29 kB)
Collecting psutil (from visualdl->paddleocr==2.7.0)
  Downloading psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl (155 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 155.6/155.6 kB 13.4 MB/s eta 0:00:00
Collecting blinker>=1.9.0 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
Collecting click>=8.1.3 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading click-8.3.1-py3-none-any.whl (108 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 108.3/108.3 kB 12.1 MB/s eta 0:00:00
Collecting itsdangerous>=2.2.0 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Collecting jinja2>=3.1.2 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 134.9/134.9 kB 9.8 MB/s eta 0:00:00
Collecting markupsafe>=2.1.1 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading markupsafe-3.0.3-cp310-cp310-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (20 kB)
Collecting werkzeug>=3.1.0 (from flask>=1.1.1->visualdl->paddleocr==2.7.0)
  Downloading werkzeug-3.1.6-py3-none-any.whl (225 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 225.2/225.2 kB 17.5 MB/s eta 0:00:00
Collecting Babel>=2.12 (from Flask-Babel>=3.0.0->visualdl->paddleocr==2.7.0)
  Downloading babel-2.18.0-py3-none-any.whl (10.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.2/10.2 MB 62.5 MB/s eta 0:00:00
Collecting pytz>=2022.7 (from Flask-Babel>=3.0.0->visualdl->paddleocr==2.7.0)
  Downloading pytz-2025.2-py2.py3-none-any.whl (509 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 509.2/509.2 kB 32.6 MB/s eta 0:00:00
Collecting exceptiongroup>=1.0.2 (from anyio->httpx->paddlepaddle==2.6.2)
  Downloading exceptiongroup-1.3.1-py3-none-any.whl (16 kB)
Collecting pycryptodome>=3.8.0 (from bce-python-sdk->visualdl->paddleocr==2.7.0)
  Downloading pycryptodome-3.23.0-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.3/2.3 MB 35.3 MB/s eta 0:00:00
Collecting future>=0.6.0 (from bce-python-sdk->visualdl->paddleocr==2.7.0)
  Downloading future-1.0.0-py3-none-any.whl (491 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 491.3/491.3 kB 37.8 MB/s eta 0:00:00
Collecting more-itertools (from cssutils->premailer->paddleocr==2.7.0)
  Downloading more_itertools-10.8.0-py3-none-any.whl (69 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 69.7/69.7 kB 8.3 MB/s eta 0:00:00
Collecting contourpy>=1.0.1 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading contourpy-1.3.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (325 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 325.0/325.0 kB 26.1 MB/s eta 0:00:00
Collecting cycler>=0.10 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading cycler-0.12.1-py3-none-any.whl (8.3 kB)
Collecting kiwisolver>=1.3.1 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading kiwisolver-1.4.9-cp310-cp310-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (1.6 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 66.6 MB/s eta 0:00:00
Collecting pyparsing>=3 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading pyparsing-3.3.2-py3-none-any.whl (122 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 122.8/122.8 kB 13.8 MB/s eta 0:00:00
Collecting python-dateutil>=2.7 (from matplotlib->imgaug->paddleocr==2.7.0)
  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 229.9/229.9 kB 21.4 MB/s eta 0:00:00
Collecting tzdata>=2022.7 (from pandas->visualdl->paddleocr==2.7.0)
  Downloading tzdata-2025.3-py2.py3-none-any.whl (348 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 348.5/348.5 kB 31.4 MB/s eta 0:00:00
Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/site-packages (from requests->premailer->paddleocr==2.7.0) (2.0.4)
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /usr/local/lib/python3.10/site-packages (from requests->premailer->paddleocr==2.7.0) (1.26.16)
Installing collected packages: pytz, lmdb, tzdata, typing-extensions, termcolor, soupsieve, rarfile, rapidfuzz, python-dateutil, pyparsing, PyMuPDF, pycryptodome, pyclipper, psutil, protobuf, Pillow, numpy, networkx, more-itertools, markupsafe, lxml, lazy-loader, kiwisolver, itsdangerous, h11, future, fonttools, et-xmlfile, decorator, cython, cycler, cssselect, click, cachetools, blinker, Babel, attrdict, astor, werkzeug, tifffile, shapely, scipy, python-docx, pandas, opt-einsum, openpyxl, opencv-python-headless, opencv-python, opencv-contrib-python, jinja2, imageio, httpcore, fire, exceptiongroup, cssutils, contourpy, beautifulsoup4, bce-python-sdk, scikit-image, premailer, pdf2docx, matplotlib, flask, anyio, imgaug, httpx, Flask-Babel, visualdl, paddlepaddle, paddleocr
Successfully installed Babel-2.18.0 Flask-Babel-4.0.0 Pillow-12.1.1 PyMuPDF-1.20.2 anyio-4.12.1 astor-0.8.1 attrdict-2.0.1 bce-python-sdk-0.9.60 beautifulsoup4-4.14.3 blinker-1.9.0 cachetools-7.0.1 click-8.3.1 contourpy-1.3.2 cssselect-1.4.0 cssutils-2.11.1 cycler-0.12.1 cython-3.2.4 decorator-5.2.1 et-xmlfile-2.0.0 exceptiongroup-1.3.1 fire-0.7.1 flask-3.1.3 fonttools-4.61.1 future-1.0.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 imageio-2.37.2 imgaug-0.4.0 itsdangerous-2.2.0 jinja2-3.1.6 kiwisolver-1.4.9 lazy-loader-0.4 lmdb-1.7.5 lxml-6.0.2 markupsafe-3.0.3 matplotlib-3.10.8 more-itertools-10.8.0 networkx-3.4.2 numpy-2.2.6 opencv-contrib-python-4.6.0.66 opencv-python-4.6.0.66 opencv-python-headless-4.13.0.92 openpyxl-3.1.5 opt-einsum-3.3.0 paddleocr-2.7.0.0 paddlepaddle-2.6.2 pandas-2.3.3 pdf2docx-0.5.8 premailer-3.10.0 protobuf-6.33.5 psutil-7.2.2 pyclipper-1.4.0 pycryptodome-3.23.0 pyparsing-3.3.2 python-dateutil-2.9.0.post0 python-docx-1.2.0 pytz-2025.2 rapidfuzz-3.14.3 rarfile-4.2 scikit-image-0.25.2 scipy-1.15.3 shapely-2.1.2 soupsieve-2.8.3 termcolor-3.3.0 tifffile-2025.5.10 typing-extensions-4.15.0 tzdata-2025.3 visualdl-2.5.3 werkzeug-3.1.6
WARNING: The following packages were previously imported in this runtime:
  [astor,click,cv2,cycler,dateutil,decorator,google,httpx,kiwisolver,matplotlib,more_itertools,mpl_toolkits,numpy,opt_einsum,paddle,psutil,pyparsing]
You must restart the runtime in order to use newly installed versions.