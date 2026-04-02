"""Local command executor for IBM Storage Scale MCP Server.

This module provides local command execution using subprocess.
"""

import subprocess
from typing import Optional
import logging

from .base import (
    CommandExecutorInterface,
    CommandResult,
    CommandExecutionError,
    CommandTimeoutError
)

logger = logging.getLogger(__name__)


class LocalCommandExecutor(CommandExecutorInterface):
    """Execute commands locally using subprocess.
    
    This executor runs commands on the local machine using Python's
    subprocess module. It supports shell execution, working directory
    specification, and timeout controls.
    """
    
    def __init__(self, command_timeout: int = 30):
        """Initialize the local command executor.
        
        Args:
            command_timeout: Maximum execution time in seconds (default: 30)
        """
        self.command_timeout = command_timeout
        logger.info(f"LocalCommandExecutor initialized with timeout={command_timeout}s")
    
    def execute(
        self,
        command: list[str],
        shell: bool = False,
        cwd: Optional[str] = None,
        **kwargs
    ) -> CommandResult:
        """Execute a command locally.
        
        Args:
            command: Command and arguments as a list
            shell: Whether to execute through shell (default: False)
            cwd: Working directory for command execution (optional)
            
        Returns:
            CommandResult: Unified result structure with stdout, stderr, and returncode
            
        Raises:
            CommandTimeoutError: If command exceeds timeout
            CommandExecutionError: If command execution fails
        """
        command_str = ' '.join(command)
        
        logger.info(f"Executing local command: {command_str}")
        if cwd:
            logger.debug(f"Working directory: {cwd}")
        
        try:
            result = subprocess.run(
                command if not shell else command_str,
                shell=shell,
                text=True,
                capture_output=True,
                timeout=self.command_timeout,
                cwd=cwd,
            )
            
            command_result = CommandResult(
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode,
                command=command_str
            )
            
            if command_result.success:
                logger.info("Command executed successfully (exit code: 0)")
            else:
                logger.warning(f"Command failed with exit code {result.returncode}")
            
            return command_result
            
        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after {self.command_timeout} seconds"
            logger.error(error_msg)
            raise CommandTimeoutError(error_msg) from e
            
        except Exception as e:
            error_msg = f"Command execution failed: {str(e)}"
            logger.error(error_msg)
            raise CommandExecutionError(error_msg) from e
