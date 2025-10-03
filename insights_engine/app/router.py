"""
Expert Router - Routes dataset contexts to appropriate domain experts
"""

from typing import Dict, List, Any, Tuple
import logging
from datetime import datetime
import json

from .experts.base_expert import BaseExpert
from .experts.energy_efficiency import EnergyEfficiencyExpert


class ExpertRouter:
    """
    Routes dataset contexts to appropriate domain experts using
    intelligent routing logic and maintains audit logs.
    """
    
    def __init__(self):
        self.experts: List[BaseExpert] = []
        self.logger = logging.getLogger('expert_router')
        self._initialize_experts()
    
    def _initialize_experts(self):
        """Initialize all available domain experts."""
        self.experts = [
            EnergyEfficiencyExpert(),
            # Additional experts would be added here:
            # TransportationExpert(),
            # HealthcareExpert(),
            # EducationExpert(),
            # etc.
        ]
        
        self.logger.info(f"Initialized {len(self.experts)} domain experts")
    
    def route_to_experts(self, context: Dict[str, Any]) -> Tuple[List[BaseExpert], Dict[str, Any]]:
        """
        Route dataset context to appropriate experts.
        
        Args:
            context: Dataset context containing metadata and analysis
        
        Returns:
            Tuple of (selected_experts, routing_log)
        """
        routing_log = {
            "timestamp": datetime.now().isoformat(),
            "dataset_name": context.get('name', 'Unknown'),
            "routing_decisions": [],
            "selected_experts": [],
            "routing_strategy": "capability_matching"
        }
        
        selected_experts = []
        
        for expert in self.experts:
            try:
                can_handle = expert.can_handle(context)
                
                decision_log = {
                    "expert_name": expert.name,
                    "expert_domain": expert.domain,
                    "can_handle": can_handle,
                    "alignment_score": expert.assess_strategic_alignment(context) if can_handle else 0.0,
                    "decision_timestamp": datetime.now().isoformat()
                }
                
                routing_log["routing_decisions"].append(decision_log)
                
                if can_handle:
                    selected_experts.append(expert)
                    routing_log["selected_experts"].append({
                        "name": expert.name,
                        "domain": expert.domain,
                        "capabilities": expert.capabilities
                    })
                    
            except Exception as e:
                self.logger.error(f"Error routing to expert {expert.name}: {str(e)}")
                decision_log = {
                    "expert_name": expert.name,
                    "expert_domain": expert.domain,
                    "can_handle": False,
                    "error": str(e),
                    "decision_timestamp": datetime.now().isoformat()
                }
                routing_log["routing_decisions"].append(decision_log)
        
        # If no experts can handle the context, select the most relevant one
        if not selected_experts:
            fallback_expert = self._select_fallback_expert(context)
            if fallback_expert:
                selected_experts.append(fallback_expert)
                routing_log["selected_experts"].append({
                    "name": fallback_expert.name,
                    "domain": fallback_expert.domain,
                    "capabilities": fallback_expert.capabilities,
                    "fallback": True
                })
                routing_log["routing_strategy"] = "fallback_selection"
        
        self.logger.info(f"Routed dataset '{context.get('name')}' to {len(selected_experts)} experts")
        
        return selected_experts, routing_log
    
    def generate_use_cases(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate use cases using routed experts.
        
        Args:
            context: Dataset context
        
        Returns:
            Dictionary containing generated use cases and metadata
        """
        experts, routing_log = self.route_to_experts(context)
        
        generation_log = {
            "timestamp": datetime.now().isoformat(),
            "dataset_name": context.get('name', 'Unknown'),
            "experts_used": len(experts),
            "use_cases_generated": 0,
            "generation_errors": []
        }
        
        use_cases = []
        
        for expert in experts:
            try:
                use_case = expert.generate_use_case(context)
                if expert.validate_use_case(use_case):
                    use_case["generated_by"] = {
                        "expert_name": expert.name,
                        "expert_domain": expert.domain,
                        "generation_timestamp": datetime.now().isoformat()
                    }
                    use_cases.append(use_case)
                    generation_log["use_cases_generated"] += 1
                else:
                    self.logger.warning(f"Invalid use case generated by {expert.name}")
                    generation_log["generation_errors"].append({
                        "expert": expert.name,
                        "error": "Use case validation failed"
                    })
                    
            except Exception as e:
                self.logger.error(f"Error generating use case with {expert.name}: {str(e)}")
                generation_log["generation_errors"].append({
                    "expert": expert.name,
                    "error": str(e)
                })
        
        return {
            "use_cases": use_cases,
            "routing_log": routing_log,
            "generation_log": generation_log,
            "context": context
        }
    
    def _select_fallback_expert(self, context: Dict[str, Any]) -> BaseExpert:
        """
        Select the most relevant expert when no expert can handle the context.
        
        Args:
            context: Dataset context
        
        Returns:
            Most relevant expert or None
        """
        if not self.experts:
            return None
        
        # For now, return the first expert as fallback
        # In a full implementation, this would use similarity scoring
        fallback_expert = self.experts[0]
        
        self.logger.info(f"Selected fallback expert: {fallback_expert.name}")
        return fallback_expert
    
    def get_available_experts(self) -> List[Dict[str, Any]]:
        """
        Get information about all available experts.
        
        Returns:
            List of expert information dictionaries
        """
        return [
            {
                "name": expert.name,
                "domain": expert.domain,
                "capabilities": expert.capabilities,
                "keywords": expert.get_domain_keywords()
            }
            for expert in self.experts
        ]
    
    def save_routing_log(self, routing_log: Dict[str, Any], log_dir: str = "logs"):
        """
        Save routing log to file for audit purposes.
        
        Args:
            routing_log: Routing log dictionary
            log_dir: Directory to save logs
        """
        try:
            import os
            os.makedirs(log_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dataset_name = routing_log.get("dataset_name", "unknown").replace(" ", "_")
            filename = f"{log_dir}/routing_log_{dataset_name}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(routing_log, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Routing log saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save routing log: {str(e)}")
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about expert routing performance.
        
        Returns:
            Dictionary containing routing statistics
        """
        return {
            "total_experts": len(self.experts),
            "available_domains": [expert.domain for expert in self.experts],
            "expert_names": [expert.name for expert in self.experts],
            "total_capabilities": sum(len(expert.capabilities) for expert in self.experts)
        }