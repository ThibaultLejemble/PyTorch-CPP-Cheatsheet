# PyTorch C++ Cheatsheet

![logo](https://github.com/ThibaultLejemble/PyTorch-CPP-Cheatsheet/blob/d4e5360f53145e24d53d706c8aded8b46a203674/docs/_static/logo.png)

A unique C++ file showing how to use the [PyTorch C++ API](https://pytorch.org/cppdocs) : [`pytorch_cpp_cheatsheet.cpp`](https://github.com/ThibaultLejemble/PyTorch-CPP-Cheatsheet/blob/main/pytorch_cpp_cheatsheet.cpp).

Checkout the HTML version [here](https://thibaultlejemble.github.io/PyTorch-CPP-Cheatsheet/index.html).

## Build and run the C++ executable

Download PyTorch from [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally).
- `Stable (2.6.0)`
- `Linux`
- `LibTorch`
- `C++/Java`
- `CPU`
```bash
wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.6.0%2Bcpu.zip
unzip libtorch-cxx11-abi-shared-with-deps-2.6.0+cpu.zip
```

Run CMake and compile
```bash
mkdir -p build
cd build
cmake -DCMAKE_PREFIX_PATH=$(pwd)/../libtorch ..
make
```

Execute 
```bash
./pytorch_cpp_cheatsheet
````
