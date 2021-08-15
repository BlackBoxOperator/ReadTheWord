""" Quick n Simple Image Folder, Tarfile based DataSet

Hacked together by / Copyright 2020 Ross Wightman
"""
import torch.utils.data as data
import os
import torch
import logging

from PIL import Image

_logger = logging.getLogger(__name__)


_ERROR_RETRY = 50

# input a list of PIL image
class PILDataset(data.Dataset):

    def __init__(
            self,
            images,
            parser=None,
            class_map='',
            load_bytes=False,
            transform=None,
    ):

        self.images = images
        self.load_bytes = load_bytes
        self.transform = transform
        self._consecutive_errors = 0

    def __getitem__(self, index):
        img, target = self.images[index], None
        try:
            if self.load_bytes:
                img = img.read()
            elif isinstance(img, str):
                img = Image.open(img).convert('RGB')
        except Exception as e:
            _logger.warning(f'Skipped sample (index {index}, file of PIL). {str(e)}')
            self._consecutive_errors += 1
            if self._consecutive_errors < _ERROR_RETRY:
                return self.__getitem__((index + 1) % len(self.images))
            else:
                raise e
        self._consecutive_errors = 0
        if self.transform is not None:
            img = self.transform(img)
        if target is None:
            target = torch.tensor(-1, dtype=torch.long)
        return img, target

    def __len__(self):
        return len(self.images)

    def filename(self, index, basename=False, absolute=False):
        return f'{index}.image'

    def filenames(self, basename=False, absolute=False):
        return [f'{index}.image' for index in range(len(self.images))]
