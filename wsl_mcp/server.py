"""
WSL MCP Server - WSL2环境管理工具
基于FastMCP框架开发
"""

from fastmcp import FastMCP
from typing import Optional, Dict, Any

mcp = FastMCP("WSL MCP")


@mcp.tool()
def execute_wsl_command(
    command: str, 
    timeout: int = 30
) -> Dict[str, Any]:
    """
    执行WSL命令
    
    参数:
        command: 要在WSL中执行的命令
        timeout: 命令超时时间（秒）
        
    返回:
        命令执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.execute_command(command, timeout)
    
    return {
        "成功": result.returncode == 0,
        "命令": command,
        "输出": result.stdout,
        "错误": result.stderr,
        "返回码": result.returncode
    }


@mcp.tool()
def execute_wsl_command_advanced(
    command: str,
    distribution: str = "",
    user: str = "",
    working_dir: str = "",
    shell_type: str = "",
    timeout: int = 30
) -> Dict[str, Any]:
    """
    高级WSL命令执行，支持更多选项
    
    参数:
        command: 要在WSL中执行的命令
        distribution: WSL发行版名称，为空则使用默认
        user: 用户名，为空则使用默认用户
        working_dir: 工作目录，~表示主目录
        shell_type: shell类型，可选 standard|login|none
        timeout: 命令超时时间（秒）
        
    返回:
        命令执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.execute_command_advanced(
        command, distribution, user, working_dir, shell_type, timeout
    )
    
    return {
        "成功": result.returncode == 0,
        "命令": command,
        "发行版": distribution or "默认",
        "用户": user or "默认",
        "工作目录": working_dir or "默认",
        "输出": result.stdout,
        "错误": result.stderr,
        "返回码": result.returncode
    }


@mcp.tool()
def shutdown_wsl() -> Dict[str, Any]:
    """
    关闭所有WSL发行版和虚拟机
    
    返回:
        执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.shutdown_wsl()
    
    return {
        "成功": result.returncode == 0,
        "消息": result.stdout,
        "错误": result.stderr
    }


@mcp.tool()
def terminate_wsl_distribution(distribution: str) -> Dict[str, Any]:
    """
    终止指定的WSL发行版
    
    参数:
        distribution: 要终止的发行版名称
        
    返回:
        执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.terminate_distribution(distribution)
    
    return {
        "成功": result.returncode == 0,
        "发行版": distribution,
        "消息": result.stdout,
        "错误": result.stderr
    }


@mcp.tool()
def set_default_wsl_distribution(distribution: str) -> Dict[str, Any]:
    """
    设置默认WSL发行版
    
    参数:
        distribution: 要设为默认的发行版名称
        
    返回:
        执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.set_default_distribution(distribution)
    
    return {
        "成功": result.returncode == 0,
        "发行版": distribution,
        "消息": result.stdout,
        "错误": result.stderr
    }


@mcp.tool()
def export_wsl_distribution(
    distribution: str,
    file_path: str,
    format_type: str = "tar"
) -> Dict[str, Any]:
    """
    导出WSL发行版到tar文件
    
    参数:
        distribution: 要导出的发行版名称
        file_path: 导出文件路径
        format_type: 格式类型，支持 tar|tar.gz|tar.xz|vhd
        
    返回:
        执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.export_distribution(distribution, file_path, format_type)
    
    return {
        "成功": result.returncode == 0,
        "发行版": distribution,
        "文件路径": file_path,
        "格式": format_type,
        "消息": result.stdout,
        "错误": result.stderr
    }


@mcp.tool()
def import_wsl_distribution(
    distribution: str,
    install_location: str,
    file_path: str,
    version: int = 2
) -> Dict[str, Any]:
    """
    导入WSL发行版
    
    参数:
        distribution: 新发行版名称
        install_location: 安装位置
        file_path: tar文件路径
        version: WSL版本，1或2
        
    返回:
        执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.import_distribution(distribution, install_location, file_path, version)
    
    return {
        "成功": result.returncode == 0,
        "发行版": distribution,
        "安装位置": install_location,
        "版本": version,
        "消息": result.stdout,
        "错误": result.stderr
    }


@mcp.tool()
def unregister_wsl_distribution(distribution: str) -> Dict[str, Any]:
    """
    注销并删除WSL发行版
    
    参数:
        distribution: 要注销的发行版名称
        
    返回:
        执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.unregister_distribution(distribution)
    
    return {
        "成功": result.returncode == 0,
        "发行版": distribution,
        "消息": result.stdout,
        "错误": result.stderr
    }


@mcp.tool()
def get_wsl_status() -> Dict[str, Any]:
    """
    获取WSL状态信息
    
    返回:
        状态信息
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.get_wsl_status()
    
    return {
        "成功": result.returncode == 0,
        "状态信息": result.stdout,
        "错误": result.stderr
    }


@mcp.tool()
def list_wsl_online_distributions() -> Dict[str, Any]:
    """
    列出可在线安装的WSL发行版
    
    返回:
        可用发行版列表
    """
    from wsl_mcp.core.wsl import wsl_tool
    distros = wsl_tool.list_online_distributions()
    
    return {
        "成功": True,
        "发行版数量": len(distros),
        "发行版列表": distros
    }


@mcp.tool()
def install_wsl_distribution(
    distribution: str = "",
    web_download: bool = False,
    no_launch: bool = False
) -> Dict[str, Any]:
    """
    安装WSL发行版
    
    参数:
        distribution: 要安装的发行版名称，为空则安装默认
        web_download: 是否从网络下载
        no_launch: 安装后是否不启动
        
    返回:
        执行结果
    """
    from wsl_mcp.core.wsl import wsl_tool
    result = wsl_tool.install_distribution(distribution, web_download, no_launch)
    
    return {
        "成功": result.returncode == 0,
        "发行版": distribution or "默认",
        "消息": result.stdout,
        "错误": result.stderr
    }


@mcp.tool()
def get_wsl_version() -> Dict[str, Any]:
    """
    获取WSL版本信息
    
    返回:
        WSL版本信息
    """
    from wsl_mcp.core.wsl import wsl_tool
    version = wsl_tool.get_wsl_version()
    
    return {
        "成功": True,
        "版本信息": version
    }


@mcp.tool()
def list_wsl_distributions() -> Dict[str, Any]:
    """
    列出已安装的WSL发行版
    
    返回:
        发行版列表
    """
    from wsl_mcp.core.wsl import wsl_tool
    distros = wsl_tool.list_distributions()
    
    return {
        "成功": True,
        "发行版数量": len(distros),
        "发行版列表": distros
    }


@mcp.tool()
def get_default_distribution() -> Dict[str, Any]:
    """
    获取默认WSL发行版
    
    返回:
        默认发行版信息
    """
    from wsl_mcp.core.wsl import wsl_tool
    distro = wsl_tool.get_default_distribution()
    
    return {
        "成功": True,
        "默认发行版": distro
    }


@mcp.tool()
def convert_windows_to_wsl_path(windows_path: str) -> Dict[str, Any]:
    """
    将Windows路径转换为WSL路径
    
    参数:
        windows_path: Windows路径，如 C:\\Users\\Name
        
    返回:
        转换后的WSL路径
    """
    from wsl_mcp.core.wsl import wsl_tool
    wsl_path = wsl_tool.convert_windows_path(windows_path)
    
    return {
        "成功": True,
        "Windows路径": windows_path,
        "WSL路径": wsl_path
    }


@mcp.tool()
def convert_wsl_to_windows_path(wsl_path: str) -> Dict[str, Any]:
    """
    将WSL路径转换为Windows路径
    
    参数:
        wsl_path: WSL路径，如 /mnt/c/Users/Name
        
    返回:
        转换后的Windows路径
    """
    from wsl_mcp.core.wsl import wsl_tool
    windows_path = wsl_tool.convert_to_windows_path(wsl_path)
    
    return {
        "成功": True,
        "WSL路径": wsl_path,
        "Windows路径": windows_path
    }


@mcp.tool()
def read_wsl_file(
    file_path: str, 
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """
    读取WSL中的文件内容
    
    参数:
        file_path: WSL中的文件路径
        encoding: 文件编码
        
    返回:
        文件内容
    """
    from wsl_mcp.tools.file_manager import read_file
    return read_file(file_path, encoding)


@mcp.tool()
def write_wsl_file(
    file_path: str, 
    content: str, 
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """
    创建或覆盖WSL中的文件
    
    参数:
        file_path: WSL中的文件路径
        content: 文件内容
        encoding: 文件编码
        
    返回:
        写入结果
    """
    from wsl_mcp.tools.file_manager import write_file
    return write_file(file_path, content, encoding)


@mcp.tool()
def append_to_wsl_file(
    file_path: str, 
    content: str, 
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """
    追加内容到WSL中的文件
    
    参数:
        file_path: WSL中的文件路径
        content: 要追加的内容
        encoding: 文件编码
        
    返回:
        追加结果
    """
    from wsl_mcp.tools.file_manager import append_to_file
    return append_to_file(file_path, content, encoding)


@mcp.tool()
def create_wsl_directory(
    dir_path: str, 
    parents: bool = True
) -> Dict[str, Any]:
    """
    在WSL中创建目录
    
    参数:
        dir_path: WSL中的目录路径
        parents: 是否创建父目录
        
    返回:
        创建结果
    """
    from wsl_mcp.tools.file_manager import create_directory
    return create_directory(dir_path, parents)


@mcp.tool()
def list_wsl_directory(dir_path: str = "~") -> Dict[str, Any]:
    """
    列出WSL目录内容
    
    参数:
        dir_path: WSL中的目录路径，默认为用户主目录
        
    返回:
        目录内容列表
    """
    from wsl_mcp.tools.file_manager import list_directory
    return list_directory(dir_path)


@mcp.tool()
def delete_wsl_path(
    file_path: str, 
    recursive: bool = False
) -> Dict[str, Any]:
    """
    删除WSL中的文件或目录
    
    参数:
        file_path: WSL中的文件或目录路径
        recursive: 是否递归删除（仅对目录有效）
        
    返回:
        删除结果
    """
    from wsl_mcp.tools.file_manager import delete_file
    return delete_file(file_path, recursive)


@mcp.tool()
def copy_wsl_file(
    source: str, 
    destination: str, 
    recursive: bool = False
) -> Dict[str, Any]:
    """
    复制WSL中的文件或目录
    
    参数:
        source: 源路径
        destination: 目标路径
        recursive: 是否递归复制（仅对目录有效）
        
    返回:
        复制结果
    """
    from wsl_mcp.tools.file_manager import copy_file
    return copy_file(source, destination, recursive)


@mcp.tool()
def move_wsl_file(source: str, destination: str) -> Dict[str, Any]:
    """
    移动或重命名WSL中的文件或目录
    
    参数:
        source: 源路径
        destination: 目标路径
        
    返回:
        移动结果
    """
    from wsl_mcp.tools.file_manager import move_file
    return move_file(source, destination)


@mcp.tool()
def get_wsl_file_info(file_path: str) -> Dict[str, Any]:
    """
    获取WSL中文件或目录的详细信息
    
    参数:
        file_path: WSL中的文件或目录路径
        
    返回:
        文件信息
    """
    from wsl_mcp.tools.file_manager import get_file_info
    return get_file_info(file_path)


@mcp.tool()
def check_wsl_path_exists(file_path: str) -> Dict[str, Any]:
    """
    检查WSL中文件或目录是否存在
    
    参数:
        file_path: WSL中的文件或目录路径
        
    返回:
        检查结果
    """
    from wsl_mcp.tools.file_manager import file_exists
    return file_exists(file_path)


@mcp.tool()
def is_wsl_directory(path: str) -> Dict[str, Any]:
    """
    检查WSL中路径是否为目录
    
    参数:
        path: WSL中的路径
        
    返回:
        检查结果
    """
    from wsl_mcp.tools.file_manager import is_directory
    return is_directory(path)


@mcp.tool()
def is_wsl_file(path: str) -> Dict[str, Any]:
    """
    检查WSL中路径是否为文件
    
    参数:
        path: WSL中的路径
        
    返回:
        检查结果
    """
    from wsl_mcp.tools.file_manager import is_file
    return is_file(path)


@mcp.tool()
def get_wsl_current_directory() -> Dict[str, Any]:
    """
    获取WSL当前工作目录
    
    返回:
        当前工作目录
    """
    from wsl_mcp.tools.file_manager import get_current_directory
    return get_current_directory()


@mcp.tool()
def change_wsl_directory(dir_path: str) -> Dict[str, Any]:
    """
    切换WSL当前工作目录
    
    参数:
        dir_path: 目标目录路径
        
    返回:
        切换结果
    """
    from wsl_mcp.tools.file_manager import change_directory
    return change_directory(dir_path)


@mcp.tool()
def read_wsl_file_lines(
    file_path: str, 
    start_line: int = 1, 
    end_line: Optional[int] = None,
    encoding: str = "utf-8"
) -> Dict[str, Any]:
    """
    读取WSL中文件的指定行
    
    参数:
        file_path: WSL中的文件路径
        start_line: 起始行号（从1开始）
        end_line: 结束行号，为空则到文件末尾
        encoding: 文件编码
        
    返回:
        文件内容
    """
    from wsl_mcp.tools.file_manager import read_file_lines
    return read_file_lines(file_path, start_line, end_line, encoding)


@mcp.tool()
def search_in_wsl_file(
    file_path: str, 
    pattern: str, 
    use_regex: bool = False
) -> Dict[str, Any]:
    """
    在WSL文件中搜索内容
    
    参数:
        file_path: WSL中的文件路径
        pattern: 搜索模式
        use_regex: 是否使用正则表达式
        
    返回:
        搜索结果
    """
    from wsl_mcp.tools.file_manager import search_in_file
    return search_in_file(file_path, pattern, use_regex)


@mcp.tool()
def count_wsl_file_lines(file_path: str) -> Dict[str, Any]:
    """
    统计WSL中文件的行数
    
    参数:
        file_path: WSL中的文件路径
        
    返回:
        统计结果
    """
    from wsl_mcp.tools.file_manager import count_lines
    return count_lines(file_path)


if __name__ == "__main__":
    mcp.run(transport='stdio')
