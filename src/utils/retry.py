"""
Retry utility for handling flaky scenarios with bounded waits.
Use sparingly and only for legitimate retry scenarios.
"""

import time
from typing import Callable, Optional, Type, Union


def retry(
    max_attempts: int = 3,
    wait_seconds: float = 1.0,
    backoff_factor: float = 1.0,
    exception_types: Union[Type[Exception], tuple] = Exception,
) -> Callable:
    """
    Decorator for retrying a function with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        wait_seconds: Initial wait time between retries (seconds)
        backoff_factor: Multiplier for wait time on each retry
        exception_types: Exception type(s) to catch for retry
    
    Example:
        @retry(max_attempts=3, wait_seconds=0.5)
        def flaky_operation():
            ...
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            last_exception = None
            wait_time = wait_seconds
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exception_types as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(wait_time)
                        wait_time *= backoff_factor
            
            # All attempts failed, raise the last exception
            raise last_exception
        
        return wrapper
    
    return decorator


def wait_for(
    condition: Callable[[], bool],
    timeout: float = 10.0,
    poll_interval: float = 0.5,
) -> bool:
    """
    Wait for a condition to become true.
    
    Args:
        condition: Callable that returns True when condition is met
        timeout: Maximum time to wait in seconds
        poll_interval: Time between condition checks
    
    Returns:
        True if condition was met, False if timeout exceeded
    
    Example:
        wait_for(lambda: element.is_visible(), timeout=5)
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            if condition():
                return True
        except Exception:
            pass
        
        time.sleep(poll_interval)
    
    return False
