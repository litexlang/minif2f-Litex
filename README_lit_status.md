# Minif2f Litex Status Management

这个目录包含了用于管理 `minif2f.jsonl` 文件中 `lit_completed` 状态的工具脚本。

## 文件说明

### 1. `update_jsonl_with_lit_status.py`
- **功能**: 一次性为 JSONL 文件添加 `lit_completed` 列
- **用法**: `python3 update_jsonl_with_lit_status.py`
- **特点**: 
  - 自动检测 `valid_litex_code` 目录中的 `.lit` 文件
  - 创建备份文件 `minif2f.jsonl.backup`
  - 为每个问题添加 `lit_completed` 字段（true/false）

### 2. `quick_update.py`
- **功能**: 快速更新现有的 `lit_completed` 状态
- **用法**: `python3 quick_update.py`
- **特点**:
  - 轻量级脚本，运行快速
  - 根据当前 `.lit` 文件状态更新 JSONL
  - 显示完成统计信息

### 3. `manage_lit_status.py`
- **功能**: 高级交互式状态管理工具
- **用法**: `python3 manage_lit_status.py`
- **特点**:
  - 交互式菜单界面
  - 支持搜索、标记、统计等功能
  - 可以导出完成报告
  - 支持手动标记特定问题

## 使用场景

### 场景1: 首次设置
```bash
# 为 JSONL 文件添加 lit_completed 列
python3 update_jsonl_with_lit_status.py
```

### 场景2: 日常更新
```bash
# 快速更新状态（推荐日常使用）
python3 quick_update.py
```

### 场景3: 高级管理
```bash
# 使用交互式工具进行详细管理
python3 manage_lit_status.py
```

## 数据结构

更新后的 JSONL 文件每行包含以下字段：
```json
{
  "name": "problem_name",
  "split": "valid",
  "informal_prefix": "问题描述...",
  "formal_statement": "theorem...",
  "goal": "证明目标...",
  "header": "import语句...",
  "lit_completed": true/false
}
```

## 统计信息

当前状态（运行 `quick_update.py` 后显示）：
- 总问题数: 488
- 已完成: 45 (9.2%)
- 剩余: 443

## 手动标记

如果需要手动标记特定问题为已完成：

1. 使用 `manage_lit_status.py` 的交互式界面
2. 或者直接编辑 JSONL 文件，将 `"lit_completed": false` 改为 `"lit_completed": true`

## 备份和恢复

- 自动备份: `minif2f.jsonl.backup`
- 恢复命令: `cp minif2f.jsonl.backup minif2f.jsonl`

## 注意事项

1. 运行脚本前确保 `valid_litex_code` 目录存在
2. 脚本会自动创建备份，但建议手动备份重要数据
3. JSONL 文件使用 UTF-8 编码
4. 问题名称必须与 `.lit` 文件名（不含扩展名）完全匹配
