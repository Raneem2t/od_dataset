"""
Base Expert Class - Template for all domain experts
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging


class BaseExpert(ABC):
    """
    Abstract base class for all domain experts in the Insights Engine.
    
    Each expert specializes in a specific domain and can:
    1. Determine if they can handle a given dataset context
    2. Generate strategic use cases aligned with national objectives
    """
    
    def __init__(self, name: str, domain: str, capabilities: List[str]):
        self.name = name
        self.domain = domain
        self.capabilities = capabilities
        self.logger = logging.getLogger(f"expert.{self.name.lower().replace(' ', '_')}")
    
    @abstractmethod
    def can_handle(self, context: Dict[str, Any]) -> bool:
        """
        Determine if this expert can handle the given dataset context.
        
        Args:
            context: Dictionary containing dataset metadata and analysis context
                    - name: Dataset name
                    - description: Dataset description
                    - keywords: List of keywords
                    - domain_classification: Classified domain(s)
                    - strategic_alignment: Strategic alignment score
        
        Returns:
            bool: True if this expert can handle the context, False otherwise
        """
        pass
    
    @abstractmethod
    def generate_use_case(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a strategic use case for the given dataset context.
        
        Args:
            context: Dataset context dictionary
        
        Returns:
            Dict containing the generated use case with structure:
            {
                "title": str,
                "objective": str,
                "implementation": str,
                "strategic_alignment": List[str],
                "impact_areas": List[str],
                "priority": str,  # "high", "medium", "low"
                "timeline": str,
                "resources_required": List[str],
                "success_metrics": List[str]
            }
        """
        pass
    
    def get_domain_keywords(self) -> List[str]:
        """
        Get domain-specific keywords that this expert handles.
        
        Returns:
            List of keywords relevant to this expert's domain
        """
        return []
    
    def assess_strategic_alignment(self, context: Dict[str, Any]) -> float:
        """
        Assess how well the dataset aligns with strategic objectives.
        
        Args:
            context: Dataset context dictionary
        
        Returns:
            float: Alignment score between 0.0 and 1.0
        """
        return 0.5  # Default neutral alignment
    
    def log_routing_decision(self, context: Dict[str, Any], can_handle: bool, reason: str):
        """
        Log the routing decision for audit purposes.
        
        Args:
            context: Dataset context
            can_handle: Whether this expert can handle the context
            reason: Reason for the decision
        """
        self.logger.info(f"Routing Decision - Expert: {self.name}, "
                        f"Dataset: {context.get('name', 'Unknown')}, "
                        f"Can Handle: {can_handle}, Reason: {reason}")
    
    def validate_use_case(self, use_case: Dict[str, Any]) -> bool:
        """
        Validate the generated use case structure.
        
        Args:
            use_case: Generated use case dictionary
        
        Returns:
            bool: True if use case is valid, False otherwise
        """
        required_fields = [
            "title", "objective", "implementation", 
            "strategic_alignment", "impact_areas", "priority"
        ]
        
        for field in required_fields:
            if field not in use_case or not use_case[field]:
                self.logger.error(f"Missing or empty required field: {field}")
                return False
        
        if use_case["priority"] not in ["high", "medium", "low"]:
            self.logger.error(f"Invalid priority value: {use_case['priority']}")
            return False
        
        return True