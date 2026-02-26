# Understanding: Important Documents

This document summarizes and organizes key information from the important documents related to 6D object pose estimation, point cloud completion, and related pipelines. Some math equations and symbols may not have been captured fully; placeholders are added for clarity.

---

## English_Pipeline.doc

⚠️ Could not read `.doc` due to Windows COM error. Use `pywin32` or Microsoft Word to access content.

---

## English_Pipeline.pdf

**Topic:** 2D planar grasp pipeline

**System Overview:**

- Fig.1: System overview.
- Instance segmentation model:
  - Input: RGB image
  - Output: object category, bounding box, mask
  - Mask example: black area (Fig.2)
  - Suggested methods: MaskRCNN or similar

**Point Cloud Generation:**

1. Object point cloud = RGB + depth + mask + camera intrinsics + camera extrinsics
2. Align depth map to RGB (better for mask accuracy)
3. Compute UV coordinates and depth values for points in the mask (N points)
4. Transform points to camera coordinates → then to world coordinates
5. Denoising required due to segmentation noise (e.g., desktop points)
   - Suggested: radius outlier removal (Open3D)

**Object Pose & Grasp:**

- Position = center of object points
- Pose = rotation about Z-axis, estimated via PCA (first and second principal components)
- Grasp configuration:
  - Center of clamping jaw = object center
  - Approach direction = -Z axis
  - Close direction = second principal component
- Simulation: Vrep

> ⚠️ Math placeholders: center = ?, rotation angle = ?, PCA components = ?

---

## English_Pipeline_v2.docx

Mostly identical to `English_Pipeline.pdf` with updated formatting.

Key improvements:

- Grasp configuration clearly divided into three components
- Notes on partial observation: if only top view, apply displacement along approach direction
- Re-emphasized coordinate system: Z axis is up

> ⚠️ Same placeholders for math/PCA

---

## MaskRCNN_Practice.docx

**Topic:** Instance segmentation training

**Summary:**

- Mask R-CNN: object detection, instance segmentation, keypoint detection
- Key links:
  - Paper: https://arxiv.org/pdf/1703.06870.pdf
  - Tutorial: https://blog.csdn.net/u010901792/article/details/100044200

**Data Annotation:**

- Use `labelme` tool
- Save JSON annotations in same folder as images
- Notes on group IDs and class naming

**Training:**

- Use cloud disk scripts (`train_28classes_1225.py`)
- Modify labels to match dataset
- Pretrained models provided for faster training

---

## Point_Cloud_Completion.docx

**Topic:** PCN – Point Completion Network

**Network Overview:**

- Input: Partial point clouds
- Output: Complete point clouds
- Architecture: Two stacked PointNet networks → extract latent vectors → MLP → coarse point cloud → Folding-based upsampling for fine details

**Datasets:**

1. Synthetic: ShapeNet → generate partial clouds from depth maps
   - Variants: ShapeNet-34, ShapeNet-55
2. Real: KITTI → LiDAR scans
   - No complete labels
   - Some papers validate using ShapeNet “car” category

---

## Point_Cloud_Completion_Project.zip

**Authors:** Wentao Yuan, Tejas Khot, David Held, Christoph Mertz, Martial Hebert (CMU)

**Summary:**

- PCN operates directly on raw point clouds (no symmetry/semantic assumptions)
- Encoder-decoder network for shape completion
- Handles various levels of incompleteness and noise
- Dense completions while keeping parameter count low
- Data & code: https://wentaoyuan.github.io/pcn

**Challenges:**

- Incomplete real-world 3D data
- High memory usage of voxelized methods
- Loss of fine geometric details

---

## Point_Cloud_Completion_v2.docx

Mostly same as `.docx` above with minor updates:

- Clearer description of synthetic vs real datasets
- Emphasizes ability to generate your own dataset
- Mentions other related datasets: YCB, ShapeNet variations

---

## Notes / To-Do

1. Fill in missing equations and PCA math from `English_Pipeline.pdf` / `v2.docx`
2. Consider adding images or diagrams from `07_concept_images` corresponding to each figure referenced (Fig.1, Fig.2, etc.)
3. Keep cross-references for PCA, MaskRCNN, and PCN for easier reading
4. Add links to scripts for preprocessing / training wherever referenced

---
