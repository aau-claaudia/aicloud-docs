"""
Example of using Automatic Mixed Precision (AMP) with PyTorch

This example shows the change needed to incorporate AMP in a
PyTorch model. In general the benefits are
1. Faster computations due to the introduction of half-precision
floats and tensor core operations with e.g. V100 GPUs
2. Larger batch size as loss, cache, and gradients can be
saved at a lower precision.

This is just an example of using AMP. The solution can be computed 
more easily using linear least-squares and we use this for 
validating the results.

Tobias Lindstrøm Jensen
Dec 2020
tlj@its.aau.dk

"""


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
