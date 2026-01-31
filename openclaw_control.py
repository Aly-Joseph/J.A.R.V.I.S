"""
OpenClaw Integration Module for Jarvis AI
Handles robotic claw/gripper operations, movement control, and vision-based manipulation
"""

import time
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import OpenClaw - graceful fallback if not installed
try:
    from openclaw import ClawController, GripperState, MovementMode
    OPENCLAW_AVAILABLE = True
except ImportError:
    logger.warning("OpenClaw not installed. Install via: pip install openclaw")
    OPENCLAW_AVAILABLE = False

@dataclass
class ClawAction:
    """Represents a claw action"""
    action_type: str  # "grab", "release", "move", "rotate"
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    rotation: Optional[float] = None
    force: Optional[float] = None
    duration: Optional[float] = None

class OpenClawInterface:
    """Main interface for OpenClaw control"""
    
    def __init__(self, port: str = None):
        """
        Initialize OpenClaw interface
        
        Args:
            port: Serial port for claw connection (auto-detect if None)
        """
        self.connected = False
        self.controller = None
        self.last_position = (0, 0, 0)
        self.gripper_state = "open"
        self.action_history = []
        
        if OPENCLAW_AVAILABLE:
            try:
                self.controller = ClawController(port=port)
                self.connected = True
                logger.info("OpenClaw successfully connected")
            except Exception as e:
                logger.error(f"Failed to initialize OpenClaw: {e}")
                self.connected = False
        else:
            logger.warning("OpenClaw not available - running in simulation mode")
    
    def grab(self, force: float = 50.0, duration: float = 1.0) -> bool:
        """
        Close gripper to grab object
        
        Args:
            force: Grip force (0-100)
            duration: Time to apply force
            
        Returns:
            Success status
        """
        try:
            if self.connected and self.controller:
                self.controller.grip(force=force, duration=duration)
            
            self.gripper_state = "closed"
            action = ClawAction("grab", force=force, duration=duration)
            self.action_history.append(action)
            logger.info(f"Grab executed - Force: {force}%, Duration: {duration}s")
            return True
        except Exception as e:
            logger.error(f"Grab failed: {e}")
            return False
    
    def release(self, speed: float = 50.0) -> bool:
        """
        Open gripper to release object
        
        Args:
            speed: Release speed (0-100)
            
        Returns:
            Success status
        """
        try:
            if self.connected and self.controller:
                self.controller.release(speed=speed)
            
            self.gripper_state = "open"
            action = ClawAction("release")
            self.action_history.append(action)
            logger.info(f"Release executed - Speed: {speed}%")
            return True
        except Exception as e:
            logger.error(f"Release failed: {e}")
            return False
    
    def move_to(self, x: float, y: float, z: float, speed: float = 50.0) -> bool:
        """
        Move claw to absolute position
        
        Args:
            x, y, z: Target coordinates
            speed: Movement speed (0-100)
            
        Returns:
            Success status
        """
        try:
            if self.connected and self.controller:
                self.controller.move_to(x=x, y=y, z=z, speed=speed)
            
            self.last_position = (x, y, z)
            action = ClawAction("move", x=x, y=y, z=z)
            self.action_history.append(action)
            logger.info(f"Move executed - Position: ({x}, {y}, {z}), Speed: {speed}%")
            return True
        except Exception as e:
            logger.error(f"Move failed: {e}")
            return False
    
    def move_relative(self, dx: float, dy: float, dz: float, speed: float = 50.0) -> bool:
        """
        Move claw relative to current position
        
        Args:
            dx, dy, dz: Relative movement
            speed: Movement speed (0-100)
            
        Returns:
            Success status
        """
        try:
            new_x = self.last_position[0] + dx
            new_y = self.last_position[1] + dy
            new_z = self.last_position[2] + dz
            
            return self.move_to(new_x, new_y, new_z, speed)
        except Exception as e:
            logger.error(f"Relative move failed: {e}")
            return False
    
    def rotate(self, angle: float, axis: str = "z", speed: float = 50.0) -> bool:
        """
        Rotate gripper
        
        Args:
            angle: Rotation angle in degrees
            axis: Rotation axis (x, y, or z)
            speed: Rotation speed (0-100)
            
        Returns:
            Success status
        """
        try:
            if self.connected and self.controller:
                self.controller.rotate(angle=angle, axis=axis, speed=speed)
            
            action = ClawAction("rotate", rotation=angle)
            self.action_history.append(action)
            logger.info(f"Rotate executed - Angle: {angle}°, Axis: {axis}, Speed: {speed}%")
            return True
        except Exception as e:
            logger.error(f"Rotate failed: {e}")
            return False
    
    def sequence(self, actions: List[ClawAction], delay: float = 0.5) -> bool:
        """
        Execute sequence of actions
        
        Args:
            actions: List of ClawAction objects
            delay: Delay between actions
            
        Returns:
            Success status
        """
        try:
            for action in actions:
                if action.action_type == "grab":
                    self.grab(force=action.force, duration=action.duration)
                elif action.action_type == "release":
                    self.release()
                elif action.action_type == "move":
                    self.move_to(action.x, action.y, action.z)
                elif action.action_type == "rotate":
                    self.rotate(action.rotation)
                
                time.sleep(delay)
            
            logger.info(f"Sequence completed - {len(actions)} actions executed")
            return True
        except Exception as e:
            logger.error(f"Sequence failed: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get current claw status"""
        return {
            "connected": self.connected,
            "position": self.last_position,
            "gripper": self.gripper_state,
            "actions_executed": len(self.action_history)
        }
    
    def home(self) -> bool:
        """Move to home position"""
        try:
            if self.connected and self.controller:
                self.controller.home()
            
            self.last_position = (0, 0, 0)
            self.gripper_state = "open"
            logger.info("Home position reached")
            return True
        except Exception as e:
            logger.error(f"Home failed: {e}")
            return False
    
    def disconnect(self):
        """Safely disconnect from claw"""
        try:
            if self.connected and self.controller:
                self.controller.disconnect()
            self.connected = False
            logger.info("OpenClaw disconnected")
        except Exception as e:
            logger.error(f"Disconnect failed: {e}")

# Global claw instance
_claw_instance = None

def init_claw(port: str = None) -> OpenClawInterface:
    """Initialize global claw instance"""
    global _claw_instance
    _claw_instance = OpenClawInterface(port=port)
    return _claw_instance

def get_claw() -> OpenClawInterface:
    """Get global claw instance"""
    global _claw_instance
    if _claw_instance is None:
        _claw_instance = OpenClawInterface()
    return _claw_instance

# =========================
# VOICE COMMAND HANDLERS
# =========================

def handle_grab_command(instruction: str) -> str:
    """Handle grab/close commands via voice"""
    claw = get_claw()
    
    # Extract force if specified
    force = 50.0
    if "force" in instruction.lower():
        try:
            force = float(''.join(filter(str.isdigit, instruction)))
        except:
            pass
    
    success = claw.grab(force=force)
    return "Claw grabbed successfully" if success else "Grab operation failed"

def handle_release_command(instruction: str) -> str:
    """Handle release/open commands via voice"""
    claw = get_claw()
    success = claw.release()
    return "Object released successfully" if success else "Release operation failed"

def handle_move_command(instruction: str) -> str:
    """Handle move commands via voice"""
    claw = get_claw()
    
    # Parse coordinates from instruction
    try:
        # Simple parsing: "move to 10 20 30"
        parts = instruction.lower().split()
        coords = [float(x) for x in parts if x.replace('.', '', 1).isdigit()]
        
        if len(coords) >= 3:
            success = claw.move_to(coords[0], coords[1], coords[2])
            return f"Moved to ({coords[0]}, {coords[1]}, {coords[2]})" if success else "Move failed"
    except:
        pass
    
    return "Could not parse movement coordinates"

def handle_home_command(instruction: str) -> str:
    """Handle home position command"""
    claw = get_claw()
    success = claw.home()
    return "Returned to home position" if success else "Home command failed"

def handle_status_command(instruction: str) -> str:
    """Get current claw status"""
    claw = get_claw()
    status = claw.get_status()
    return f"Claw Status: Connected={status['connected']}, Position={status['position']}, Gripper={status['gripper']}"

# Voice command routing
CLAW_VOICE_COMMANDS = {
    "grab": handle_grab_command,
    "grasp": handle_grab_command,
    "close": handle_grab_command,
    "clench": handle_grab_command,
    "release": handle_release_command,
    "open": handle_release_command,
    "drop": handle_release_command,
    "move": handle_move_command,
    "go": handle_move_command,
    "home": handle_home_command,
    "return": handle_home_command,
    "status": handle_status_command,
    "report": handle_status_command,
}

def process_claw_command(user_text: str) -> Optional[str]:
    """
    Process voice command for claw control
    
    Args:
        user_text: User's voice input
        
    Returns:
        Response string or None if not a claw command
    """
    user_lower = user_text.lower()
    
    for keyword, handler in CLAW_VOICE_COMMANDS.items():
        if keyword in user_lower:
            return handler(user_text)
    
    return None
