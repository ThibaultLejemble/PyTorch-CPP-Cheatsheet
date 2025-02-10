# PyTorch-CPP-Cheatsheet

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
