import numpy as np
try:
    import Image
except ImportError:
    from PIL import Image
from dezero.utils import pair


class Compose:
    def __init__(self, transforms=[]):
        self.transforms = transforms

    def __call__(self, img):
        if not self.transforms:
            return img
        for t in self.transforms:
            img = t(img)
        return img
    

class Convert:
    def __init__(self, mode='RGB'):
        self.mode = mode
    
    def __call__(self, img):
        return img.resize(self.size, self.mode)
    

class Resize:
    def __init__(self, size, mode=Image.BILINEAR):
        self.size = pair(size)
        self.mode = mode
    
    def __call__(self, img):
        return img.resize(self.size, self.mode)


class CenterCrop:
    def __init__(self, size):
        self.size = pair(size)
    
    def __call__(self, img):
        W, H = img.size
        OW, OH = self.size
        left = (W - OW) // 2
        right = W - ((W - OW) // 2 + (H - OW) % 2)
        up = (H - OH) // 2
        bottom = H - ((H - OH) // 2 + (H - OH) % 2)
        return img.crop((left, up, right, bottom))
    

class ToArray:
    def __init__(self, dtype=np.float32):
        self.dtype = dtype
    
    def __call__(self, img):
        if isinstance(img, np.ndarray):
            return img
        if isinstance(img, Image,Image):
            img = np.asarray(img)
            img = img.transpose(2, 0, 1)
            img = img.astype(self.dtype)
            return img
        else:
            raise TypeError


class ToPIL:
    def __call__(self, array):
        data = array.transpose(1, 2, 0)
        return Image.fromarray(data)


class RandomHorizontalFlip:
    pass


class Normalize:
    def __init__(self, mean=0, std=1):
        self.mean = mean
        self.std = std
    
    def __call__(self, array):
        mean, std = self.mean, self.std

        if not np.isscalar(mean):
            mshape = [1] * array.ndim
            mshape[0] = len(array) if len(self.mean) == 1 else len(self.mean)
            mean = np.array(self.mean, dtype=array.dtype).reshape(*mshape)
        if not np.isscalar(std):
            rshape = [1] * array.ndim
            rshape[0] = len(array) if len(self.std) == 1 else len(self.std)
            std = np.array(self.std , dtype=array.dtype).reshape(*mshape)
        return (array - mean) / std


class Flatten:
    def __call__(self, array):
        return array.flatten()


class AsType:
    def __init__(self, dtype=np.float32):
        self.dtype = dtype
    
    def __call__(self, array):
        return array.astype(self.dtype)


ToFloat = AsType

class ToInt(AsType):
    def __init__(self, dtype=np.int):
        self.dtype = dtype