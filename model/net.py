import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    """Residual Block."""
    def __init__(self, dim_in, dim_out):
        super(ResidualBlock, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(dim_in, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(dim_out, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True))

    def forward(self, x):
        return x + self.main(x)

class Generator_branch(nn.Module):
    """Generator. Encoder-Decoder Architecture."""
    # input 2 images and output 2 images as well
    def __init__(self, conv_dim=64, repeat_num=6, input_nc=3):
        super(Generator_branch, self).__init__()

        # Branch input
        layers_branch = []
        layers_branch.append(nn.Conv2d(input_nc, conv_dim, kernel_size=7, stride=1, padding=3, bias=False))
        layers_branch.append(nn.InstanceNorm2d(conv_dim, affine=True))
        layers_branch.append(nn.ReLU(inplace=True))
        layers_branch.append(nn.Conv2d(conv_dim, conv_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
        layers_branch.append(nn.InstanceNorm2d(conv_dim*2, affine=True))
        layers_branch.append(nn.ReLU(inplace=True))
        self.Branch_0 = nn.Sequential(*layers_branch)

        # Branch input
        layers_branch = []
        layers_branch.append(nn.Conv2d(input_nc, conv_dim, kernel_size=7, stride=1, padding=3, bias=False))
        layers_branch.append(nn.InstanceNorm2d(conv_dim, affine=True))
        layers_branch.append(nn.ReLU(inplace=True))
        layers_branch.append(nn.Conv2d(conv_dim, conv_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
        layers_branch.append(nn.InstanceNorm2d(conv_dim*2, affine=True))
        layers_branch.append(nn.ReLU(inplace=True))
        self.Branch_1 = nn.Sequential(*layers_branch)

        # Down-Sampling, branch merge
        layers = []
        curr_dim = conv_dim*2
        layers.append(nn.Conv2d(curr_dim*2, curr_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
        layers.append(nn.InstanceNorm2d(curr_dim*2, affine=True))
        layers.append(nn.ReLU(inplace=True))
        curr_dim = curr_dim * 2
     
        # Bottleneck
        for i in range(repeat_num):
            layers.append(ResidualBlock(dim_in=curr_dim, dim_out=curr_dim))

        # Up-Sampling
        for i in range(2):
            layers.append(nn.ConvTranspose2d(curr_dim, curr_dim//2, kernel_size=4, stride=2, padding=1, bias=False))
            layers.append(nn.InstanceNorm2d(curr_dim//2, affine=True))
            layers.append(nn.ReLU(inplace=True))
            curr_dim = curr_dim // 2

        self.main = nn.Sequential(*layers)

        layers_1 = []
        layers_1.append(nn.Conv2d(curr_dim, curr_dim, kernel_size=3, stride=1, padding=1, bias=False))
        layers_1.append(nn.InstanceNorm2d(curr_dim, affine=True))
        layers_1.append(nn.ReLU(inplace=True))
        layers_1.append(nn.Conv2d(curr_dim, curr_dim, kernel_size=3, stride=1, padding=1, bias=False))
        layers_1.append(nn.InstanceNorm2d(curr_dim, affine=True))
        layers_1.append(nn.ReLU(inplace=True))
        layers_1.append(nn.Conv2d(curr_dim, 3, kernel_size=7, stride=1, padding=3, bias=False))
        layers_1.append(nn.Tanh())
        self.branch_1 = nn.Sequential(*layers_1)
        layers_2 = []
        layers_2.append(nn.Conv2d(curr_dim, curr_dim, kernel_size=3, stride=1, padding=1, bias=False))
        layers_2.append(nn.InstanceNorm2d(curr_dim, affine=True))
        layers_2.append(nn.ReLU(inplace=True))
        layers_2.append(nn.Conv2d(curr_dim, curr_dim, kernel_size=3, stride=1, padding=1, bias=False))
        layers_2.append(nn.InstanceNorm2d(curr_dim, affine=True))
        layers_2.append(nn.ReLU(inplace=True))
        layers_2.append(nn.Conv2d(curr_dim, 3, kernel_size=7, stride=1, padding=3, bias=False))
        layers_2.append(nn.Tanh())
        self.branch_2 = nn.Sequential(*layers_2)

    def forward(self, x, y):
        input_x = self.Branch_0(x)
        input_y = self.Branch_1(y)
        input_fuse = torch.cat((input_x, input_y), dim=1)
        out = self.main(input_fuse)
        out_A = self.branch_1(out)
        out_B = self.branch_2(out)
        return out_A, out_B
