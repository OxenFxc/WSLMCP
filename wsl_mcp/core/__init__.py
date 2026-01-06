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
    
    def execute_command_with_distro(
        self, 
        command: str, 
        distribution: str = "",
        timeout: int = 30
    ) -> WSLCommandResult:
        """
        执行指定WSL发行版的命令
        
        参数:
            command: 要在WSL中执行的命令
            distribution: WSL发行版名称
            timeout: 命令超时时间（秒）
            
        返回:
            命令执行结果
        """
        try:
            cmd_list = [self.wsl_path]
            if distribution:
                cmd_list.extend(["-d", distribution])
            cmd_list.extend(["sh", "-c", command])
            
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
