#!/usr/bin/env python3
"""
从 BodyParts3D 开源解剖数据库提取并轻量化本项目所需的 83 个医学 .stl 网格。

用法：
  1. 先克隆 BodyParts3D 仓库：
     git clone --depth 1 https://github.com/Kevin-Mattheus-Moerman/BodyParts3D.git ~/opensrc/anatomy-3d-refs/BodyParts3D
  2. 运行本脚本：
     python3 scripts/prepare_models.py --src ~/opensrc/anatomy-3d-refs/BodyParts3D/assets/BodyParts3D_data/stl --dst ./models
"""

import argparse
import os
import shutil
import struct
import numpy as np

# 直接复制的 80 个轻量化 .stl 网格（FMA / BP ID）
COPY_FILES = [
    # 气道 (3)
    "FMA55099.stl", "FMA7394.stl", "FMA7409.stl",
    # 双肺 5 叶 (5)
    "FMA7333.stl", "FMA7383.stl", "FMA7337.stl", "FMA7370.stl", "FMA7371.stl",
    # 横膈肌 (1)
    "FMA13295.stl",
    # 颈肩辅助/代偿肌群：胸锁乳突肌 + 6 块斜角肌 + 上斜方肌 + 胸小肌 (12)
    "FMA13408.stl", "FMA13409.stl",
    "FMA13392.stl", "FMA13393.stl", "FMA13390.stl", "FMA13391.stl", "FMA13388.stl", "FMA13389.stl",
    "FMA33586.stl", "FMA33587.stl", "FMA13375.stl", "FMA13376.stl",
    # 真实盆底肌群：耻骨尾骨肌、耻骨直肠肌、髂骨尾骨肌、尾骨肌 (8)
    "FMA45854.stl", "FMA45855.stl", "FMA45856.stl", "FMA45857.stl",
    "FMA45858.stl", "FMA45859.stl", "FMA46443.stl", "FMA46444.stl",
    # 胸骨、锁骨、肋软骨 (7)
    "FMA7486.stl", "FMA7487.stl", "FMA7488.stl",
    "FMA13322.stl", "FMA13323.stl", "BP24.stl", "BP28.stl",
    # 第 1~12 对完整肋骨 (24)
    "FMA7857.stl", "FMA7987.stl", "FMA7882.stl", "FMA8012.stl", "FMA7909.stl", "FMA8039.stl",
    "FMA7957.stl", "FMA8148.stl", "FMA8066.stl", "FMA8093.stl", "FMA8175.stl", "FMA8202.stl",
    "FMA8229.stl", "FMA8256.stl", "FMA8283.stl", "FMA8310.stl", "FMA8364.stl", "FMA8391.stl",
    "FMA8445.stl", "FMA8472.stl", "FMA8531.stl", "FMA8532.stl", "FMA8533.stl", "FMA8534.stl",
    # 胸椎 T1-T12 + 腰椎 L1-L5 (17)
    "FMA9165.stl", "FMA9187.stl", "FMA9209.stl", "FMA9248.stl",
    "FMA9922.stl", "FMA9945.stl", "FMA9968.stl", "FMA9991.stl",
    "FMA10014.stl", "FMA10037.stl", "FMA10059.stl", "FMA10081.stl",
    "FMA13072.stl", "FMA13073.stl", "FMA13074.stl", "FMA13075.stl", "FMA13076.stl",
    # 骨盆：骶骨 + 左右髋骨 (3)
    "FMA16202.stl", "FMA16586.stl", "FMA16587.stl",
]

# 原始体积过大（15~40MB）需体素聚类抽稀的 3 个肌肉网格
DECIMATE_FILES = {
    "FMA9756.stl": 2.6,   # 肋间外肌 (40.8MB -> ~4.8MB)
    "FMA22344.stl": 3.2,  # 右侧腹横肌 (15.7MB -> ~1.8MB)
    "FMA22345.stl": 3.2,  # 左侧腹横肌 (15.6MB -> ~1.8MB)
}


def decimate_stl(src_path: str, dst_path: str, voxel_size: float) -> None:
    with open(src_path, "rb") as f:
        header = f.read(80)
        n_tri = struct.unpack("<I", f.read(4))[0]
        dt = np.dtype([("n", "<3f4"), ("v", "<3f4", (3,)), ("attr", "<u2")])
        data = np.frombuffer(f.read(n_tri * 50), dtype=dt)

    verts = data["v"]
    q = np.floor(verts / voxel_size).astype(np.int32)
    keep = (
        np.any(q[:, 0] != q[:, 1], axis=1)
        & np.any(q[:, 1] != q[:, 2], axis=1)
        & np.any(q[:, 2] != q[:, 0], axis=1)
    )
    flat_v = verts[keep].reshape(-1, 3)
    flat_q = q[keep].reshape(-1, 3)

    uniq_q, inv = np.unique(flat_q, axis=0, return_inverse=True)
    sums = np.zeros((len(uniq_q), 3), dtype=np.float64)
    counts = np.bincount(inv)
    np.add.at(sums, inv, flat_v)
    means = (sums / counts[:, None]).astype(np.float32)
    new_v = means[inv].reshape(-1, 3, 3)

    e1 = new_v[:, 1] - new_v[:, 0]
    e2 = new_v[:, 2] - new_v[:, 0]
    norms = np.cross(e1, e2)
    lens = np.linalg.norm(norms, axis=1, keepdims=True)
    valid = lens[:, 0] > 1e-6
    new_v = new_v[valid]
    norms = (norms[valid] / lens[valid]).astype(np.float32)

    out_data = np.zeros(len(new_v), dtype=dt)
    out_data["n"] = norms
    out_data["v"] = new_v
    with open(dst_path, "wb") as f:
        f.write(header)
        f.write(struct.pack("<I", len(new_v)))
        f.write(out_data.tobytes())

    print(
        f"[DECIMATE] {os.path.basename(src_path)}: {n_tri:,} -> {len(new_v):,} tris "
        f"({os.path.getsize(src_path)/1e6:.1f}MB -> {os.path.getsize(dst_path)/1e6:.2f}MB)"
    )


def main():
    parser = argparse.ArgumentParser(description="Extract and decimate BodyParts3D respiratory STLs.")
    parser.add_argument(
        "--src",
        default=os.path.expanduser("~/opensrc/anatomy-3d-refs/BodyParts3D/assets/BodyParts3D_data/stl"),
        help="Path to BodyParts3D_data/stl directory",
    )
    parser.add_argument("--dst", default="./models", help="Output models directory")
    args = parser.parse_args()

    os.makedirs(args.dst, exist_ok=True)
    for fname in COPY_FILES:
        src = os.path.join(args.src, fname)
        dst = os.path.join(args.dst, fname)
        if not os.path.exists(src):
            raise FileNotFoundError(f"Missing STL: {src}")
        shutil.copy2(src, dst)
    print(f"[COPY] Copied {len(COPY_FILES)} STL files to {args.dst}")

    for fname, voxel in DECIMATE_FILES.items():
        decimate_stl(os.path.join(args.src, fname), os.path.join(args.dst, fname), voxel)

    print(f"[DONE] Total {len(COPY_FILES) + len(DECIMATE_FILES)} STL models ready in {args.dst}")


if __name__ == "__main__":
    main()
