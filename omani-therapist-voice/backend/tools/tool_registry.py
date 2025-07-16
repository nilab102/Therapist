"""
Therapeutic Tool Registry for OMANI Therapist Voice.
Manages dynamic registration and creation of therapeutic tools.
"""

from typing import Dict, List, Type, Optional, Any
from loguru import logger
from .base_tool import BaseTool


class TherapeuticToolRegistry:
    """
    Registry for managing therapeutic tools in the OMANI Therapist Voice system.
    
    Provides dynamic tool registration, creation, and management with
    clinical safety and cultural sensitivity features.
    """
    
    def __init__(self):
        """Initialize the therapeutic tool registry."""
        self._tool_classes: Dict[str, Type[BaseTool]] = {}
        self._active_tools: Dict[str, BaseTool] = {}
        self._clinical_metadata: Dict[str, Dict] = {}
        logger.info("🏥 Initialized TherapeuticToolRegistry")
    
    def register_tool(self, tool_name: str, tool_class: Type[BaseTool], clinical_metadata: Optional[Dict] = None):
        """
        Register a therapeutic tool class.
        
        Args:
            tool_name: Unique name for the tool
            tool_class: Tool class that inherits from BaseTool
            clinical_metadata: Optional clinical metadata for the tool
        """
        if not issubclass(tool_class, BaseTool):
            raise ValueError(f"Tool class {tool_class.__name__} must inherit from BaseTool")
        
        self._tool_classes[tool_name] = tool_class
        self._clinical_metadata[tool_name] = clinical_metadata or {}
        
        logger.info(f"🏥 Registered therapeutic tool: {tool_name} ({tool_class.__name__})")
    
    def create_tool(self, tool_name: str, rtvi_processor, task=None) -> Optional[BaseTool]:
        """
        Create an instance of a registered therapeutic tool.
        
        Args:
            tool_name: Name of the tool to create
            rtvi_processor: RTVI processor for the tool
            task: Optional pipeline task
            
        Returns:
            Created tool instance or None if tool not found
        """
        if tool_name not in self._tool_classes:
            logger.error(f"🏥 Therapeutic tool '{tool_name}' not registered")
            return None
        
        try:
            tool_class = self._tool_classes[tool_name]
            tool_instance = tool_class(rtvi_processor, task)
            self._active_tools[tool_name] = tool_instance
            
            logger.info(f"🏥 Created therapeutic tool instance: {tool_name}")
            return tool_instance
        
        except Exception as e:
            logger.error(f"🏥 Error creating therapeutic tool '{tool_name}': {e}")
            return None
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """
        Get an active therapeutic tool instance.
        
        Args:
            tool_name: Name of the tool to retrieve
            
        Returns:
            Tool instance or None if not found
        """
        return self._active_tools.get(tool_name)
    
    def list_available_tools(self) -> List[str]:
        """
        List all available (registered) therapeutic tool names.
        
        Returns:
            List of available tool names
        """
        return list(self._tool_classes.keys())
    
    def list_active_tools(self) -> List[str]:
        """
        List all active (instantiated) therapeutic tool names.
        
        Returns:
            List of active tool names
        """
        return list(self._active_tools.keys())
    
    def get_tool_definitions(self) -> List[Dict]:
        """
        Get tool definitions for all active therapeutic tools.
        
        Returns:
            List of tool definitions for LLM function calling
        """
        definitions = []
        for tool_name, tool_instance in self._active_tools.items():
            try:
                definition = tool_instance.get_tool_definition()
                definitions.append(definition.to_dict() if hasattr(definition, 'to_dict') else definition)
            except Exception as e:
                logger.error(f"🏥 Error getting definition for tool '{tool_name}': {e}")
        
        return definitions
    
    def set_task_for_all_tools(self, task):
        """
        Set the pipeline task for all active therapeutic tools.
        
        Args:
            task: Pipeline task to set
        """
        for tool_name, tool_instance in self._active_tools.items():
            tool_instance.task = task
            logger.debug(f"🏥 Set task for therapeutic tool: {tool_name}")
    
    def get_clinical_metadata(self, tool_name: str) -> Dict:
        """
        Get clinical metadata for a therapeutic tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Clinical metadata dictionary
        """
        return self._clinical_metadata.get(tool_name, {})
    
    def get_all_clinical_data(self) -> Dict[str, Dict]:
        """
        Get clinical data from all active therapeutic tools.
        
        Returns:
            Dictionary mapping tool names to their clinical data
        """
        clinical_data = {}
        for tool_name, tool_instance in self._active_tools.items():
            if hasattr(tool_instance, 'clinical_data'):
                clinical_data[tool_name] = tool_instance.clinical_data
        
        return clinical_data
    
    def check_crisis_status(self) -> Dict[str, Any]:
        """
        Check crisis status across all active therapeutic tools.
        
        Returns:
            Crisis status summary
        """
        crisis_status = {
            "any_crisis_detected": False,
            "emergency_escalation_needed": False,
            "tools_with_crisis": [],
            "tools_with_escalation": []
        }
        
        for tool_name, tool_instance in self._active_tools.items():
            if hasattr(tool_instance, 'crisis_detected') and tool_instance.crisis_detected:
                crisis_status["any_crisis_detected"] = True
                crisis_status["tools_with_crisis"].append(tool_name)
            
            if hasattr(tool_instance, 'emergency_escalation_needed') and tool_instance.emergency_escalation_needed:
                crisis_status["emergency_escalation_needed"] = True
                crisis_status["tools_with_escalation"].append(tool_name)
        
        return crisis_status
    
    def reset_all_crisis_flags(self):
        """Reset crisis flags for all active therapeutic tools."""
        for tool_name, tool_instance in self._active_tools.items():
            if hasattr(tool_instance, 'crisis_detected'):
                tool_instance.crisis_detected = False
            if hasattr(tool_instance, 'emergency_escalation_needed'):
                tool_instance.emergency_escalation_needed = False
            if hasattr(tool_instance, 'professional_referral_suggested'):
                tool_instance.professional_referral_suggested = False
        
        logger.info("🏥 Reset crisis flags for all therapeutic tools")
    
    def deactivate_tool(self, tool_name: str) -> bool:
        """
        Deactivate an active therapeutic tool.
        
        Args:
            tool_name: Name of the tool to deactivate
            
        Returns:
            True if successfully deactivated
        """
        if tool_name in self._active_tools:
            del self._active_tools[tool_name]
            logger.info(f"🏥 Deactivated therapeutic tool: {tool_name}")
            return True
        return False
    
    def deactivate_all_tools(self):
        """Deactivate all active therapeutic tools."""
        self._active_tools.clear()
        logger.info("🏥 Deactivated all therapeutic tools")
    
    def get_tool_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the therapeutic tool registry.
        
        Returns:
            Tool registry statistics
        """
        return {
            "total_registered_tools": len(self._tool_classes),
            "total_active_tools": len(self._active_tools),
            "registered_tools": list(self._tool_classes.keys()),
            "active_tools": list(self._active_tools.keys()),
            "crisis_status": self.check_crisis_status(),
            "tools_with_clinical_data": [
                name for name, tool in self._active_tools.items() 
                if hasattr(tool, 'clinical_data') and tool.clinical_data
            ]
        }


# Global therapeutic tool registry instance
global_tool_registry = TherapeuticToolRegistry()


def register_tool(tool_name: str, tool_class: Type[BaseTool], clinical_metadata: Optional[Dict] = None):
    """
    Convenience function to register a therapeutic tool globally.
    
    Args:
        tool_name: Unique name for the tool
        tool_class: Tool class that inherits from BaseTool
        clinical_metadata: Optional clinical metadata for the tool
    """
    global_tool_registry.register_tool(tool_name, tool_class, clinical_metadata) 