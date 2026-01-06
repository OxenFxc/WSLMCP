"""
WSL核心执行模块
提供WSL命令执行的基础功能
"""

import subprocess
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class WSLCommandResult:
    """WSL命令执行结果"""
    returncode: int
    stdout: str
    stderr: str


class WSLTool:
    """
    WSL工具类
    提供在WSL2环境中执行命令的功能
    """
    
    def __init__(self):
        """初始化WSL工具"""
        self.wsl_path = self._find_wsl()
    
    def _find_wsl(self) -> str:
        """
        查找WSL可执行文件路径
        
        返回:
            WSL可执行文件路径
        """
        return "wsl.exe"
    
    def execute_command(
        self, 
        command: str, 
        timeout: int = 30
    ) -> WSLCommandResult:
        """
        执行WSL命令
        
        参数:
            command: 要在WSL中执行的命令
            timeout: 命令超时时间（秒）
            
        返回:
            命令执行结果
        """
        try:
            result = subprocess.run(
                [self.wsl_path, "sh", "-c", command],
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            
            return WSLCommandResult(
                returncode=result.returncode,
                stdout=result.stdout.strip(),
                stderr=result.stderr.strip()
            )
        except subprocess.TimeoutExpired:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr="命令执行超时"
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def execute_command_advanced(
        self,
        command: str,
        distribution: str = "",
        user: str = "",
        working_dir: str = "",
        shell_type: str = "",
        timeout: int = 30
    ) -> WSLCommandResult:
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
        try:
            cmd_list = [self.wsl_path]
            
            if distribution:
                cmd_list.extend(["-d", distribution])
            
            if user:
                cmd_list.extend(["-u", user])
            
            if working_dir:
                cmd_list.extend(["--cd", working_dir])
            
            if shell_type:
                cmd_list.extend(["--shell-type", shell_type])
            
            cmd_list.extend(["--exec", "sh", "-c", command])
            
            result = subprocess.run(
                cmd_list,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            
            return WSLCommandResult(
                returncode=result.returncode,
                stdout=result.stdout.strip(),
                stderr=result.stderr.strip()
            )
        except subprocess.TimeoutExpired:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr="命令执行超时"
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def shutdown_wsl(self) -> WSLCommandResult:
        """
        关闭所有WSL发行版和虚拟机
        
        返回:
            执行结果
        """
        try:
            result = subprocess.run(
                [self.wsl_path, "--shutdown"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace'
            )
            return WSLCommandResult(
                returncode=result.returncode,
                stdout="WSL已关闭" if result.returncode == 0 else "",
                stderr=result.stderr.strip()
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def terminate_distribution(self, distribution: str) -> WSLCommandResult:
        """
        终止指定的WSL发行版
        
        参数:
            distribution: 要终止的发行版名称
            
        返回:
            执行结果
        """
        try:
            result = subprocess.run(
                [self.wsl_path, "-t", distribution],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace'
            )
            return WSLCommandResult(
                returncode=result.returncode,
                stdout=f"发行版 {distribution} 已终止" if result.returncode == 0 else "",
                stderr=result.stderr.strip()
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def set_default_distribution(self, distribution: str) -> WSLCommandResult:
        """
        设置默认WSL发行版
        
        参数:
            distribution: 要设为默认的发行版名称
            
        返回:
            执行结果
        """
        try:
            result = subprocess.run(
                [self.wsl_path, "-s", distribution],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace'
            )
            return WSLCommandResult(
                returncode=result.returncode,
                stdout=f"{distribution} 已设为默认发行版" if result.returncode == 0 else "",
                stderr=result.stderr.strip()
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def export_distribution(
        self,
        distribution: str,
        file_path: str,
        format_type: str = "tar"
    ) -> WSLCommandResult:
        """
        导出WSL发行版到tar文件
        
        参数:
            distribution: 要导出的发行版名称
            file_path: 导出文件路径
            format_type: 格式类型，支持 tar|tar.gz|tar.xz|vhd
            
        返回:
            执行结果
        """
        try:
            result = subprocess.run(
                [self.wsl_path, "--export", distribution, file_path, "--format", format_type],
                capture_output=True,
                text=True,
                timeout=300,
                encoding='utf-8',
                errors='replace'
            )
            return WSLCommandResult(
                returncode=result.returncode,
                stdout=f"发行版已导出到 {file_path}" if result.returncode == 0 else "",
                stderr=result.stderr.strip()
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def import_distribution(
        self,
        distribution: str,
        install_location: str,
        file_path: str,
        version: int = 2
    ) -> WSLCommandResult:
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
        try:
            result = subprocess.run(
                [self.wsl_path, "--import", distribution, install_location, file_path, "--version", str(version)],
                capture_output=True,
                text=True,
                timeout=300,
                encoding='utf-8',
                errors='replace'
            )
            return WSLCommandResult(
                returncode=result.returncode,
                stdout=f"发行版 {distribution} 已导入" if result.returncode == 0 else "",
                stderr=result.stderr.strip()
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def unregister_distribution(self, distribution: str) -> WSLCommandResult:
        """
        注销并删除WSL发行版
        
        参数:
            distribution: 要注销的发行版名称
            
        返回:
            执行结果
        """
        try:
            result = subprocess.run(
                [self.wsl_path, "--unregister", distribution],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            return WSLCommandResult(
                returncode=result.returncode,
                stdout=f"发行版 {distribution} 已注销" if result.returncode == 0 else "",
                stderr=result.stderr.strip()
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def get_wsl_status(self) -> WSLCommandResult:
        """
        获取WSL状态信息
        
        返回:
            状态信息
        """
        try:
            result = subprocess.run(
                [self.wsl_path, "--status"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace'
            )
            return WSLCommandResult(
                returncode=result.returncode,
                stdout=result.stdout.strip(),
                stderr=result.stderr.strip()
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def list_online_distributions(self) -> list:
        """
        列出可在线安装的WSL发行版
        
        返回:
            可用发行版列表
        """
        try:
            result = subprocess.run(
                [self.wsl_path, "-l", "--online"],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                distros = []
                for line in lines[1:]:
                    if line.strip():
                        distros.append(line.strip())
                return distros
            return []
        except Exception:
            return []
    
    def install_distribution(
        self,
        distribution: str = "",
        web_download: bool = False,
        no_launch: bool = False
    ) -> WSLCommandResult:
        """
        安装WSL发行版
        
        参数:
            distribution: 要安装的发行版名称，为空则安装默认
            web_download: 是否从网络下载
            no_launch: 安装后是否不启动
            
        返回:
            执行结果
        """
        try:
            cmd_list = [self.wsl_path, "--install"]
            
            if distribution:
                cmd_list.append(distribution)
            
            if web_download:
                cmd_list.append("--web-download")
            
            if no_launch:
                cmd_list.extend(["--no-launch"])
            
            result = subprocess.run(
                cmd_list,
                capture_output=True,
                text=True,
                timeout=300,
                encoding='utf-8',
                errors='replace'
            )
            return WSLCommandResult(
                returncode=result.returncode,
                stdout="正在安装发行版..." if result.returncode == 0 else "",
                stderr=result.stderr.strip()
            )
        except Exception as e:
            return WSLCommandResult(
                returncode=-1,
                stdout="",
                stderr=str(e)
            )
    
    def get_wsl_version(self) -> str:
        """
        获取WSL版本信息
        
        返回:
            WSL版本字符串
        """
        result = subprocess.run(
            [self.wsl_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout.strip() if result.returncode == 0 else "无法获取WSL版本"
    
    def list_distributions(self) -> list:
        """
        列出已安装的WSL发行版
        
        返回:
            发行版列表
        """
        result = subprocess.run(
            [self.wsl_path, "-l", "--verbose"],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            distros = []
            for line in lines[1:]:
                if line.strip():
                    parts = line.split()
                    distros.append({
                        "名称": parts[0],
                        "状态": parts[1] if len(parts) > 1 else "",
                        "版本": parts[2] if len(parts) > 2 else ""
                    })
            return distros
        return []
    
    def get_default_distribution(self) -> str:
        """
        获取默认WSL发行版
        
        返回:
            默认发行版名称
        """
        result = subprocess.run(
            [self.wsl_path, "-e", "echo", "$WSL_DISTRO_NAME"],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    
    def convert_windows_path(self, windows_path: str) -> str:
        """
        将Windows路径转换为WSL路径
        
        参数:
            windows_path: Windows路径，如 C:\\Users\\Name
            
        返回:
            WSL路径，如 /mnt/c/Users/Name
        """
        if len(windows_path) >= 2 and windows_path[1] == ':':
            drive = windows_path[0].lower()
            wsl_path = f"/mnt/{drive}/{windows_path[2:].replace('\\', '/').replace('//', '/')}"
            return wsl_path
        return windows_path
    
    def convert_to_windows_path(self, wsl_path: str) -> str:
        """
        将WSL路径转换为Windows路径
        
        参数:
            wsl_path: WSL路径，如 /mnt/c/Users/Name
            
        返回:
            Windows路径，如 C:\\Users\\Name
        """
        if wsl_path.startswith("/mnt/"):
            parts = wsl_path.split("/")
            if len(parts) >= 3:
                drive = parts[2].upper()
                windows_path = f"{drive}:\\{'/'.join(parts[3:])}"
                return windows_path.replace("/", "\\")
        return wsl_path


wsl_tool = WSLTool()
