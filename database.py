"""
Database module for IG Trading portfolio tracking and rebalancing.
Uses SQLite for persistent storage.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from contextlib import contextmanager
import os


DB_PATH = "ig_trading.db"


@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Initialize the database with required tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Portfolio snapshots table - stores current state of portfolio
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                total_value REAL,
                cash_balance REAL,
                positions_json TEXT,  -- JSON array of positions
                metadata_json TEXT,   -- Additional metadata (account info, etc.)
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Rebalancing actions table - logs all rebalancing decisions and actions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rebalancing_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                snapshot_id INTEGER,  -- Reference to portfolio_snapshots
                action_type TEXT NOT NULL,  -- 'buy', 'sell', 'rebalance', 'no_action'
                target_allocation_json TEXT,  -- Target portfolio allocation
                current_allocation_json TEXT,  -- Current portfolio allocation
                actions_taken_json TEXT,  -- JSON array of specific trades/actions
                reason TEXT,  -- Why this rebalancing was done
                success BOOLEAN,  -- Whether the action was successful
                error_message TEXT,  -- Error details if failed
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (snapshot_id) REFERENCES portfolio_snapshots(id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_snapshots_timestamp 
            ON portfolio_snapshots(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_rebalancing_timestamp 
            ON rebalancing_actions(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_rebalancing_snapshot 
            ON rebalancing_actions(snapshot_id)
        """)
        
        print("Database initialized successfully")


def save_portfolio_snapshot(
    total_value: Optional[float] = None,
    cash_balance: Optional[float] = None,
    positions: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> int:
    """
    Save a portfolio snapshot to the database.
    
    Args:
        total_value: Total portfolio value
        cash_balance: Available cash balance
        positions: List of position dictionaries
        metadata: Additional metadata dictionary
    
    Returns:
        The ID of the created snapshot
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        positions_json = json.dumps(positions) if positions else None
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute("""
            INSERT INTO portfolio_snapshots 
            (timestamp, total_value, cash_balance, positions_json, metadata_json)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            total_value,
            cash_balance,
            positions_json,
            metadata_json
        ))
        
        snapshot_id = cursor.lastrowid
        print(f"Portfolio snapshot saved with ID: {snapshot_id}")
        return snapshot_id


def save_rebalancing_action(
    snapshot_id: Optional[int],
    action_type: str,
    target_allocation: Optional[Dict[str, Any]] = None,
    current_allocation: Optional[Dict[str, Any]] = None,
    actions_taken: Optional[List[Dict[str, Any]]] = None,
    reason: Optional[str] = None,
    success: bool = True,
    error_message: Optional[str] = None
) -> int:
    """
    Save a rebalancing action to the database.
    
    Args:
        snapshot_id: ID of the related portfolio snapshot
        action_type: Type of action ('buy', 'sell', 'rebalance', 'no_action')
        target_allocation: Target portfolio allocation
        current_allocation: Current portfolio allocation
        actions_taken: List of specific actions/trades taken
        reason: Reason for the rebalancing
        success: Whether the action was successful
        error_message: Error message if failed
    
    Returns:
        The ID of the created rebalancing action
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        target_json = json.dumps(target_allocation) if target_allocation else None
        current_json = json.dumps(current_allocation) if current_allocation else None
        actions_json = json.dumps(actions_taken) if actions_taken else None
        
        cursor.execute("""
            INSERT INTO rebalancing_actions 
            (timestamp, snapshot_id, action_type, target_allocation_json, 
             current_allocation_json, actions_taken_json, reason, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            snapshot_id,
            action_type,
            target_json,
            current_json,
            actions_json,
            reason,
            success,
            error_message
        ))
        
        action_id = cursor.lastrowid
        print(f"Rebalancing action saved with ID: {action_id}")
        return action_id


def get_latest_snapshot() -> Optional[Dict[str, Any]]:
    """Get the most recent portfolio snapshot."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM portfolio_snapshots 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def get_snapshots(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent portfolio snapshots."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM portfolio_snapshots 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]


def get_rebalancing_actions(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent rebalancing actions."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM rebalancing_actions 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]


def get_snapshot_with_actions(snapshot_id: int) -> Optional[Dict[str, Any]]:
    """Get a snapshot with its associated rebalancing actions."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get snapshot
        cursor.execute("SELECT * FROM portfolio_snapshots WHERE id = ?", (snapshot_id,))
        snapshot_row = cursor.fetchone()
        if not snapshot_row:
            return None
        
        snapshot = dict(snapshot_row)
        
        # Get associated actions
        cursor.execute("""
            SELECT * FROM rebalancing_actions 
            WHERE snapshot_id = ? 
            ORDER BY timestamp DESC
        """, (snapshot_id,))
        actions = [dict(row) for row in cursor.fetchall()]
        
        snapshot['rebalancing_actions'] = actions
        return snapshot


if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
    print(f"Database file created at: {os.path.abspath(DB_PATH)}")

