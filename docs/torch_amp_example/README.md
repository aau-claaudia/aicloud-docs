The NVIDIA Tesla V100 comes with specialized hardware for tensor operations called tensor cores. For the V100, the tensor cores work on integers or half-precision floats and the default in many DNN frameworks is single precision. Additional changes to the code are then necessary to activate half-precision models in cuDNN and utilize the tensor core hardware for:

1. Faster execution
2. Lower memory footprint that allows for an increased batch size.

An example on how to adapt your PyTorch code is provided [here](https://github.com/aau-claaudia/aicloud-docs/tree/master/docs/torch_amp_example). The example uses [APEX](https://nvidia.github.io/apex/) automatic multi precision [AMP](https://nvidia.github.io/apex/amp.html) and native [Torch AMP](https://pytorch.org/docs/stable/amp.html) available in NGC from version 20.06.

## PyTorch and automatic mixed precision with APEX

The following is an example of using automatic mixed precision [(AMP)](https://nvidia.github.io/apex/amp.html) for PyTorch with [APEX](https://nvidia.github.io/apex/) and and native [Torch AMP](https://pytorch.org/docs/stable/amp.html) available in NGC from version 20.06. The benefits in general are:

1. Faster computations due to the introduction of half-precision floats and tensor core operations with e.g. V100 GPUs.
2. Larger batch size as the loss, cache and gradients can be saved at a lower precision.

For more information, see the [training neural networks with tensor cores](https://nvlabs.github.io/eccv2020-mixed-precision-tutorial/files/dusan_stosic-training-neural-networks-with-tensor-cores.pdf) which presents two methods for doing AMP that we use below. For more information see also these [videos on mixed precision training](https://developer.nvidia.com/blog/video-mixed-precision-techniques-tensor-cores-deep-learning/).

The following example should be seen as how to approach AMP. The solution to the given problem can be computed more easily using linear least-squares and we use this for validating the results. The example is from the PyTorch [Documentation](https://pytorch.org/tutorials/beginner/pytorch_with_examples.html)


```console
import torch
import numpy as np
from apex import amp


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print('Using device:', device)


def compute(amp_type='None', iterations=5000, verbose=False):
    """
    amt_type:
      'apex': use AMP from the APEX package
      'native': use AMP from the Torch package
      'none': do not use AMP

    """
    
    # Create Tensors to hold input and outputs.
    x = torch.linspace(-np.pi, np.pi, 2000).to(device)
    y = torch.sin(x).to(device)
    
    # Prepare the input tensor (x, x^2, x^3).
    p = torch.tensor([1, 2, 3]).to(device)
    xx = x.unsqueeze(-1).pow(p)

    # Use the nn package to define our model and loss function.
    model = torch.nn.Sequential(
        torch.nn.Linear(3, 1),
        torch.nn.Flatten(0, 1)
    )
    model.to(device)

    loss_fn = torch.nn.MSELoss(reduction='sum')

    # Create optimizer  
    optimizer = torch.optim.RMSprop(model.parameters(), lr=1e-3)

    if amp_type == 'apex':
        # Make model and optimizer AMP models and optimizers
        model, optimizer = amp.initialize(model, optimizer)
    elif amp_type == 'native':
        scaler = torch.cuda.amp.GradScaler()
        
    for t in range(iterations):
        # Forward pass: compute predicted y by passing x to the model.
        if amp_type == 'native':
            with torch.cuda.amp.autocast():
                y_pred = model(xx)
                loss = loss_fn(y_pred, y)
        else:
            y_pred = model(xx)
            loss = loss_fn(y_pred, y)
        
        # Compute and print loss.
        if verbose:
            if t % 100 == 99:
                print("t={:4}, loss={:4}".format(t, loss.item()))

        optimizer.zero_grad()

        # Backward pass: compute gradient of the loss with respect to model
        # parameters using AMP. Substitutes loss.backward() in other models
        if amp_type == 'apex':
            with amp.scale_loss(loss, optimizer) as scaled_loss:
                scaled_loss.backward()
            optimizer.step()
            
        elif amp_type == 'native':
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        elif amp_type == 'none':
            loss.backward()
            optimizer.step()
        else:
            print(f'No such option amp_type={amp_type}')
            raise ValueError

    return model[0], loss.item()


def computeLS():
    x = np.linspace(-np.pi, np.pi, 2000)
    y = np.sin(x)
    p, res, rank, singular_values, rcond = np.polyfit(x, y, deg=3, full=True)
    return p[::-1], res[0]


def display(model_name, loss, p):
    print(f'{model_name}: MSE loss = {loss:.2e}')
    print(f'{model_name}: y = {p[0]:.2e} + {p[1]:.2e} x + {p[2]:.2e} x^2 + {p[3]:.2e} x^3')


without_amp, without_amp_loss = compute(amp_type='none')
with_amp_native, with_amp_native_loss = compute(amp_type='native')
with_amp_apex, with_amp_apex_loss = compute(amp_type='apex')
ls, ls_loss = computeLS()


display("Torch with amp apex  ", with_amp_apex_loss, [with_amp_apex.bias.item(), with_amp_apex.weight[:, 0].item(),
                           with_amp_apex.weight[:, 1].item(), with_amp_apex.weight[:, 2].item()])
display("Torch with amp native", with_amp_native_loss, [with_amp_native.bias.item(), with_amp_native.weight[:, 0].item(),
                           with_amp_native.weight[:, 1].item(), with_amp_native.weight[:, 2].item()])
display("Torch without amp    ", without_amp_loss, [without_amp.bias.item(), without_amp.weight[:, 0].item(),
                           without_amp.weight[:, 1].item(), without_amp.weight[:, 2].item()])
display("LS model             ", ls_loss, ls)
```

Notive the changes at particular parts of the code due to the usage of different AMP approaches (and no AMP)

```console
Using device: cuda:0
Selected optimization level O1:  Insert automatic casts around Pytorch functions and Tensor methods.

Defaults for this optimization level are:
enabled                : True
opt_level              : O1
cast_model_type        : None
patch_torch_functions  : True
keep_batchnorm_fp32    : None
master_weights         : None
loss_scale             : dynamic
Processing user overrides (additional kwargs that are not None)...
After processing overrides, optimization options are:
enabled                : True
opt_level              : O1
cast_model_type        : None
patch_torch_functions  : True
keep_batchnorm_fp32    : None
master_weights         : None
loss_scale             : dynamic
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 32768.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 16384.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 8192.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 4096.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 2048.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 1024.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 512.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 256.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 128.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 64.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 32.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 16.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 8.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 4.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 2.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 1.0
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 0.5
Gradient overflow.  Skipping step, loss scaler 0 reducing loss scale to 0.25
Torch with amp apex  : MSE loss = 8.86e+00
Torch with amp apex  : y = 4.94e-04 + 8.57e-01 x + 4.99e-04 x^2 + -9.37e-02 x^3
Torch with amp native: MSE loss = 8.85e+00
Torch with amp native: y = 4.97e-04 + 8.57e-01 x + 4.98e-04 x^2 + -9.35e-02 x^3
Torch without amp    : MSE loss = 8.92e+00
Torch without amp    : y = 5.00e-04 + 8.57e-01 x + 5.00e-04 x^2 + -9.28e-02 x^3
LS model             : MSE loss = 8.82e+00
LS model             : y = -5.91e-18 + 8.57e-01 x + 0.00e+00 x^2 + -9.33e-02 x^3
```

Notice the final accuracy of Torch with and without AMP methods are comparable, but slightly less accurate than the exact linear least squares solution here used for validation.

It is unclear if we are actually using tensor cores in this example, but now the code is structured such that more advanced NN models can use tensor cores using the above recipe.
