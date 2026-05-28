# This Python file uses the following encoding: utf-8
from dataclasses import dataclass, field
import numpy as np
import SimpleITK as sitk
import nibabel as nib

@dataclass
class MRIVolume:
    file_path: str
    slices: dict
    DICOMOrient: str
    raw_DICOMOrient: str
    array_4d: np.ndarray | None = None
    spacing: tuple = ()
    ref_image: object = None  # sitk.Image
    is_4d: bool = False
    timestamp4D: list = field(default_factory=list)



    @classmethod
    def from_file(cls, file_path: str) -> "MRIVolume":
        image_raw = sitk.ReadImage(file_path)
        array_raw = sitk.GetArrayFromImage(image_raw)
        nib_img = nib.load(file_path)
        raw_DICOMOrient = nib.aff2axcodes(nib_img.affine)

        is_4d = array_raw.ndim == 4

        array_4d = None
        timestamp4D = []
        if is_4d:
            size = list(image_raw.GetSize())
            size[3] = 0
            volumes = []
            for t in range(image_raw.GetSize()[3]):
                image = sitk.DICOMOrient(image_raw[:, :, :, t], "LSA")
                DICOMOrient = "LAS"
                a, b, c = sitk.GetArrayFromImage(image).shape
                if a < c:
                    volumes.append(sitk.GetArrayFromImage(image))
                else:
                    image = sitk.DICOMOrient(image_raw[:, :, :, t], "SAL")
                    volumes.append(sitk.GetArrayFromImage(image))
                    DICOMOrient = "SAL"
            array_4d = np.stack(volumes)
            timestamp4D = [0, 4, 7] if array_4d.shape[0] > 7 else [0, 2, 5]
            slices = {
                    0: array_4d[timestamp4D[0], :, :, :].copy(),
                    1: array_4d[timestamp4D[1], :, :, :].copy(),
                    2: array_4d[timestamp4D[2], :, :, :].copy(),
                }
        else:
            DICOMOrient = "LAS"
            image = sitk.DICOMOrient(image_raw, DICOMOrient)
            vol = sitk.GetArrayFromImage(image)
            slices = {0: vol} #, 1: vol, 2: vol}

        spacing = image.GetSpacing()[::-1]


        return cls(
            file_path=file_path,
            slices=slices,
            ref_image=image,
            is_4d=is_4d,
            #axes_to_flip=[False,False,False],
            spacing=spacing,
            array_4d=array_4d,
            timestamp4D = timestamp4D,
            DICOMOrient=DICOMOrient,
            raw_DICOMOrient=raw_DICOMOrient
        )


