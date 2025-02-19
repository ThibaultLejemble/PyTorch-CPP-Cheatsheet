PyTorch C++ Cheatsheet
======================

.. include:: brief.rst

Tensor creation 
----------------

|  See also `tensor_creation.html <https://pytorch.org/cppdocs/notes/tensor_creation.html>`_
|  Factory arguments order = `(function-specific, sizes, options)` (except for `torch::full`)

.. code-block:: cpp

    torch::Tensor x;
    auto opts = torch::TensorOptions()
        .dtype(torch::kFloat32)     // kUInt8, kInt8, kInt16, kInt32, kInt64, kFloat32, or kFloat64
        .layout(torch::kStrided)    // kStrided, or kSparse
        .device(torch::kCPU)        // kCPU, or kCUDA
        .requires_grad(false);      // true, or false
    
    x = torch::zeros({3,2}, opts);          // 0
    x = torch::ones( {3,2}, opts);          // 1
    x = torch::empty({3,2}, opts);          // uninitialized  
    x = torch::full( {3,2}, 3.14f, opts);   // single value (warning: args order)
    x = torch::eye(  5,     opts);          // identity matrix (square)
    x = torch::eye(  3, 2,  opts);          // identity matrix (rectangular)
    x = torch::rand( {3,2}, opts);          // uniform distribution on [0, 1)
    x = torch::randn({3,2}, opts);          // center-normalized normal distribution 
    x = torch::randint(10, {3,2}, opts);    // random integers (low=0)
    x = torch::randint(3, 10, {3,2}, opts); // random integers in (low,high)
    
    // multiple chained short options
    x = torch::zeros({3,2}, torch::dtype(torch::kFloat64).device(torch::kCPU));
    
    // only one option (directly given as parameter)
    x = torch::zeros({3,2}, torch::kFloat64);

Tensor shape
------------

.. code-block:: cpp

    torch::Tensor x = torch::rand({3, 4, 5});
    
    // dimension
    int dim = x.dim();
    assert(dim == 3);
    
    // sizes
    torch::ArrayRef<long int> sizes = x.sizes();
    assert(sizes == std::vector<int64_t>({3, 4, 5})); // comparable to std::vector<int64_t>
    
    // single size
    int size1 = x.size(1);
    assert(size1 == 4);

Tensor data type
----------------

|  Types are constexpr values of enum class type `torch::ScalarType`
|  See the enum class type here: `ScalarType.h <https://github.com/pytorch/pytorch/blob/69301fb10eb3f7fd49af5c681a2e386af115baba/c10/core/ScalarType.h#L151C12-L151C22>`_
|  See the different types here: `types.h <https://github.com/pytorch/pytorch/blob/69301fb10eb3f7fd49af5c681a2e386af115baba/torch/csrc/api/include/torch/types.h>`_

.. code-block:: cpp

    torch::ScalarType type_float32 = torch::kFloat32; // or torch::kF32
    
    // map torch to c++ type
    static_assert(std::is_same_v<c10::impl::ScalarTypeToCPPType<torch::kFloat32>::type, float>);
    static_assert(std::is_same_v<c10::impl::ScalarTypeToCPPType<torch::kFloat64>::type, double>);
    static_assert(std::is_same_v<c10::impl::ScalarTypeToCPPType<torch::kInt32>::type,   int>);
    
    // map c++ to torch type (Cpp not CPP!)
    static_assert(c10::CppTypeToScalarType<float>::value  == torch::kFloat32);
    static_assert(c10::CppTypeToScalarType<double>::value == torch::kFloat64);
    static_assert(c10::CppTypeToScalarType<int>::value    == torch::kInt32);
    
    std::cout << torch::toString(torch::kFloat32) << std::endl; // print 'Float'
    const size_t bytes = torch::elementSize(torch::kFloat32);   // dynamic equivalent of sizeof(float)
    assert(bytes == 4); // 4 bytes = 32 bits
    
    assert(torch::isIntegralType(torch::kFloat32, /*includeBool=*/true) == false);
    assert(torch::isFloatingType(torch::kFloat32) == true);

Tensor (efficient) accessors 
-----------------------------

|  See also `tensor_basics.html <https://pytorch.org/cppdocs/notes/tensor_basics.html#efficient-access-to-tensor-elements>`_
|  Type and dimension must be known at compile-time 

.. code-block:: cpp

    torch::Tensor x = torch::rand({3, 4, 5});
    
    // cpu
    auto accessor = x.accessor<float,3>(); // dim = 3
    accessor[1][2][0] = 3.14f;
    float& ref = accessor[1][2][0];
    

Tensor (inefficient) indexing 
------------------------------

|  See also `tensor_indexing.html <https://pytorch.org/cppdocs/notes/tensor_indexing.html>`_

.. code-block:: cpp

    torch::Tensor x = torch::rand({3, 4, 5});
    x.index({1, 2, 0}) = 3.14f;
    torch::Tensor y = x.index({1, 2, 0});
    assert(y.dim() == 0); // 0-dim tensor = juste one value
    float val = y.item<float>();

Tensor memory and device
------------------------

|  Row-major order by default

.. code-block:: cpp

    torch::Tensor x = torch::rand({3, 4, 5});
    
    // memory ptr
    void* raw_ptr = x.data_ptr();
    float* typed_ptr = x.data_ptr<float>();
    
    // device
    assert(    x.is_cpu());
    assert(not x.is_cuda());
    
    torch::Device device = x.device();
    assert(    device.is_cpu());
    assert(not device.is_cuda());
    
    // memory layout
    assert(x.is_contiguous());
    torch::Layout layout = x.layout();
    long int stride0 = x.stride(0);
    long int stride1 = x.stride(1);
    long int stride2 = x.stride(2);
    assert(stride0 == 4*5); // x[0,i,j] and x[1,i,j] are 10 values apart
    assert(stride1 == 5);
    assert(stride2 == 1);

Dispatching
-----------

.. code-block:: cpp

    torch::Tensor x = torch::rand({3, 4, 5});
    // AT_DISPATCH_ALL_TYPES(x.scalar_type(), "unique_name", [&] {
    //     scalar_t val;
    // });

Tensor creation from raw data
-----------------------------

.. code-block:: cpp

    int* raw_data = (int*)malloc(3 * 4 * sizeof(int));
    for(int i = 0; i < 3 * 4; ++i)
        raw_data[i] = i;
    // data = [0,  1,  2,  3,
    //         4,  5,  6,  7,
    //         8,  9, 10, 11]
    std::function<void(void*)> deleter = [](void*){std::cout << "delete!" << std::endl;};
    torch::Tensor x = torch::from_blob(raw_data, {3, 4}, deleter, torch::dtype(torch::kInt32));
    // end of scope prints "delete!"

