"""
Example of well-written Python code following best practices.

This file demonstrates proper coding standards, security practices,
and follows PEP 8 style guidelines.
"""

import logging
from typing import List, Dict, Optional, Any
from decimal import Decimal
from pathlib import Path
import json

# Configure logging instead of using print()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Constants instead of magic numbers
DISCOUNT_TIER_HIGH = Decimal('0.15')
DISCOUNT_TIER_MEDIUM = Decimal('0.10')
DISCOUNT_TIER_LOW = Decimal('0.05')
PRICE_THRESHOLD_HIGH = Decimal('1000')
PRICE_THRESHOLD_MEDIUM = Decimal('500')


def calculate_user_score(value: float) -> float:
    """
    Calculate a user score based on input value.

    Args:
        value: Numeric value to calculate score from

    Returns:
        Calculated score as a float

    Raises:
        TypeError: If value is not a number
        ValueError: If value is negative
    """
    # Input validation instead of eval()
    if not isinstance(value, (int, float)):
        raise TypeError(f"Expected number, got {type(value)}")

    if value < 0:
        raise ValueError("Score cannot be negative")

    logger.info(f"Calculating score for value: {value}")

    result = value * 100
    return result


def process_database_query(table: str, condition: str) -> List[Dict[str, Any]]:
    """
    Execute a parameterized database query safely.

    Args:
        table: Table name to query
        condition: WHERE condition

    Returns:
        List of result rows as dictionaries
    """
    # Use parameterized queries to prevent SQL injection
    # This is a placeholder - in real code, use SQLAlchemy or similar
    query = "SELECT * FROM ? WHERE ?"
    params = (table, condition)

    try:
        # Proper error handling
        result = execute_parameterized_query(query, params)
        logger.info(f"Query executed successfully on table: {table}")
        return result
    except DatabaseError as e:
        logger.error(f"Database query failed: {e}")
        raise


def read_config_file(filename: str = "config.txt") -> str:
    """
    Read configuration file with proper resource management.

    Args:
        filename: Path to configuration file

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file cannot be read
    """
    file_path = Path(filename)

    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {filename}")

    # Use context manager for automatic resource cleanup
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        logger.info(f"Successfully read config from {filename}")
        return data
    except IOError as e:
        logger.error(f"Failed to read config file: {e}")
        raise


def get_item_from_list(items: List[Any], index: int = 5) -> Optional[Any]:
    """
    Safely retrieve an item from a list with bounds checking.

    Args:
        items: List to retrieve from
        index: Index position (default: 5)

    Returns:
        Item at index, or None if index out of bounds
    """
    # Proper bounds checking
    if not items:
        logger.warning("Attempted to access empty list")
        return None

    if index < 0 or index >= len(items):
        logger.warning(f"Index {index} out of bounds for list of length {len(items)}")
        return None

    return items[index]


def divide_numbers(numerator: float, denominator: float) -> float:
    """
    Safely divide two numbers with zero-check.

    Args:
        numerator: Number to be divided
        denominator: Number to divide by

    Returns:
        Result of division

    Raises:
        ZeroDivisionError: If denominator is zero
    """
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero")

    return numerator / denominator


def append_to_list(item: Any, my_list: Optional[List[Any]] = None) -> List[Any]:
    """
    Append an item to a list, avoiding mutable default argument pitfall.

    Args:
        item: Item to append
        my_list: Optional list to append to (creates new list if None)

    Returns:
        List with item appended
    """
    # Avoid mutable default arguments
    if my_list is None:
        my_list = []

    my_list.append(item)
    return my_list


class UserManager:
    """Manages user creation and operations."""

    def __init__(self) -> None:
        """Initialize UserManager."""
        self.logger = logging.getLogger(f"{__name__}.UserManager")

    def create_user(self, name: str, email: str) -> str:
        """
        Create a new user and return serialized data.

        Args:
            name: User's full name
            email: User's email address

        Returns:
            JSON string of user data

        Raises:
            ValueError: If name or email is invalid
        """
        # Input validation
        if not name or not isinstance(name, str):
            raise ValueError("Invalid name")

        if not email or '@' not in email:
            raise ValueError("Invalid email")

        user_data = {
            'name': name,
            'email': email
        }

        # Use JSON instead of pickle for security
        serialized = json.dumps(user_data)
        self.logger.info(f"Created user: {name}")

        return serialized

    def execute_safe_command(self, command: List[str]) -> bytes:
        """
        Execute a system command safely.

        Args:
            command: Command as list of strings (not shell string)

        Returns:
            Command output as bytes

        Raises:
            subprocess.CalledProcessError: If command fails
        """
        import subprocess

        # Use shell=False and list of arguments to prevent injection
        try:
            result = subprocess.run(
                command,
                shell=False,  # Important for security!
                capture_output=True,
                check=True,
                timeout=30
            )
            self.logger.info(f"Command executed successfully: {command[0]}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e}")
            raise


def calculate_discount(price: Decimal) -> Decimal:
    """
    Calculate discount based on price tiers using named constants.

    Args:
        price: Item price as Decimal

    Returns:
        Discount amount as Decimal
    """
    if price > PRICE_THRESHOLD_HIGH:
        return price * DISCOUNT_TIER_HIGH
    elif price > PRICE_THRESHOLD_MEDIUM:
        return price * DISCOUNT_TIER_MEDIUM
    else:
        return price * DISCOUNT_TIER_LOW


def risky_operation() -> Optional[Dict[str, Any]]:
    """
    Perform operation with proper exception handling.

    Returns:
        Processed data dictionary, or None if operation fails
    """
    try:
        data = fetch_data()
        processed = process(data)
        return processed
    except ValueError as e:
        # Catch specific exceptions
        logger.error(f"Value error during operation: {e}")
        return None
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return None
    # Let unexpected exceptions propagate


# All functions have:
# - Type hints for parameters and return values
# - Comprehensive docstrings
# - Proper error handling
# - Input validation
# - Logging instead of print()
# - Named constants instead of magic numbers
