#!/usr/bin/env python3
"""
View database contents - useful for debugging and monitoring.
"""

import json
from database import get_snapshots, get_rebalancing_actions, get_latest_snapshot


def print_snapshot(snapshot):
    """Pretty print a portfolio snapshot."""
    print(f"\n{'='*60}")
    print(f"Snapshot ID: {snapshot['id']}")
    print(f"Timestamp: {snapshot['timestamp']}")
    print(f"Total Value: {snapshot['total_value']}")
    print(f"Cash Balance: {snapshot['cash_balance']}")
    
    if snapshot['positions_json']:
        positions = json.loads(snapshot['positions_json'])
        print(f"\nPositions ({len(positions)}):")
        for pos in positions:
            print(f"  - {pos}")
    else:
        print("\nNo positions data")
    
    if snapshot['metadata_json']:
        metadata = json.loads(snapshot['metadata_json'])
        print(f"\nMetadata: {json.dumps(metadata, indent=2)}")


def print_rebalancing_action(action):
    """Pretty print a rebalancing action."""
    print(f"\n{'='*60}")
    print(f"Action ID: {action['id']}")
    print(f"Timestamp: {action['timestamp']}")
    print(f"Snapshot ID: {action['snapshot_id']}")
    print(f"Action Type: {action['action_type']}")
    print(f"Success: {action['success']}")
    print(f"Reason: {action['reason']}")
    
    if action['actions_taken_json']:
        actions = json.loads(action['actions_taken_json'])
        print(f"\nActions Taken ({len(actions)}):")
        for act in actions:
            print(f"  - {json.dumps(act, indent=2)}")
    
    if action['error_message']:
        print(f"\nError: {action['error_message']}")


def main():
    """Main function to view database contents."""
    print("IG Trading Database Viewer")
    print("="*60)
    
    # Show latest snapshot
    print("\n=== Latest Portfolio Snapshot ===")
    latest = get_latest_snapshot()
    if latest:
        print_snapshot(latest)
    else:
        print("No snapshots found in database")
    
    # Show recent snapshots
    print("\n\n=== Recent Portfolio Snapshots (last 5) ===")
    snapshots = get_snapshots(limit=5)
    if snapshots:
        for snapshot in snapshots:
            print(f"\nSnapshot ID {snapshot['id']}: {snapshot['timestamp']} - "
                  f"Value: {snapshot['total_value']}, Cash: {snapshot['cash_balance']}")
    else:
        print("No snapshots found")
    
    # Show recent rebalancing actions
    print("\n\n=== Recent Rebalancing Actions (last 5) ===")
    actions = get_rebalancing_actions(limit=5)
    if actions:
        for action in actions:
            print_rebalancing_action(action)
    else:
        print("No rebalancing actions found")


if __name__ == "__main__":
    main()

