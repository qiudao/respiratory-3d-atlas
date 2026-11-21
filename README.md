# Open Respiratory & Core 3D Atlas

基于 **Three.js** 与 **BodyParts3D** 真实医学网格（83 个 `.stl` 解剖模型）构建的交互式 3D 呼吸系统与核心发力可视化平台。

## 在线预览（GitHub Pages）
* **完整 83 网格 3D 呼吸与核心发力图谱**：[https://qiudao.github.io/respiratory-3d-atlas/](https://qiudao.github.io/respiratory-3d-atlas/)

## 核心特性
- **83 个真实医学 `.stl` 网格**：包含喉（甲状软骨）、气管、支气管树、双肺 5 叶、横膈肌、肋间外肌、胸锁乳突肌、6 块斜角肌、上斜方肌、胸小肌、左右腹横肌、8 块真实盆底肌（肛提肌+尾骨肌）、胸骨、锁骨、肋软骨、1~12 对肋骨、T1–T12 胸椎、L1–L5 腰椎及骨盆环。
- **4 种呼吸模式生物力学对比**：`腹式呼吸` / `360° 胸腹联合（推荐）` / `胸式呼吸` / `颈部代偿呼吸`，支持分区胸廓运动（锁骨耸肩 / 胸骨泵柄 / 下肋桶柄）、实时 EMG 激活高亮与 3D 发力矢量箭头。
- **Atlas 级交互**：点击任意器官查看中英文与 FMA ID、孤立/隐藏/半透明/聚焦、冠状面 3D 剖面切片、X-Ray 气道透视、实时呼吸力学三通道示波器。

## 本地运行
```bash
python3 -m http.server 8765
# 浏览器访问 http://localhost:8765/
```

## 医学模型数据致谢
本项目的 3D 器官与骨骼 `.stl` 网格来源于东京大学 DBCLS 开源解剖数据集 **[BodyParts3D](http://lifesciencedb.jp/bp3d/)**（CC BY-SA 2.1 Japan 许可协议）。
