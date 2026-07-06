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
    view_names: list
    array_4d: np.ndarray | None = None
    spacing: tuple = ()
    oriented_ref_image: object = None  # sitk.Image
    raw_ref_image: object = None  # sitk.Image
    is_4d: bool = False
    timestamp4D: list = field(default_factory=list)

    @classmethod
    def from_file(cls, file_path: str,DICOMOrient = "RAS",view_name=None) -> "MRIVolume":
        image_raw = sitk.ReadImage(file_path)
        array_raw = sitk.GetArrayFromImage(image_raw)
        nib_img = nib.load(file_path)
        raw_DICOMOrient = nib.aff2axcodes(nib_img.affine)
        raw_DICOMOrient = "".join(raw_DICOMOrient)

        is_4d = array_raw.ndim == 4

        array_4d = None
        timestamp4D = []
        view_names = []
        if is_4d:
            size = list(image_raw.GetSize())
            size[3] = 0
            volumes = []
            for t in range(image_raw.GetSize()[3]):
                if view_name=='coronal' or view_name=="axial":
                    DICOMOrient = "RSA"
                elif view_name=='sagittal':
                    DICOMOrient = "ASR"
                image = sitk.DICOMOrient(image_raw[:, :, :, t], DICOMOrient)
                volumes.append(sitk.GetArrayFromImage(image))
            array_4d = np.stack(volumes)
            timestamp4D = [0, 4, 7] if array_4d.shape[0] > 7 else [0, 2, 5]
            slices = {
                    0: array_4d[timestamp4D[0], :, :, :].copy(),
                    1: array_4d[timestamp4D[1], :, :, :].copy(),
                    2: array_4d[timestamp4D[2], :, :, :].copy(),
                }
            view_names = [view_name]
        else:
            image = sitk.DICOMOrient(image_raw, DICOMOrient)
            vol = sitk.GetArrayFromImage(image)
            slices = {0: vol}
            view_names = ['axial','coronal','sagittal']

        spacing = image.GetSpacing()[::-1]

        return cls(
            file_path=file_path,
            slices=slices,
            raw_ref_image=image_raw,
            oriented_ref_image=image,
            is_4d=is_4d,
            spacing=spacing,
            array_4d=array_4d,
            timestamp4D = timestamp4D,
            DICOMOrient=DICOMOrient,
            raw_DICOMOrient=raw_DICOMOrient,
            view_names=view_names,
        )


