"""
WSL文件管理工具模块
提供在WSL2环境中进行文件和目录操作的功能
"""

import subprocess
from typing import Dict, Any, Optional
from wsl_mcp.core.wsl import wsl_tool


def read_file(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    读取WSL中的文件内容
    
    参数:
        file_path: WSL中的文件路径
        encoding: 文件编码
        
    返回:
        文件内容
    """
    command = f"cat '{file_path}'"
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        try:
            content = result.stdout
            return {
                "成功": True,
                "文件路径": file_path,
                "内容": content,
                "编码": encoding
            }
        except UnicodeDecodeError:
            return {
                "成功": False,
                "文件路径": file_path,
                "错误": "文件编码无法解析，请尝试其他编码"
            }
    else:
        return {
            "成功": False,
            "文件路径": file_path,
            "错误": result.stderr
        }


def write_file(
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
    escaped_content = content.replace("'", "'\"'\"'")
    command = f"echo '{escaped_content}' > '{file_path}'"
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "文件路径": file_path,
            "消息": "文件写入成功"
        }
    else:
        return {
            "成功": False,
            "文件路径": file_path,
            "错误": result.stderr
        }


def append_to_file(
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
    escaped_content = content.replace("'", "'\"'\"'")
    command = f"echo '{escaped_content}' >> '{file_path}'"
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "文件路径": file_path,
            "消息": "内容追加成功"
        }
    else:
        return {
            "成功": False,
            "文件路径": file_path,
            "错误": result.stderr
        }


def create_directory(
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
    if parents:
        command = f"mkdir -p '{dir_path}'"
    else:
        command = f"mkdir '{dir_path}'"
    
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "目录路径": dir_path,
            "消息": "目录创建成功"
        }
    else:
        return {
            "成功": False,
            "目录路径": dir_path,
            "错误": result.stderr
        }


def list_directory(dir_path: str = "~") -> Dict[str, Any]:
    """
    列出WSL目录内容
    
    参数:
        dir_path: WSL中的目录路径，默认为用户主目录
        
    返回:
        目录内容列表
    """
    command = f"ls -la '{dir_path}'"
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        items = []
        for line in lines:
            if line:
                parts = line.split()
                if len(parts) >= 9:
                    perms = parts[0]
                    name = " ".join(parts[8:])
                    is_dir = perms.startswith('d')
                    items.append({
                        "名称": name,
                        "权限": perms,
                        "类型": "目录" if is_dir else "文件"
                    })
        
        return {
            "成功": True,
            "目录路径": dir_path,
            "项目数量": len(items),
            "内容": items
        }
    else:
        return {
            "成功": False,
            "目录路径": dir_path,
            "错误": result.stderr
        }


def delete_file(file_path: str, recursive: bool = False) -> Dict[str, Any]:
    """
    删除WSL中的文件或目录
    
    参数:
        file_path: WSL中的文件或目录路径
        recursive: 是否递归删除（仅对目录有效）
        
    返回:
        删除结果
    """
    if recursive:
        command = f"rm -rf '{file_path}'"
    else:
        command = f"rm -f '{file_path}'"
    
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "路径": file_path,
            "消息": "删除成功"
        }
    else:
        return {
            "成功": False,
            "路径": file_path,
            "错误": result.stderr
        }


def copy_file(
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
    if recursive:
        command = f"cp -r '{source}' '{destination}'"
    else:
        command = f"cp '{source}' '{destination}'"
    
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "源路径": source,
            "目标路径": destination,
            "消息": "复制成功"
        }
    else:
        return {
            "成功": False,
            "源路径": source,
            "目标路径": destination,
            "错误": result.stderr
        }


def move_file(source: str, destination: str) -> Dict[str, Any]:
    """
    移动或重命名WSL中的文件或目录
    
    参数:
        source: 源路径
        destination: 目标路径
        
    返回:
        移动结果
    """
    command = f"mv '{source}' '{destination}'"
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "源路径": source,
            "目标路径": destination,
            "消息": "移动成功"
        }
    else:
        return {
            "成功": False,
            "源路径": source,
            "目标路径": destination,
            "错误": result.stderr
        }


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    获取WSL中文件或目录的详细信息
    
    参数:
        file_path: WSL中的文件或目录路径
        
    返回:
        文件信息
    """
    command = f"stat '{file_path}'"
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "路径": file_path,
            "详细信息": result.stdout
        }
    else:
        return {
            "成功": False,
            "路径": file_path,
            "错误": result.stderr
        }


def file_exists(file_path: str) -> Dict[str, Any]:
    """
    检查WSL中文件或目录是否存在
    
    参数:
        file_path: WSL中的文件或目录路径
        
    返回:
        检查结果
    """
    command = f"if [ -e '{file_path}' ]; then echo 'exists'; else echo 'not_exists'; fi"
    result = wsl_tool.execute_command(command)
    
    exists = result.stdout == "exists"
    return {
        "成功": True,
        "路径": file_path,
        "存在": exists
    }


def is_directory(path: str) -> Dict[str, Any]:
    """
    检查WSL中路径是否为目录
    
    参数:
        path: WSL中的路径
        
    返回:
            检查结果
    """
    command = f"if [ -d '{path}' ]; then echo 'dir'; else echo 'not_dir'; fi"
    result = wsl_tool.execute_command(command)
    
    is_dir = result.stdout == "dir"
    return {
        "成功": True,
        "路径": path,
        "是目录": is_dir
    }


def is_file(path: str) -> Dict[str, Any]:
    """
    检查WSL中路径是否为文件
    
    参数:
        path: WSL中的路径
        
    返回:
        检查结果
    """
    command = f"if [ -f '{path}' ]; then echo 'file'; else echo 'not_file'; fi"
    result = wsl_tool.execute_command(command)
    
    is_file = result.stdout == "file"
    return {
        "成功": True,
        "路径": path,
        "是文件": is_file
    }


def get_current_directory() -> Dict[str, Any]:
    """
    获取WSL当前工作目录
    
    返回:
        当前工作目录
    """
    result = wsl_tool.execute_command("pwd")
    
    if result.returncode == 0:
        return {
            "成功": True,
            "当前目录": result.stdout
        }
    else:
        return {
            "成功": False,
            "错误": result.stderr
        }


def change_directory(dir_path: str) -> Dict[str, Any]:
    """
    切换WSL当前工作目录
    
    参数:
        dir_path: 目标目录路径
        
    返回:
        切换结果
    """
    command = f"cd '{dir_path}' && pwd"
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "新目录": result.stdout
        }
    else:
        return {
            "成功": False,
            "目标目录": dir_path,
            "错误": result.stderr
        }


def read_file_lines(
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
    if end_line:
        command = f"sed -n '{start_line},{end_line}p' '{file_path}'"
    else:
        command = f"sed -n '{start_line},$p' '{file_path}'"
    
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        return {
            "成功": True,
            "文件路径": file_path,
            "起始行": start_line,
            "结束行": end_line,
            "内容": result.stdout
        }
    else:
        return {
            "成功": False,
            "文件路径": file_path,
            "错误": result.stderr
        }


def search_in_file(
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
    if use_regex:
        command = f"grep -n '{pattern}' '{file_path}'"
    else:
        command = f"grep -nF '{pattern}' '{file_path}'"
    
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n') if result.stdout else []
        return {
            "成功": True,
            "文件路径": file_path,
            "搜索模式": pattern,
            "匹配行数": len(lines),
            "匹配结果": lines
        }
    else:
        return {
            "成功": False,
            "文件路径": file_path,
            "搜索模式": pattern,
            "错误": result.stderr
        }


def count_lines(file_path: str) -> Dict[str, Any]:
    """
    统计WSL中文件的行数
    
    参数:
        file_path: WSL中的文件路径
        
    返回:
        统计结果
    """
    command = f"wc -l '{file_path}'"
    result = wsl_tool.execute_command(command)
    
    if result.returncode == 0:
        try:
            line_count = int(result.stdout.strip().split()[0])
            return {
                "成功": True,
                "文件路径": file_path,
                "行数": line_count
            }
        except (ValueError, IndexError):
            return {
                "成功": False,
                "文件路径": file_path,
                "错误": "无法解析行数"
            }
    else:
        return {
            "成功": False,
            "文件路径": file_path,
            "错误": result.stderr
        }
