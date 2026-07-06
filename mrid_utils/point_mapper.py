import SimpleITK as sitk
import os
import numpy as np

def find_moving_img(registerpath):
    swarp_path = os.path.join(registerpath, "s_warp")
    movingImgName = ""
    if os.path.exists(swarp_path):
        files = os.listdir(swarp_path)
        for file in files:
            if file.startswith("sub-") and file.endswith(".nii.gz"):
                movingImgName = file.split(".")[0]
                movingImgName = movingImgName + "_resampled.nii.gz"

    return movingImgName


def load_transform(path):
    try:
        transform_moving2fixed = sitk.ReadTransform(path)
        print("Succesfully loaded transform: " + path.split("/")[-1])
    except:
        print("error loading the transform file")

    return transform_moving2fixed


def load_sitkimage(path):
    try:
        sitkImg = sitk.ReadImage(path)  # Moving image
        print("Succesfully loaded sitk img: " + path.split("/")[-1])
    except:
        print("error loading the sitk img file" + path.split("/")[-1])

    return sitkImg


def map_coordinates(fixedImg, movingImg, transform_moving2fixed):
    nx, ny, nz = fixedImg.GetSize()

    moving_coordinates = np.empty((nx * ny * nz, 3))
    fixed_coordinates = np.empty((nx * ny * nz, 3))

    i = 0
    for x in range(nx):
        if x % 10 == 0:
            print("Progress: " + str(x) + "/" + str(nx))
        for y in range(ny):
            for z in range(nz):
                idx = [x, y, z]
                fixedpnt = fixedImg.TransformIndexToPhysicalPoint(idx)
                movingpnt = transform_moving2fixed.TransformPoint(fixedpnt) #mri world frame
                movingidx = movingImg.TransformPhysicalPointToIndex(movingpnt)
                fixed_coordinates[i, :] = idx
                moving_coordinates[i, :] = movingidx
                i = i + 1

    return moving_coordinates, fixed_coordinates
