#include <torch/torch.h>

#include <iostream>

int main(int argc, char const *argv[])
{
    //! ==============================================================
    //! Tensor creation 
    //! ==============================================================
    {
        //!
        //! See also [tensor_creation.html](https://pytorch.org/cppdocs/notes/tensor_creation.html)
        //!
        //! Factory arguments order = `(function-specific, sizes, options)` (except for torch::full)
        //!
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
        x = torch::randn({3,2}, opts);          // unit normal distribution 
        x = torch::randint(10, {3,2}, opts);    // random integers (low=0)
        x = torch::randint(3, 10, {3,2}, opts); // random integers in (low,high)
        // linspace
        // arange
        // logspace
        // randperm

        // multiple chained short options
        x = torch::zeros({3,2}, torch::dtype(torch::kFloat64).device(torch::kCPU));

        // only one option (directly given as parameter)
        x = torch::zeros({3,2}, torch::kFloat64);
    }
    //! ==============================================================
    //! Tensor shape
    //! ==============================================================
    {
        const torch::Tensor x = torch::randn({3, 4, 5});
        
        // dimension
        const int dim = x.dim();
        assert(dim == 3);
        
        // sizes
        const torch::ArrayRef<long int> sizes = x.sizes();
        assert(sizes == std::vector<int64_t>({3, 4, 5})); // comparable to std::vector<int64_t>

        // single size
        const int size1 = x.size(1); // same as x.sizes()[1]
        assert(size1 == 4);
    }
    //! ==============================================================
    //! Tensor data type
    //! ==============================================================
    {
        //!
        //! types are static constant of type `torch::ScalarType`
        //!
        torch::ScalarType type_float32 = torch::kFloat32; // type = c10::ScalarType
        
        // map torch to c++ type
        static_assert(std::is_same_v<c10::impl::ScalarTypeToCPPType<torch::kFloat32>::type, float>);
        static_assert(std::is_same_v<c10::impl::ScalarTypeToCPPType<torch::kFloat64>::type, double>);
        static_assert(std::is_same_v<c10::impl::ScalarTypeToCPPType<torch::kInt32>::type,   int>);
        // ...

        // map c++ to torch type (Cpp not CPP)
        static_assert(c10::CppTypeToScalarType<float>::value == torch::kFloat32);
        // ...

        std::cout << torch::toString(torch::kFloat32) << std::endl; // print ''
        const size_t bytes = torch::elementSize(torch::kFloat32);
        assert(bytes == 4); // 4 bytes = 32 bits

        assert(torch::isIntegralType(torch::kFloat32, /*includeBool=*/true) == false);
        assert(torch::isFloatingType(torch::kFloat32) == true);
    }
    //! ==============================================================
    //! Tensor accessors 
    //! ==============================================================
    {
        //!
        //! see also [tensor_basics.html](https://pytorch.org/cppdocs/notes/tensor_basics.html#efficient-access-to-tensor-elements)
        //!
        torch::Tensor x = torch::zeros({4,3,2}, torch::kFloat32);

        // cpu
        auto accessor = x.accessor<float,3>(); // dim = 3
        accessor[1][2][0] = 3.14f;

        // gpu
        // TODO
    }
    //! ==============================================================
    //! Tensor memory and device
    //! ==============================================================
    {
        torch::Tensor x = torch::zeros({4,3,2}, torch::kFloat32);

        // memory ptr
        void* raw_ptr = x.data_ptr();
        float* typed_ptr = x.data_ptr<float>();
        
        // device
        assert(x.is_cpu());
        assert(not x.is_cuda());

        torch::Device device = x.device();
        assert(device.is_cpu());
        assert(not device.is_cuda());
        
        // memory
        assert(x.is_contiguous());
        torch::Layout layout = x.layout();
        long int stride0 = x.stride(0);
        long int stride1 = x.stride(1);
        long int stride2 = x.stride(2);
        assert(stride0 == 3*2);
        assert(stride1 == 2);
        assert(stride2 == 1);
    }
    //! ==============================================================
    //! Dispatch
    //! ==============================================================
    {
        torch::Tensor x = torch::rand({3,2}, torch::kFloat32);
        AT_DISPATCH_ALL_TYPES(x.scalar_type(), "unique_name", [&] {
            scalar_t val;
        });
    }
    //! ==============================================================
    //! From blob
    //! ==============================================================
    {
        int rows = 4;
        int cols = 3;
        int* raw_data = (int*)malloc(rows * cols * sizeof(int));
        for(int i = 0; i < rows * cols; ++i)
            raw_data[i] = i;
        // data = [0,  1,  2,
        //         3,  4,  5,
        //         6,  7,  8,
        //         9, 10, 11]
        std::function<void(void*)> deleter = [](void*){std::cout << "delete!" << std::endl;};
        torch::Tensor x = torch::from_blob(raw_data, {rows, cols}, deleter, torch::dtype(torch::kInt32));
        std::cout << x << std::endl;
        // end of scope prints 'delete!'
    }
    //! ==============================================================
    //! Indexing
    //! ==============================================================
    {
        //! see [tensor_indexing.html](https://pytorch.org/cppdocs/notes/tensor_indexing.html)
        torch::Tensor x = torch::rand({10,20,30});
        std::cout << x.index({1, 2, 3}).sizes() << std::endl;
    }

    // TODO

    // auto indices = torch::arange({20}, torch::kInt32);
    // std::cout << "indices = " << indices << std::endl;

    // std::cout << "____" << std::endl;
    // auto tmp0 = torch::randperm(10);
    // std::cout << "tmp0 = " << tmp0 << std::endl;
    // indices = torch::gather(indices, 0, tmp0);
    // std::cout << "indices = " << indices << std::endl;


    // std::cout << "____" << std::endl;
    // auto tmp1 = torch::randperm(5);
    // std::cout << "tmp1 = " << tmp1 << std::endl;
    // indices = torch::gather(indices, 0, tmp1);
    // std::cout << "indices = " << indices << std::endl;

    return 0;
}
