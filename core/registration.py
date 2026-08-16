# This Python file uses the following encoding: utf-8
import SimpleITK as sitk
import os
import math
import numpy as np
from file_handling.itksnap_registration import register_rigid

class Registration:
    """
       Perform rigid registration of a moving MRI image to a fixed MRI image.

       This class uses SimpleITK to perform a rigid registration (Euler 3D transform)
       and saves the resulting transform both as a rigid transform and an affine-style transform.

       Parameters
       ----------
       LoadMRI : object
           The main MRI loader object that contains session information,
           paths, and image file selections.
    """
    def __init__(self,LoadMRI,buttonsgui_3d,index):
        """
            Initialize the Registration object and perform rigid registration.
        """
        self.LoadMRI = LoadMRI

        filename = self.LoadMRI.movingimg_filename[index] #self.LoadMRI.combo_Regimgname.itemText(0)
        folder = f"{self.LoadMRI.session_path}/anat"

        file_part = self.LoadMRI.volumes[0].file_path.split("ind_")[1]  # e.g., '0-resampled100um.nii'
        number_str = ""
        for c in file_part:
            if c.isdigit():
                number_str += c
            else:
                break  # stop at first non-digit
        self.fixed_ind = int(number_str)
        moving_file_part = filename.split("ind_")[1]
        moving_number_str = ""
        for c in moving_file_part:
            if c.isdigit():
                moving_number_str += c
            else:
                break
        self.moving_ind = int(moving_number_str)

        import sys
        def dbg(msg):
            print(msg, file=sys.__stderr__, flush=True)

        dbg(f"[REG] reading fixed: {self.LoadMRI.volumes[0].file_path}")
        self.fixed_image = sitk.ReadImage(self.LoadMRI.volumes[0].file_path)
        dbg("[REG] fixed read ok")
        self.moving_filepath = os.path.join(folder, filename)
        dbg(f"[REG] reading moving: {self.moving_filepath}")
        self.moving_image = sitk.ReadImage(self.moving_filepath)
        dbg("[REG] moving read ok — orienting...")
        self.moving_image = sitk.DICOMOrient(self.moving_image, 'RAS')
        self.fixed_image = sitk.DICOMOrient(self.fixed_image, 'RAS')
        dbg("[REG] orientation done")
        dbg(f"[REG] fixed  origin (RAS): {self.fixed_image.GetOrigin()}")
        dbg(f"[REG] moving origin (RAS): {self.moving_image.GetOrigin()}")
        fo = self.fixed_image.GetOrigin()
        mo = self.moving_image.GetOrigin()
        dbg(f"[REG] moving-fixed origin diff (RAS): {tuple(m-f for m,f in zip(mo,fo))}")

        if len(self.moving_image.GetSize())==4:
            self.moving_image = self.get3Dimage(self.moving_image)

        coarest_options = [8,4,2,1]
        finest_options = [1,2,4]
        metric_options = ["NMI","NCC","SSD"]
        self.coarsest = coarest_options[self.LoadMRI.coarsest_index] #comboBox_coarsest
        self.finest = finest_options[self.LoadMRI.finest_index] #comboBox_finest
        # trajectory_planning/registration.py calls Registration() directly without
        # going through initialize_registration(), so metric_index may not be set.
        self.metric = metric_options[getattr(self.LoadMRI, "metric_index", 0)] #comboBox_regitstration_metric
        dbg(f"[REG] calling rigid_transformation  coarsest={self.coarsest} finest={self.finest} metric={self.metric}")
        self.rigid_transformation()




    def get3Dimage(self,img):
        """
            Extract a single 3D volume from a 4D image.

            Parameters
            ----------
            img : SimpleITK.Image
                A 4D image where the last dimension represents time or frames.
        """
        t_index = 0
        size = list(img.GetSize())
        img3d = sitk.Extract(img, size[:3] + [0], [0, 0, 0, t_index])

        return img3d


    def rigid_transformation(self):
        """
            Perform rigid registration of the moving image to the fixed image,
            reproducing exactly what ITK-SNAP's "Registration" panel does
            (see file_handling/itksnap_registration.py for the full rationale).
        """

        fixed = self.fixed_image
        moving = self.moving_image
        if fixed.GetNumberOfComponentsPerPixel() > 1:
            fixed = sitk.VectorIndexSelectionCast(fixed, 0)
        if moving.GetNumberOfComponentsPerPixel() > 1:
            moving = sitk.VectorIndexSelectionCast(moving, 0)

        # self.coarsest/self.finest are shrink FACTORS (8,4,2,1 / 1,2,4), while
        # register_rigid expects pyramid LEVELS (level k -> shrink factor 2**k).
        coarsest_level = int(math.log2(self.coarsest))
        finest_level = int(math.log2(self.finest))

        result = register_rigid(
            fixed,
            moving,
            metric=self.metric,
            coarsest_level=coarsest_level,
            finest_level=finest_level,
            # search_iterations left at 0 (off): a wide random-restart search
            # actively found a worse, anatomically-wrong optimum that NMI
            # nonetheless scored better than the true near-identity alignment
            # -- confirmed empirically on this data. register_rigid()'s default
            # identity init now dodges greedy's forced jitter deterministically
            # instead (see its docstring), avoiding the corruption without
            # gambling on a broad search.
            verbose=True,
        )
        mat_rigid = result.matrix_ras

        transform_filename = f"transformation-ind_{self.moving_ind}-to-ind_{self.fixed_ind}.txt"
        output_path = os.path.join(self.LoadMRI.session_path, "anat", transform_filename)

        np.set_printoptions(precision=12, suppress=False)

        RAS2LPS = np.diag([-1, -1, 1, 1])
        mat_end = RAS2LPS @ mat_rigid @ RAS2LPS

        with open(output_path, "w") as f:
            f.write("#Insight Transform File V1.0\n")
            f.write("#Transform 0\n")
            f.write("Transform: MatrixOffsetTransformBase_double_3_3\n")
            f.write("Parameters: ")

            # 9 rotation + 3 translation = 12 parameters
            np.savetxt(f, mat_end[:3, :3].reshape(1, 9), fmt="%.12f", newline=" ")
            f.write(" ")
            np.savetxt(f, mat_end[:3, 3].reshape(1, 3), fmt="%.12f", newline=" ")
            f.write("\nFixedParameters: 0 0 0\n")


