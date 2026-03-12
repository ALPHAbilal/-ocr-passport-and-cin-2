  failed with:

         no such file or directory


      CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
      CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage
      -- Configuring incomplete, errors occurred!

      *** CMake configuration failed
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for llama-cpp-python
Failed to build llama-cpp-python

[notice] A new release of pip is available: 24.3.1 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
ERROR: ERROR: Failed to build installable wheels for some pyproject.toml based projects (llama-cpp-python)
(venv) PS E:\-ocr-passport-and-cin-2>  pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu       
Looking in indexes: https://pypi.org/simple, https://abetlen.github.io/llama-cpp-python/whl/cpu
Collecting llama-cpp-python
  Using cached llama_cpp_python-0.3.16.tar.gz (50.7 MB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Installing backend dependencies ... done
  Preparing metadata (pyproject.toml) ... done
Requirement already satisfied: typing-extensions>=4.5.0 in e:\-ocr-passport-and-cin-2\venv\lib\site-packages (from llama-cpp-python) (4.15.0)
Requirement already satisfied: numpy>=1.20.0 in e:\-ocr-passport-and-cin-2\venv\lib\site-packages (from llama-cpp-python) (2.4.3)
Collecting diskcache>=5.6.1 (from llama-cpp-python)
  Using cached diskcache-5.6.3-py3-none-any.whl.metadata (20 kB)
Requirement already satisfied: jinja2>=2.11.3 in e:\-ocr-passport-and-cin-2\venv\lib\site-packages (from llama-cpp-python) (3.1.6)
Requirement already satisfied: MarkupSafe>=2.0 in e:\-ocr-passport-and-cin-2\venv\lib\site-packages (from jinja2>=2.11.3->llama-cpp-python) (3.0.3)
Using cached diskcache-5.6.3-py3-none-any.whl (45 kB)
Building wheels for collected packages: llama-cpp-python
  Building wheel for llama-cpp-python (pyproject.toml) ... error
  error: subprocess-exited-with-error

  × Building wheel for llama-cpp-python (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [20 lines of output]
      *** scikit-build-core 0.12.2 using CMake 4.2.3 (wheel)
      *** Configuring CMake...
      2026-03-12 11:32:19,403 - scikit_build_core - WARNING - Can't find a Python library, got libdir=None, ldlibrary=None, multiarch=None, masd=None
      loading initial cache file C:\Users\Bilal\AppData\Local\Temp\tmp50pgm480\build\CMakeInit.txt
      -- Building for: NMake Makefiles
      CMake Error at CMakeLists.txt:3 (project):
        Running

         'nmake' '-?'

        failed with:

         no such file or directory


      CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
      CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage
      -- Configuring incomplete, errors occurred!

      *** CMake configuration failed
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for llama-cpp-python
Failed to build llama-cpp-python

[notice] A new release of pip is available: 24.3.1 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
ERROR: ERROR: Failed to build installable wheels for some pyproject.toml based projects (llama-cpp-python)
(venv) PS E:\-ocr-passport-and-cin-2> 