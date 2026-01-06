# WSL MCP Tool

WSL MCP Tool 是一个基于 FastMCP 框架开发的 WSL2 环境管理工具，通过 WSL 命令与 Windows Subsystem for Linux 进行交互，提供丰富的 WSL 管理和文件操作功能。

## 作者信息

- GitHub: OxenFxc
- 哔哩哔哩: DifierLine

## 版本信息

- 当前版本: 1.0.0
- 发布日期: 2026-01-07

## 功能特性

### 1. WSL 命令执行
- 执行基本的 WSL 命令
- 高级 WSL 命令执行，支持指定发行版、用户、工作目录和 Shell 类型
- 可配置超时时间

### 2. WSL 发行版管理
- 列出已安装的 WSL 发行版
- 列出可在线安装的 WSL 发行版
- 安装新的 WSL 发行版
- 终止指定的 WSL 发行版
- 设置默认 WSL 发行版
- 导出 WSL 发行版到 tar 文件
- 导入 WSL 发行版
- 注销并删除 WSL 发行版
- 关闭所有 WSL 发行版和虚拟机

### 3. WSL 状态查询
- 获取 WSL 状态信息
- 获取 WSL 版本信息
- 获取默认 WSL 发行版

### 4. 路径转换
- 将 Windows 路径转换为 WSL 路径
- 将 WSL 路径转换为 Windows 路径

### 5. 文件管理
- 读取 WSL 中的文件内容
- 创建或覆盖 WSL 中的文件
- 追加内容到 WSL 中的文件
- 读取 WSL 中文件的指定行
- 在 WSL 文件中搜索内容
- 统计 WSL 中文件的行数

### 6. 目录管理
- 列出 WSL 目录内容
- 在 WSL 中创建目录
- 获取 WSL 当前工作目录
- 切换 WSL 当前工作目录

### 7. 文件操作
- 删除 WSL 中的文件或目录
- 复制 WSL 中的文件或目录
- 移动或重命名 WSL 中的文件或目录

### 8. 文件检查
- 检查 WSL 中文件或目录是否存在
- 获取 WSL 中文件或目录的详细信息
- 检查 WSL 中路径是否为目录
- 检查 WSL 中路径是否为文件

## 项目结构

```
wsl_mcp/
├── __init__.py            # 工具包初始化文件
├── server.py              # FastMCP 服务器入口
├── core/
│   ├── __init__.py
│   └── wsl.py             # WSL 核心执行模块
└── tools/
    ├── __init__.py
    └── file_manager.py    # 文件管理工具模块
```

## 使用方法

### 1. 安装依赖

```bash
pip install fastmcp
```

### 2. 配置 MCP

编辑 `mcp.json` 文件，将 `PYTHONPATH` 替换为 `wsl_mcp` 目录的实际路径：

```json
{
  "mcpServers": {
    "WSLMCP": {
      "command": "python",
      "args": [
        "-m",
        "wsl_mcp.server"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\ruilo\\Documents\\TRAE"
      }
    }
  }
}
```

## 可用工具列表

| 工具函数 | 功能描述 |
|---------|---------|
| execute_wsl_command | 执行 WSL 命令 |
| execute_wsl_command_advanced | 高级 WSL 命令执行 |
| shutdown_wsl | 关闭所有 WSL 发行版和虚拟机 |
| terminate_wsl_distribution | 终止指定的 WSL 发行版 |
| set_default_wsl_distribution | 设置默认 WSL 发行版 |
| export_wsl_distribution | 导出 WSL 发行版到 tar 文件 |
| import_wsl_distribution | 导入 WSL 发行版 |
| unregister_wsl_distribution | 注销并删除 WSL 发行版 |
| get_wsl_status | 获取 WSL 状态信息 |
| list_wsl_online_distributions | 列出可在线安装的 WSL 发行版 |
| install_wsl_distribution | 安装 WSL 发行版 |
| get_wsl_version | 获取 WSL 版本信息 |
| list_wsl_distributions | 列出已安装的 WSL 发行版 |
| get_default_distribution | 获取默认 WSL 发行版 |
| convert_windows_to_wsl_path | 将 Windows 路径转换为 WSL 路径 |
| convert_wsl_to_windows_path | 将 WSL 路径转换为 Windows 路径 |
| read_wsl_file | 读取 WSL 中的文件内容 |
| write_wsl_file | 创建或覆盖 WSL 中的文件 |
| append_to_wsl_file | 追加内容到 WSL 中的文件 |
| create_wsl_directory | 在 WSL 中创建目录 |
| list_wsl_directory | 列出 WSL 目录内容 |
| delete_wsl_path | 删除 WSL 中的文件或目录 |
| copy_wsl_file | 复制 WSL 中的文件或目录 |
| move_wsl_file | 移动或重命名 WSL 中的文件或目录 |
| get_wsl_file_info | 获取 WSL 中文件或目录的详细信息 |
| check_wsl_path_exists | 检查 WSL 中文件或目录是否存在 |
| is_wsl_directory | 检查 WSL 中路径是否为目录 |
| is_wsl_file | 检查 WSL 中路径是否为文件 |
| get_wsl_current_directory | 获取 WSL 当前工作目录 |
| change_wsl_directory | 切换 WSL 当前工作目录 |
| read_wsl_file_lines | 读取 WSL 中文件的指定行 |
| search_in_wsl_file | 在 WSL 文件中搜索内容 |
| count_wsl_file_lines | 统计 WSL 中文件的行数 |

## 参数说明

所有工具函数都支持以下可选参数：

- `timeout`: 命令执行超时时间（秒），默认 30 秒。
- `encoding`: 文件编码，默认 utf-8。

WSL 发行版相关参数：

- `distribution`: WSL 发行版名称，为空则使用默认发行版。
- `user`: 用户名，为空则使用默认用户。
- `working_dir`: 工作目录，~ 表示主目录。
- `shell_type`: Shell 类型，可选 standard|login|none。

## 使用示例

```python
# 执行 WSL 命令
result = execute_wsl_command("ls -la")

# 使用指定发行版执行命令
result = execute_wsl_command_advanced("echo hello", distribution="Ubuntu")

# 列出已安装的 WSL 发行版
distros = list_wsl_distributions()

# 安装新的 WSL 发行版
result = install_wsl_distribution("Ubuntu-22.04")

# 关闭所有 WSL 发行版
result = shutdown_wsl()

# 路径转换
wsl_path = convert_windows_to_wsl_path("C:\\Users\\Name")
windows_path = convert_wsl_to_windows_path("/mnt/c/Users/Name")

# 读取 WSL 文件
content = read_wsl_file("/home/user/file.txt")

# 写入 WSL 文件
result = write_wsl_file("/home/user/test.txt", "Hello World")

# 列出目录内容
files = list_wsl_directory("/home/user")

# 搜索文件内容
matches = search_in_wsl_file("/home/user/log.txt", "error")
```

## 系统要求

- Python 3.8+
- Windows 10/11 with WSL2 enabled
- FastMCP

## 许可证

本项目可以自由使用、修改和分发，但必须在项目中明确标注原作者信息。

## 致谢

感谢所有使用和支持本项目的用户。
