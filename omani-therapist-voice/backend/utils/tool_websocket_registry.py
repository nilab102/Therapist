"""
Tool WebSocket Registry for OMANI Therapist Voice.
Manages WebSocket connections for real-time tool communication with automatic cleanup.
"""

import json
from typing import Dict, Any, Optional
from fastapi import WebSocket
from loguru import logger

# Global registry for therapeutic tool WebSocket connections
tool_websockets: Dict[str, WebSocket] = {}


async def broadcast_to_all_therapeutic_clients(command_data: Dict[str, Any]) -> int:
    """
    Broadcast a command to all connected therapeutic tool WebSocket clients.
    Returns the number of clients that received the message successfully.
    """
    sent_count = 0
    failed_clients = []
    
    for client_id, ws in tool_websockets.items():
        try:
            await ws.send_json(command_data)
            sent_count += 1
            logger.debug(f"✅ Therapeutic command sent to tool client {client_id}")
        except Exception as e:
            logger.error(f"❌ Failed to send to therapeutic tool client {client_id}: {e}")
            failed_clients.append(client_id)
    
    # Clean up failed connections
    for client_id in failed_clients:
        if client_id in tool_websockets:
            del tool_websockets[client_id]
            logger.info(f"🧹 Removed disconnected therapeutic tool client {client_id}")
    
    if sent_count > 0:
        logger.info(f"✅ Therapeutic broadcast sent to {sent_count} tool clients")
    else:
        logger.warning("⚠️ No therapeutic tool WebSocket clients available for broadcast")
    
    return sent_count


async def send_to_specific_therapeutic_client(client_id: str, command_data: Dict[str, Any]) -> bool:
    """
    Send a command to a specific therapeutic tool WebSocket client.
    Returns True if successful, False otherwise.
    """
    if client_id not in tool_websockets:
        logger.error(f"❌ Therapeutic tool client {client_id} not found")
        return False
    
    try:
        ws = tool_websockets[client_id]
        await ws.send_json(command_data)
        logger.info(f"✅ Therapeutic command sent to specific tool client {client_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send to therapeutic tool client {client_id}: {e}")
        # Clean up failed connection
        if client_id in tool_websockets:
            del tool_websockets[client_id]
            logger.info(f"🧹 Removed disconnected therapeutic tool client {client_id}")
        return False


def get_therapeutic_clients_count() -> int:
    """Get the number of currently connected therapeutic tool WebSocket clients."""
    return len(tool_websockets)


def get_therapeutic_client_ids() -> list:
    """Get a list of all connected therapeutic tool WebSocket client IDs."""
    return list(tool_websockets.keys())


def is_therapeutic_client_connected(client_id: str) -> bool:
    """Check if a specific therapeutic client is connected."""
    return client_id in tool_websockets


def log_therapeutic_connection_status():
    """Log the current therapeutic connection status for debugging."""
    count = get_therapeutic_clients_count()
    if count > 0:
        client_ids = get_therapeutic_client_ids()
        logger.info(f"🏥 {count} therapeutic tool WebSocket clients connected: {client_ids}")
    else:
        logger.warning("⚠️ No therapeutic tool WebSocket clients connected")


logger.info("🔗 Therapeutic Tool WebSocket Registry initialized with cleanup functionality") 