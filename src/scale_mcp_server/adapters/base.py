"""Base classes and interfaces for command executors.

This module provides the abstract base class and common data structures
for command execution adapters.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CommandResult:
    """Unified result structure for command execution.
    
    Attributes:
        stdout: Standard output from the command
        stderr: Standard error from the command
        returncode: Exit code of the command (0 = success)
        command: The command that was executed
    """
    stdout: str
    stderr: str
    returncode: int
    command: str
    
    @property
    def success(self) -> bool:
        """Check if command executed successfully."""
        return self.returncode == 0


class CommandExecutorInterface(ABC):
    """Abstract base class for command executors.
    
    All command executor implementations must inherit from this class
    and implement the execute method.
    """
    
    @abstractmethod
    def execute(
        self,
        command: list[str],
        **kwargs
    ) -> CommandResult:
        """Execute a command and return the result.
        
        Args:
            command: Command and arguments as a list
            **kwargs: Additional executor-specific parameters
            
        Returns:
            CommandResult: Unified result structure
            
        Raises:
            CommandError: Base exception for command-related errors
        """
        pass


class CommandError(Exception):
    """Base exception for command-related errors"""
    pass


class CommandExecutionError(CommandError):
    """Command execution errors"""
    pass


class CommandTimeoutError(CommandError):
    """Command timeout errors"""
    pass


class SSHConnectionError(CommandError):
    """SSH connection errors"""
    pass
