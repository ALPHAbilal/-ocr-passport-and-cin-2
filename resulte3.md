Looking in indexes: https://www.paddlepaddle.org.cn/packages/stable/cpu/
Collecting paddlepaddle==3.0.0
  Downloading https://paddle-whl.bj.bcebos.com/stable/cpu/paddlepaddle/paddlepaddle-3.0.0-cp313-cp313-win_amd64.whl (97.1 MB)
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
     ---------------------------------------- 0.0/97.1 MB ? eta -:--:--
...
Requirement already satisfied: pycryptodome>=3.8.0 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from bce-python-sdk->aistudio-sdk>=0.3.5->paddlex<3.5.0,>=3.4.0->paddlex[ocr-core]<3.5.0,>=3.4.0->paddleocr) (3.23.0)
Requirement already satisfied: future>=0.6.0 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from bce-python-sdk->aistudio-sdk>=0.3.5->paddlex<3.5.0,>=3.4.0->paddlex[ocr-core]<3.5.0,>=3.4.0->paddleocr) (1.0.0)
Requirement already satisfied: fsspec>=2023.5.0 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from huggingface-hub->paddlex<3.5.0,>=3.4.0->paddlex[ocr-core]<3.5.0,>=3.4.0->paddleocr) (2025.5.1)
Requirement already satisfied: wcwidth in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from prettytable->paddlex<3.5.0,>=3.4.0->paddlex[ocr-core]<3.5.0,>=3.4.0->paddleocr) (0.2.13)
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

[notice] A new release of pip is available: 25.2 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
Requirement already satisfied: shapely in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (2.1.1)
Requirement already satisfied: scikit-image in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (0.26.0)
Collecting protobuf<4.0,>=3.20.0
  Downloading protobuf-3.20.3-py2.py3-none-any.whl.metadata (720 bytes)
Requirement already satisfied: numpy>=1.21 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from shapely) (2.3.4)
Requirement already satisfied: scipy>=1.11.4 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from scikit-image) (1.15.3)
Requirement already satisfied: networkx>=3.0 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from scikit-image) (3.5)
Requirement already satisfied: pillow>=10.1 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from scikit-image) (11.2.1)
Requirement already satisfied: imageio!=2.35.0,>=2.33 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from scikit-image) (2.37.2)
Requirement already satisfied: tifffile>=2022.8.12 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from scikit-image) (2026.2.20)
Requirement already satisfied: packaging>=21 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from scikit-image) (24.2)
Requirement already satisfied: lazy-loader>=0.4 in c:\users\user004\appdata\local\programs\python\python313\lib\site-packages (from scikit-image) (0.4)
Downloading protobuf-3.20.3-py2.py3-none-any.whl (162 kB)
Installing collected packages: protobuf
  Attempting uninstall: protobuf
    Found existing installation: protobuf 6.32.0
    Uninstalling protobuf-6.32.0:
      Successfully uninstalled protobuf-6.32.0
Successfully installed protobuf-3.20.3
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
grpcio-status 1.74.0 requires protobuf<7.0.0,>=6.31.1, but you have protobuf 3.20.3 which is incompatible.
opentelemetry-exporter-otlp-proto-http 1.33.1 requires opentelemetry-exporter-otlp-proto-common==1.33.1, but you have opentelemetry-exporter-otlp-proto-common 1.39.1 which is incompatible.
opentelemetry-exporter-otlp-proto-http 1.33.1 requires opentelemetry-proto==1.33.1, but you have opentelemetry-proto 1.39.1 which is incompatible.
opentelemetry-exporter-otlp-proto-http 1.33.1 requires opentelemetry-sdk~=1.33.1, but you have opentelemetry-sdk 1.39.1 which is incompatible.
opentelemetry-proto 1.39.1 requires protobuf<7.0,>=5.0, but you have protobuf 3.20.3 which is incompatible.

[notice] A new release of pip is available: 25.2 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip

-------------------------------
c:\Users\User004\AppData\Local\Programs\Python\Python313\Lib\site-packages\paddle\utils\cpp_extension\extension_utils.py:711: UserWarning: No ccache found. Please be aware that recompiling all source files may be required. You can download and install ccache from: https://github.com/ccache/ccache/blob/master/doc/INSTALL.md
  warnings.warn(warning_message)
PaddlePaddle version: 3.0.0
c:\Users\User004\AppData\Local\Programs\Python\Python313\Lib\site-packages\requests\__init__.py:113: RequestsDependencyWarning: urllib3 (2.4.0) or chardet (6.0.0.post1)/charset_normalizer (3.4.2) doesn't match a supported version!
  warnings.warn(
c:\Users\User004\AppData\Local\Programs\Python\Python313\Lib\site-packages\tqdm\auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm
---------------------------------------------------------------------------
OSError                                   Traceback (most recent call last)
Cell In[2], line 5
      2 import paddle
      3 print(f"PaddlePaddle version: {paddle.__version__}")
----> 5 from paddleocr import PaddleOCR
      6 print("PaddleOCR imported OK")

File c:\Users\User004\AppData\Local\Programs\Python\Python313\Lib\site-packages\paddleocr\__init__.py:15
      1 # Copyright (c) 2025 PaddlePaddle Authors. All Rights Reserved.
      2 #
      3 # Licensed under the Apache License, Version 2.0 (the "License");
   (...)     12 # See the License for the specific language governing permissions and
     13 # limitations under the License.
---> 15 from paddlex.inference.utils.benchmark import benchmark
     17 from ._models import (
     18     ChartParsing,
     19     DocImgOrientationClassification,
   (...)     30     TextRecognition,
     31 )
     32 from ._pipelines import (
     33     DocPreprocessor,
     34     DocUnderstanding,
   (...)     42     TableRecognitionPipelineV2,
     43 )
...
--> 253     raise err
    254 elif res is not None:
    255     is_loaded = True

OSError: [WinError 127] The specified procedure could not be found. Error loading "c:\Users\User004\AppData\Local\Programs\Python\Python313\Lib\site-packages\torch\lib\shm.dll" or one of its dependencies.
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...