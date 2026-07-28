# CryptoHack-CN

按 CryptoHack 题目集整理的中文精翻与个人解答网页。

## 目录约定

```text
CryptoHack-CN/
├─ index.md                 # 首页：只放题目集入口
├─ _layouts/                # 页面骨架
├─ _data/                   # 导航与题目索引数据
├─ assets/                  # 样式与少量交互
├─ tools/build_index.py     # 扫描目录并重建首页/分类页/题目页
└─ 题目集/
   ├─ index.md              # 题目集列表页
   └─ 题目名/
      ├─ original.md        # 英文题面
      ├─ translation.md     # 中文精翻
      ├─ WP.md              # 你的个人题解，可选
      ├─ WP.py              # 解题代码，可选
      └─ index.md           # 单题网页，由脚本生成
```

## 单题页结构

- `English Problem`：固定显示。
- `中文题面 / 精翻`：默认折叠，可展开。
- `我的解答`：默认折叠，可展开；如果还没有 `WP.md`，页面显示待补提示。

## 更新索引

新增题目集或题目后运行：

```powershell
python tools/build_index.py
```

脚本会扫描所有包含 `original.md` 的题目目录，并重建首页、题目集页和单题页。

## 协作约定

- 你写完题解后，可以让我润色；我只优化表达，不改你的语气和原意。
- 每次需要我帮你提交 GitHub，我都会先问你这次 commit 备注是什么。
