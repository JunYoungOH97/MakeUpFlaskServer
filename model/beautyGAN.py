import os
import cv2
import numpy as np

import torch
from torchvision.utils import save_image
from torchvision import transforms

from model.net import Generator_branch
from model.makeup import MAKEUP


class beautyGAN:
    def __init__(self, source, target):
        self.e = 185
        self.i = 1260
        self.test_model = f"{self.e}_{self.i}"
        self.snapshot_path = "./model/model_state"

        self.img_size = 256

        self.result_path = "./model/result"
        if(not os.path.isdir(self.result_path)):
            os.mkdir(self.result_path)

        self.G = Generator_branch(64, 6)

        if(torch.cuda.is_available()):
            self.G.cuda()

        transform = transforms.Compose([transforms.Resize((self.img_size, self.img_size)),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])])

        self.dataset_test = MAKEUP(transform=transform, source = source, target = target)

    def test(self):
        G_path = os.path.join(self.snapshot_path, '{}_G.pth'.format(self.test_model))
        self.G.load_state_dict(torch.load(G_path))
        self.G.eval()
        
        img_A, img_B = self.dataset_test.get_item()

        real_org = self.to_var(img_A)
        real_ref = self.to_var(img_B)

        fake_A, _ = self.G(real_org, real_ref)

        result = self.de_norm(fake_A)

        # save_path_0 = os.path.join("./result", "result.png")
        # save_image(result, save_path_0, nrow=1, padding=0, normalize=True)
        
        result = result.detach().cpu()
        result = torch.squeeze(result, axis=0)
        result = result.numpy().transpose((1, 2, 0))
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result = result * 255
        cv2.imwrite("./test.png", result)

        result = cv2.imencode('.png', result)[1].tostring()

        return result


    def de_norm(self, x):
        out = (x + 1) / 2
        return out.clamp(0, 1)

    def to_var(self, x):
        x = x.unsqueeze(0)
        if torch.cuda.is_available():
            return x.to("cuda:0")
        return x
