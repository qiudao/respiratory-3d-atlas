# Open Respiratory & Core 3D Atlas

基于 **Three.js** 与 **BodyParts3D** 真实医学网格（83 个 `.stl` 解剖模型）构建的交互式 3D 呼吸系统与核心发力可视化平台，完整复现**腹式呼吸 / 360° 胸腹联合呼吸 / 胸式呼吸 / 颈部代偿呼吸**的肌肉募集与生物力学机制。

## 在线预览（GitHub Pages）
* **3D 呼吸与核心发力图谱**：https://qiudao.github.io/respiratory-3d-atlas/

---

## 一、快速本地运行（开箱即用）

本仓库已包含抽稀优化后的全部 83 个 `.stl` 模型，克隆后直接起一个静态 HTTP 服务即可运行（浏览器禁止 `file://` 直接 `fetch` 本地 `.stl`）：

```bash
git clone https://github.com/qiudao/respiratory-3d-atlas.git
cd respiratory-3d-atlas
python3 -m http.server 8765
# 浏览器打开 http://localhost:8765/
```

---

## 二、前端依赖与架构说明

- **渲染引擎**：`three@0.147.0`（通过 jsDelivr CDN 加载，无需 npm 构建）
  - `https://cdn.jsdelivr.net/npm/three@0.147.0/build/three.min.js`
  - `https://cdn.jsdelivr.net/npm/three@0.147.0/examples/js/controls/OrbitControls.js`
  - `https://cdn.jsdelivr.net/npm/three@0.147.0/examples/js/loaders/STLLoader.js`
- **坐标系说明**：BodyParts3D 原始坐标单位为毫米（mm）且为 `Z-up`（`-Y` 朝前、`+Z` 朝上），在 `index.html` 中通过 `anatomyRoot.rotation.x = -Math.PI / 2` 转换为 Three.js `Y-up` 坐标系并自动居中。
- **核心交互模块**：
  - 4 种呼吸模式生物力学仿真（`腹式` / `360° 胸腹联合` / `胸式` / `颈部代偿`）
  - 分区骨骼运动（第 1~2 肋与锁骨耸肩上提 / 第 3~6 肋与胸骨泵柄运动 / 第 7~12 肋桶柄外展）
  - 模拟表面肌电（EMG）激活热力色 + 动态 3D 发力矢量箭头（`THREE.ArrowHelper`）
  - 冠状面 3D 剖面切片（`THREE.Plane` 局部裁剪）+ X-Ray 气道透视 + 3D 气道气流粒子 + 实时三通道生理示波器

---

## 三、完整上游开源参考库（一键复原研发环境）

如果以后需要扩充更多器官（如心脏、腹内外斜肌、多裂肌、膈神经等）或参考完整的开源 3D 解剖架构，按以下命令即可一键还原全部参考仓库：

```bash
mkdir -p ~/opensrc/anatomy-3d-refs && cd ~/opensrc/anatomy-3d-refs
git clone --depth 1 https://github.com/Kevin-Mattheus-Moerman/BodyParts3D.git BodyParts3D
git clone --depth 1 https://github.com/Z-Anatomy/Models-of-human-anatomy.git Z-Anatomy-Models
git clone --depth 1 https://github.com/LluisV/Z-Anatomy.git Z-Anatomy-App
git clone --depth 1 https://github.com/mhalle/oabrowser.git OpenAnatomy-Browser
git clone --depth 1 https://github.com/biocat-ugent/Open-Anatomy-Explorer.git OpenAnatomy-Explorer
```

| 上游仓库 | 用途说明 |
| :--- | :--- |
| [Kevin-Mattheus-Moerman/BodyParts3D](https://github.com/Kevin-Mattheus-Moerman/BodyParts3D) | 本项目全部 83 个 `.stl` 医学网格与 `parts_list_e.txt` / `FMA.csv` 映射表来源 |
| [Z-Anatomy/Models-of-human-anatomy](https://github.com/Z-Anatomy/Models-of-human-anatomy) | 基于 BodyParts3D 重新整理分类的 Blender 图谱（`Z-Anatomy.zip`、`TA2.csv`） |
| [LluisV/Z-Anatomy](https://github.com/LluisV/Z-Anatomy) | Z-Anatomy 交互式客户端源码（图层隔离、搜索、肌肉起止点高亮参考） |
| [mhalle/oabrowser](https://github.com/mhalle/oabrowser) | 哈佛医学院 Open Anatomy 项目 WebGL 浏览器源码参考 |
| [biocat-ugent/Open-Anatomy-Explorer](https://github.com/biocat-ugent/Open-Anatomy-Explorer) | Web 端 3D 解剖浏览器与标注交互参考 |

---

## 四、模型重新提取与轻量化脚本（完全可复现）

如需从原始 `BodyParts3D` 重新提取并抽稀模型（需安装 `numpy`）：

```bash
pip install numpy
python3 scripts/prepare_models.py \
  --src ~/opensrc/anatomy-3d-refs/BodyParts3D/assets/BodyParts3D_data/stl \
  --dst ./models
```

脚本会自动完成：
1. 复制 80 个轻量化原始 `.stl` 网格；
2. 对体积过大的 3 个肌肉网格执行体素聚类抽稀，保证 WebGL 流畅渲染：
   - `FMA9756.stl`（肋间外肌）：`40.8 MB → 4.86 MB`（`voxel=2.6mm`）
   - `FMA22344.stl`（右侧腹横肌）：`15.7 MB → 1.82 MB`（`voxel=3.2mm`）
   - `FMA22345.stl`（左侧腹横肌）：`15.6 MB → 1.83 MB`（`voxel=3.2mm`）

---

## 五、83 个解剖模型 FMA 清单

| 系统分类 | 数量 | 包含结构与 FMA ID |
| :--- | :---: | :--- |
| **上下呼吸道** | 3 | 甲状软骨 `FMA55099`、气管 `FMA7394`、支气管树 `FMA7409` |
| **双肺五叶** | 5 | 右肺上/中/下叶 `FMA7333/7383/7337`、左肺上/下叶 `FMA7370/7371` |
| **主呼吸肌** | 1 | 横膈肌 `FMA13295` |
| **胸式呼吸肌** | 1 | 肋间外肌 `FMA9756` |
| **颈肩辅助/代偿肌** | 12 | 胸锁乳突肌 `FMA13408/13409`、前/中/后斜角肌 `FMA13388~13393`、上斜方肌 `FMA33586/33587`、胸小肌 `FMA13375/13376` |
| **核心腹壁** | 2 | 左右腹横肌 `FMA22344/22345` |
| **真实盆底肌群** | 8 | 耻骨尾骨肌 `FMA45854/45855`、耻骨直肠肌 `FMA45856/45857`、髂骨尾骨肌 `FMA45858/45859`、尾骨肌 `FMA46443/46444` |
| **胸廓前壁与肋骨** | 31 | 胸骨柄/体/剑突 `FMA7486~7488`、左右锁骨 `FMA13322/13323`、左右肋软骨 `BP24/BP28`、第 1~12 对完整肋骨 |
| **脊柱与骨盆** | 20 | 胸椎 T1–T12、腰椎 L1–L5、骶骨 `FMA16202`、左右髋骨 `FMA16586/16587` |

---

## 许可与致谢
本项目 3D 解剖 `.stl` 模型数据来源于东京大学 DBCLS **[BodyParts3D](http://lifesciencedb.jp/bp3d/)**，遵循 **CC BY-SA 2.1 Japan** 开源协议。
