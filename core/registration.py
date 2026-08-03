# This Python file uses the following encoding: utf-8
import SimpleITK as sitk
import os
from picsl_greedy import Greedy3D
import numpy as np
import ants

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
        self.coarsest = coarest_options[self.LoadMRI.coarsest_index] #comboBox_coarsest
        self.finest = finest_options[self.LoadMRI.finest_index] #comboBox_finest
        dbg(f"[REG] calling rigid_transformation  coarsest={self.coarsest} finest={self.finest}")
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
            Perform rigid registration of the moving image to the fixed image.
            1. Rgid trasnformation with NMI
            2. Rigid trasnformation with MI (takes the 1. matrix as initialisation)
        """

        g = Greedy3D()

        base_iters = 100
        img_size = self.fixed_image.GetSize()
        min_size = min(img_size)
        threshold = min_size // 3
        factors = []
        f = self.coarsest
        while f >= self.finest:
            min_dim = min(s // f for s in img_size)
            if min_dim >= threshold:
                factors.append(f)
            if f == self.finest:
                break
            f = f // 2
        if not factors:
            factors = [self.finest]  # always keep at least the finest level
        n_string = "x".join(str(base_iters * factor) for factor in factors)
        print(n_string,flush=True)

        fixed = self.fixed_image
        moving = self.moving_image
        if fixed.GetNumberOfComponentsPerPixel() > 1:
            fixed = sitk.VectorIndexSelectionCast(fixed, 0)
        if moving.GetNumberOfComponentsPerPixel() > 1:
            moving = sitk.VectorIndexSelectionCast(moving, 0)
        fixed = sitk.Cast(fixed, sitk.sitkFloat32)
        moving = sitk.Cast(moving, sitk.sitkFloat32)
        fixed = sitk.RescaleIntensity(fixed, 0.0, 1.0)
        moving = sitk.RescaleIntensity(moving, 0.0, 1.0)

        #g.execute('-i my_fixed my_moving '
        #          '-a -dof 6 -m NMI '           ##NMI
        #           f'-n {n_string} '
        #           '-ia-identity '
        #          '-V 0 ' #no verbose
        #          '-o my_ncc',
        #          my_fixed = fixed, my_moving = moving,
        #          my_ncc=None)
        #g.execute('-i my_fixed my_moving '
        #    '-a -dof 6 -m NMI '
        #    f'-n {n_string} '
        #    #f'-ia {identity_path} '  # initialize from identity, RAS convention
        #    '-V 0 '
        #    '-o my_rigid',
        #    my_fixed=fixed,
        #    my_moving=moving,
        #    my_rigid=None
        #  )
        #g.execute(
        #    '-i my_fixed my_moving '
        #    '-a -dof 6 -m MI '
        #    f'-n {n_string} '
        #    '-ia-identity '
        #    '-V 0 '
        #    #f'-ia my_ncc '
        #    '-o my_rigid',
        #    my_fixed=fixed,
        #    my_moving=moving,
        #    my_rigid=None
        #)

        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            fixed_path  = os.path.join(tmpdir, 'fixed.nii.gz')
            moving_path = os.path.join(tmpdir, 'moving.nii.gz')
            nmi_mat     = os.path.join(tmpdir, 'nmi.mat')
            rigid_mat   = os.path.join(tmpdir, 'rigid.mat')

            sitk.WriteImage(fixed,  fixed_path)
            sitk.WriteImage(moving, moving_path)

            # NMI pass: single finest-resolution level only — at coarse scales the
            # misalignment is sub-voxel and the gradient is zero, causing lbfgs to
            # diverge on restart and corrupt the initialisation for finer levels.
            g.execute(
                f'-i {fixed_path} {moving_path} '
                '-a -dof 6 -m NMI '
                '-n 100 '
                '-ia-identity '
                f'-o {nmi_mat}',
            )
            # MI refinement pass: finest level only — coarser levels have near-zero
            # gradient for nearly-aligned images and trigger lbfgs random restarts
            # that corrupt the rotation. Only the finest level refines cleanly.
            g.execute(
                f'-i {fixed_path} {moving_path} '
                '-a -dof 6 -m MI '
                f'-n {n_string} '
                f'-ia {nmi_mat} '
                f'-o {rigid_mat}',
            )

            mat_rigid = np.loadtxt(rigid_mat)

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

        return

        ## --- ANTs (slow on large images, kept for reference) ---
        #import logging
        #logging.info(f"Registration started: {self.moving_filepath} → {self.LoadMRI.volumes[0].file_path}")
        #logging.info(f"  shrink_factors={shrink_factors}  smoothing_sigmas={smoothing_sigmas}  iterations={aff_iterations}")
        #fixed_ants = ants.image_read(self.LoadMRI.volumes[0].file_path)
        #moving_ants = ants.image_read(self.moving_filepath)
        #reg = ants.registration(
        #    fixed=fixed_ants,
        #    moving=moving_ants,
        #    type_of_transform="Rigid",
        #    aff_iterations=aff_iterations,
        #    aff_shrink_factors=shrink_factors,
        #    aff_smoothing_sigmas=smoothing_sigmas,
        #    verbose=1,
        #)
        #logging.info("Registration finished.")
        #print('ants ',reg["fwdtransforms"][0])
        #tx = ants.read_transform(reg["fwdtransforms"][0])
        #params = tx.parameters
        #fixed_params = tx.fixed_parameters
        #with open(output_path, "w") as f:
        #    f.write("#Insight Transform File V1.0\n")
        #    f.write("#Transform 0\n")
        #    f.write("Transform: MatrixOffsetTransformBase_double_3_3\n")
        #    f.write("Parameters: " + " ".join(f"{p:.12f}" for p in params) + "\n")
        #    f.write("FixedParameters: " + " ".join(f"{p:.12f}" for p in fixed_params) + "\n")
        ## --- end ANTs ---

        import sys
        def dbg(msg):
            print(msg, file=sys.__stderr__, flush=True)

        #fixed  = sitk.Cast(self.fixed_image,  sitk.sitkFloat32)
        #moving = sitk.Cast(self.moving_image, sitk.sitkFloat32)
        fixed_img  = self.fixed_image
        moving_img = self.moving_image
        if fixed_img.GetNumberOfComponentsPerPixel() > 1:
            fixed_img = sitk.VectorIndexSelectionCast(fixed_img, 0)
        if moving_img.GetNumberOfComponentsPerPixel() > 1:
            moving_img = sitk.VectorIndexSelectionCast(moving_img, 0)
        fixed  = sitk.Cast(fixed_img,  sitk.sitkFloat32)
        moving = sitk.Cast(moving_img, sitk.sitkFloat32)

        initial_transform = sitk.Euler3DTransform()

        reg = sitk.ImageRegistrationMethod()
        reg.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
        reg.SetOptimizerAsGradientDescent(
            learningRate=1.0,
            numberOfIterations=iterations_per_level,
            convergenceMinimumValue=1e-6,
            convergenceWindowSize=10,
        )
        reg.SetOptimizerScalesFromPhysicalShift()
        reg.SetShrinkFactorsPerLevel(shrinkFactors=list(shrink_factors))
        reg.SetSmoothingSigmasPerLevel(smoothingSigmas=list(smoothing_sigmas))
        reg.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
        reg.SetInitialTransform(initial_transform, inPlace=False)
        reg.SetInterpolator(sitk.sitkLinear)

        transform = reg.Execute(fixed, moving)
        dbg(f"[REG] Done — {reg.GetOptimizerStopConditionDescription()}")
        dbg(f"[REG] Metric={reg.GetMetricValue():.6f}  Iterations={reg.GetOptimizerIteration()}")

        # Convert Euler3DTransform result to MatrixOffsetTransformBase_double_3_3 format
        # (same format as ANTs output — downstream code expects 9 rotation + 3 translation, center at origin)
        try:
            inner = sitk.Euler3DTransform(sitk.CompositeTransform(transform).GetNthTransform(0))
        except Exception:
            inner = sitk.Euler3DTransform(transform)
        R = np.array(inner.GetMatrix()).reshape(3, 3)
        c = np.array(inner.GetCenter())
        t = np.array(inner.GetTranslation())
        offset = (np.eye(3) - R) @ c + t   # re-centre at origin
        params_str = " ".join(f"{v:.18f}" for v in list(R.flatten()) + list(offset))
        with open(output_path, "w") as fh:
            fh.write("#Insight Transform File V1.0\n")
            fh.write("#Transform 0\n")
            fh.write("Transform: MatrixOffsetTransformBase_double_3_3\n")
            fh.write(f"Parameters: {params_str}\n")
            fh.write("FixedParameters: 0 0 0\n")
        dbg(f"[REG] Transform saved: {output_path}")

        return


