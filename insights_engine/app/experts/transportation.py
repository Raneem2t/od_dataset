"""
Transportation Expert - Specializes in transportation, logistics, and mobility
"""

from typing import Dict, List, Any
from .base_expert import BaseExpert


class TransportationExpert(BaseExpert):
    """
    Domain expert specializing in transportation systems, logistics,
    urban mobility, and smart transportation infrastructure.
    """
    
    def __init__(self):
        super().__init__(
            name="Transportation Expert",
            domain="Transportation & Mobility",
            capabilities=[
                "Traffic flow optimization",
                "Public transport planning",
                "Logistics network design",
                "Smart mobility solutions",
                "Transportation infrastructure",
                "Fleet management",
                "Route optimization",
                "Multimodal integration"
            ]
        )
    
    def can_handle(self, context: Dict[str, Any]) -> bool:
        """Determine if this expert can handle transportation-related datasets."""
        transport_keywords = self.get_domain_keywords()
        
        dataset_text = f"{context.get('name', '')} {context.get('description', '')}".lower()
        keywords = [kw.lower() for kw in context.get('keywords', [])]
        
        transport_matches = sum(1 for keyword in transport_keywords if keyword in dataset_text)
        keyword_matches = sum(1 for keyword in keywords if keyword in transport_keywords)
        
        domain_classification = context.get('domain_classification', [])
        transport_domains = ['transportation', 'logistics', 'mobility', 'traffic']
        domain_match = any(domain in domain_classification for domain in transport_domains)
        
        can_handle = transport_matches >= 2 or keyword_matches >= 1 or domain_match
        
        reason = f"Transport keyword matches: {transport_matches}, " \
                f"Keyword list matches: {keyword_matches}, " \
                f"Domain match: {domain_match}"
        
        self.log_routing_decision(context, can_handle, reason)
        return can_handle
    
    def generate_use_case(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate transportation focused use case."""
        dataset_name = context.get('name', 'Transportation Dataset')
        description = context.get('description', '')
        keywords = context.get('keywords', [])
        
        focus_area = self._determine_focus_area(description, keywords)
        
        use_cases = {
            'smart_mobility': self._generate_smart_mobility_use_case(dataset_name, description),
            'public_transport': self._generate_public_transport_use_case(dataset_name, description),
            'logistics': self._generate_logistics_use_case(dataset_name, description),
            'traffic': self._generate_traffic_use_case(dataset_name, description)
        }
        
        selected_use_case = use_cases.get(focus_area, use_cases['smart_mobility'])
        
        if self.validate_use_case(selected_use_case):
            return selected_use_case
        else:
            return self._generate_fallback_use_case(dataset_name, description)
    
    def get_domain_keywords(self) -> List[str]:
        """Return transportation and mobility related keywords."""
        return [
            'transport', 'transportation', 'traffic', 'vehicle', 'car', 'truck',
            'bus', 'metro', 'train', 'railway', 'road', 'highway', 'street',
            'mobility', 'logistics', 'freight', 'cargo', 'shipping', 'delivery',
            'public transport', 'transit', 'commute', 'journey', 'route',
            'navigation', 'gps', 'mapping', 'fleet', 'aviation', 'airport',
            'port', 'maritime', 'bicycle', 'pedestrian', 'parking'
        ]
    
    def _determine_focus_area(self, description: str, keywords: List[str]) -> str:
        """Determine specific transportation focus area."""
        text = f"{description} {' '.join(keywords)}".lower()
        
        if any(kw in text for kw in ['smart', 'intelligent', 'autonomous', 'connected']):
            return 'smart_mobility'
        elif any(kw in text for kw in ['public', 'bus', 'metro', 'train', 'transit']):
            return 'public_transport'
        elif any(kw in text for kw in ['freight', 'cargo', 'logistics', 'delivery']):
            return 'logistics'
        elif any(kw in text for kw in ['traffic', 'congestion', 'flow', 'signal']):
            return 'traffic'
        else:
            return 'smart_mobility'
    
    def _generate_smart_mobility_use_case(self, dataset_name: str, description: str) -> Dict[str, Any]:
        """Generate smart mobility use case."""
        return {
            "title": "Integrated Smart Mobility Ecosystem",
            "objective": "Develop a comprehensive smart mobility platform supporting Vision 2030 smart city initiatives",
            "implementation": f"Leverage {dataset_name} to create intelligent transportation systems that optimize mobility flows and reduce congestion",
            "strategic_alignment": [
                "NEOM Smart City Development",
                "Vision 2030 Quality of Life Program",
                "Digital Transformation Initiative",
                "Sustainable Urban Development"
            ],
            "impact_areas": [
                "Urban Planning",
                "Traffic Optimization",
                "Environmental Impact",
                "Citizen Experience",
                "Economic Efficiency"
            ],
            "priority": "high",
            "timeline": "2024-2028",
            "resources_required": [
                "Ministry of Transport coordination",
                "Smart city technology platforms",
                "IoT infrastructure deployment",
                "Public-private partnerships",
                "Citizen engagement programs"
            ],
            "success_metrics": [
                "Average commute time reduction",
                "Traffic congestion index improvement",
                "Public transport ridership increase",
                "Carbon emissions reduction",
                "Citizen satisfaction scores"
            ]
        }
    
    def _generate_public_transport_use_case(self, dataset_name: str, description: str) -> Dict[str, Any]:
        """Generate public transport use case."""
        return {
            "title": "National Public Transport Optimization",
            "objective": "Enhance public transportation efficiency and accessibility to support sustainable urban mobility",
            "implementation": f"Utilize {dataset_name} to optimize routes, schedules, and capacity planning for public transport systems",
            "strategic_alignment": [
                "Riyadh Metro Project",
                "Public Transport Company development",
                "Sustainable mobility goals",
                "Urban connectivity improvement"
            ],
            "impact_areas": [
                "Public Service Quality",
                "Environmental Sustainability",
                "Social Equity",
                "Economic Development",
                "Urban Accessibility"
            ],
            "priority": "high",
            "timeline": "2024-2027",
            "resources_required": [
                "Public Transport Company",
                "Route optimization software",
                "Passenger information systems",
                "Fleet management platforms",
                "Community feedback mechanisms"
            ],
            "success_metrics": [
                "Public transport usage rates",
                "Service reliability indicators",
                "Passenger satisfaction scores",
                "Route efficiency metrics",
                "Accessibility coverage expansion"
            ]
        }
    
    def _generate_logistics_use_case(self, dataset_name: str, description: str) -> Dict[str, Any]:
        """Generate logistics use case."""
        return {
            "title": "National Logistics Hub Development",
            "objective": "Position Saudi Arabia as a global logistics hub connecting three continents",
            "implementation": f"Apply {dataset_name} to optimize freight movement, reduce logistics costs, and improve supply chain efficiency",
            "strategic_alignment": [
                "Vision 2030 Logistics Strategy",
                "Belt and Road Initiative participation",
                "Economic diversification goals",
                "Industrial sector competitiveness"
            ],
            "impact_areas": [
                "Trade Facilitation",
                "Economic Growth",
                "International Connectivity",
                "Industrial Development",
                "Employment Creation"
            ],
            "priority": "medium",
            "timeline": "2024-2029",
            "resources_required": [
                "Saudi Logistics Authority",
                "Port and airport authorities",
                "Private logistics companies",
                "Customs digitization systems",
                "International trade partnerships"
            ],
            "success_metrics": [
                "Logistics performance index ranking",
                "Freight movement efficiency",
                "Cross-border trade volume",
                "Logistics cost reduction",
                "Hub connectivity indicators"
            ]
        }
    
    def _generate_traffic_use_case(self, dataset_name: str, description: str) -> Dict[str, Any]:
        """Generate traffic management use case."""
        return {
            "title": "Intelligent Traffic Management System",
            "objective": "Implement AI-driven traffic management to reduce congestion and improve road safety",
            "implementation": f"Deploy {dataset_name} in smart traffic control systems for real-time optimization and predictive management",
            "strategic_alignment": [
                "Smart Cities Development",
                "Road safety improvement goals",
                "Environmental protection targets",
                "Digital government initiatives"
            ],
            "impact_areas": [
                "Traffic Flow Optimization",
                "Road Safety Enhancement",
                "Air Quality Improvement",
                "Economic Productivity",
                "Citizen Satisfaction"
            ],
            "priority": "medium",
            "timeline": "2024-2026",
            "resources_required": [
                "Traffic management authorities",
                "Smart traffic infrastructure",
                "AI analytics platforms",
                "Emergency response coordination",
                "Public awareness campaigns"
            ],
            "success_metrics": [
                "Traffic flow improvement rates",
                "Accident reduction percentage",
                "Emergency response times",
                "Fuel consumption reduction",
                "Air quality indicators"
            ]
        }
    
    def _generate_fallback_use_case(self, dataset_name: str, description: str) -> Dict[str, Any]:
        """Generate generic transportation use case."""
        return {
            "title": "Transportation Data Analytics Initiative",
            "objective": "Leverage transportation data for strategic planning and system optimization",
            "implementation": f"Implement analysis of {dataset_name} to support transportation sector strategic planning",
            "strategic_alignment": [
                "Vision 2030 Transportation Goals",
                "National Transportation Strategy",
                "Data-Driven Transportation Planning"
            ],
            "impact_areas": [
                "Strategic Planning",
                "System Optimization",
                "Transportation Management"
            ],
            "priority": "medium",
            "timeline": "2024-2025",
            "resources_required": [
                "Transportation analytics team",
                "Data processing infrastructure",
                "Stakeholder coordination"
            ],
            "success_metrics": [
                "Data utilization effectiveness",
                "Planning process improvement",
                "System performance indicators"
            ]
        }