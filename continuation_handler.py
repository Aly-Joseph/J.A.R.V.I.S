#!/usr/bin/env python3
"""
🔄 CONTINUATION HANDLER
Manages multi-step conversations and continuation prompts
Tracks ongoing tasks and processes "ok", "continue", "thik hai" commands
"""

import json
import os
from typing import Optional, Dict, Any

# Continuation keywords
CONTINUATION_KEYWORDS = {
    # English
    "ok", "okay", "yes", "sure", "go ahead", "proceed", "continue",
    "do it", "start", "begin", "let's go", "go", "right", "correct",
    
    # Hindi/Hinglish
    "thik hai", "bilkul", "haan", "han", "theek", "chalo",
    "shuruaat kar", "agey badho", "next", "aage chalein",
    "shi hai", "sahi hai", "theek acha", "accha", "acha"
}

class ContinuationTracker:
    """Tracks ongoing tasks and conversations for continuation"""
    
    def __init__(self):
        self.current_task: Optional[Dict[str, Any]] = None
        self.task_history = []
        self.context_buffer = ""
    
    def is_continuation(self, user_input: str) -> bool:
        """Check if input is a continuation command"""
        normalized = user_input.lower().strip()
        
        # Direct match
        if normalized in CONTINUATION_KEYWORDS:
            return True
        
        # Partial match (for phrases like "ok thik hai")
        for keyword in CONTINUATION_KEYWORDS:
            if keyword in normalized:
                return True
        
        return False
    
    def start_task(self, task_type: str, task_data: Dict[str, Any], response: str) -> None:
        """Start tracking a new task"""
        self.current_task = {
            "type": task_type,
            "data": task_data,
            "initial_response": response,
            "status": "pending_confirmation"
        }
        self.context_buffer = response
    
    def continue_task(self) -> Optional[Dict[str, Any]]:
        """Process continuation of current task"""
        if not self.current_task:
            return None
        
        # Return task info for next step
        task_info = self.current_task.copy()
        task_info["status"] = "continuing"
        
        return task_info
    
    def complete_task(self) -> None:
        """Mark current task as complete"""
        if self.current_task:
            self.task_history.append(self.current_task)
        self.current_task = None
        self.context_buffer = ""
    
    def get_continuation_context(self) -> str:
        """Get context for continuation"""
        if not self.current_task:
            return ""
        
        return f"""
Previous task type: {self.current_task['type']}
Initial response: {self.current_task['initial_response']}
Status: {self.current_task['status']}

User has confirmed to continue. Process the next step.
"""
    
    def get_multi_step_prompt(self, original_prompt: str, step: int) -> str:
        """Generate multi-step prompt"""
        return f"""
{original_prompt}

[Multi-step process - Step {step}]
Continue from the previous response. Execute the next logical action.
Maintain context from previous steps.
"""
    
    def reset(self) -> None:
        """Reset continuation state"""
        self.current_task = None
        self.context_buffer = ""

# Global tracker instance
_continuation_tracker = ContinuationTracker()

def get_tracker() -> ContinuationTracker:
    """Get global continuation tracker"""
    return _continuation_tracker

def is_continuation_prompt(user_input: str) -> bool:
    """Check if input is a continuation prompt"""
    return _continuation_tracker.is_continuation(user_input)

def start_tracking_task(task_type: str, task_data: Dict[str, Any], response: str) -> None:
    """Start tracking a task"""
    _continuation_tracker.start_task(task_type, task_data, response)

def process_continuation(original_prompt: str, step: int = 2) -> str:
    """Process continuation and get enhanced prompt"""
    context = _continuation_tracker.get_continuation_context()
    enhanced = _continuation_tracker.get_multi_step_prompt(original_prompt, step)
    return f"{enhanced}\n\n{context}"

def mark_task_complete() -> None:
    """Mark current task as complete"""
    _continuation_tracker.complete_task()

def has_active_task() -> bool:
    """Check if there's an active task being tracked"""
    return _continuation_tracker.current_task is not None

# Test
if __name__ == "__main__":
    tracker = get_tracker()
    
    print("=" * 70)
    print("🔄 CONTINUATION HANDLER TEST")
    print("=" * 70)
    
    # Test 1: Check continuation keywords
    test_inputs = [
        "ok",
        "thik hai",
        "okay proceed",
        "yes go ahead",
        "bilkul shuruaat kar",
        "something else"
    ]
    
    print("\n📝 Continuation Keyword Detection:")
    for inp in test_inputs:
        result = is_continuation_prompt(inp)
        symbol = "✓" if result else "✗"
        print(f"  {symbol} '{inp}' → {result}")
    
    # Test 2: Task tracking
    print("\n📌 Task Tracking:")
    start_tracking_task(
        "file_creation",
        {"filename": "test.py", "content": "test"},
        "File will be created at D:/test.py. Confirm?"
    )
    print(f"  Active task: {has_active_task()}")
    
    context = process_continuation("Create a Python file")
    print(f"  Continuation context length: {len(context)} chars")
    
    mark_task_complete()
    print(f"  Task completed: {not has_active_task()}")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
