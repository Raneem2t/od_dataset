"""
Context Engineering Engine - Processes and enriches dataset metadata for expert routing
"""

from typing import Dict, List, Any, Optional
import re
import logging
from datetime import datetime


class ContextEngine:
    """
    Processes dataset metadata and enriches it with contextual information
    for intelligent expert routing and use case generation.
    """
    
    def __init__(self):
        self.logger = logging.getLogger('context_engine')
        self.domain_keywords = self._load_domain_keywords()
        self.strategic_keywords = self._load_strategic_keywords()
    
    def process_context(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and enrich dataset metadata with contextual information.
        
        Args:
            metadata: Raw dataset metadata
                - name: Dataset name
                - description: Dataset description
                - keywords: List of keywords (optional)
        
        Returns:
            Enriched context dictionary
        """
        context = {
            "name": metadata.get("name", ""),
            "description": metadata.get("description", ""),
            "keywords": metadata.get("keywords", []),
            "processing_timestamp": datetime.now().isoformat()
        }
        
        # Clean and normalize text
        context["normalized_name"] = self._normalize_text(context["name"])
        context["normalized_description"] = self._normalize_text(context["description"])
        context["normalized_keywords"] = [self._normalize_text(kw) for kw in context["keywords"]]
        
        # Extract additional keywords from description
        context["extracted_keywords"] = self._extract_keywords(context["description"])
        
        # Classify domain(s)
        context["domain_classification"] = self._classify_domains(context)
        
        # Assess strategic alignment
        context["strategic_alignment"] = self._assess_strategic_alignment(context)
        
        # Identify government focus areas
        context["government_focus_areas"] = self._identify_focus_areas(context)
        
        # Calculate content richness
        context["content_richness"] = self._calculate_content_richness(context)
        
        # Add processing metadata
        context["processing_metadata"] = {
            "engine_version": "1.0.0",
            "processing_timestamp": context["processing_timestamp"],
            "confidence_score": self._calculate_confidence_score(context)
        }
        
        self.logger.info(f"Processed context for dataset: {context['name']}")
        return context
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better processing."""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep alphanumeric and basic punctuation
        text = re.sub(r'[^\w\s\-\.]', ' ', text)
        
        return text
    
    def _extract_keywords(self, description: str) -> List[str]:
        """Extract relevant keywords from description."""
        if not description:
            return []
        
        # Simple keyword extraction based on domain knowledge
        extracted = []
        normalized_desc = self._normalize_text(description)
        
        # Check against domain keywords
        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword in normalized_desc and keyword not in extracted:
                    extracted.append(keyword)
        
        # Extract potential technical terms (words with specific patterns)
        technical_terms = re.findall(r'\b[a-z]+(?:_[a-z]+)*\b', normalized_desc)
        for term in technical_terms:
            if len(term) > 3 and term not in extracted:
                extracted.append(term)
        
        return extracted[:10]  # Limit to top 10 extracted keywords
    
    def _classify_domains(self, context: Dict[str, Any]) -> List[str]:
        """Classify the dataset into relevant domains."""
        text_content = f"{context['normalized_name']} {context['normalized_description']} {' '.join(context['normalized_keywords'])}"
        
        domain_scores = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_content:
                    score += 1
            
            if score > 0:
                domain_scores[domain] = score
        
        # Return domains with scores above threshold
        threshold = 1
        classified_domains = [domain for domain, score in domain_scores.items() if score >= threshold]
        
        return classified_domains if classified_domains else ["general"]
    
    def _assess_strategic_alignment(self, context: Dict[str, Any]) -> float:
        """Assess alignment with national strategic objectives."""
        text_content = f"{context['normalized_name']} {context['normalized_description']} {' '.join(context['normalized_keywords'])}"
        
        alignment_score = 0.0
        total_strategic_keywords = len(self.strategic_keywords)
        
        if total_strategic_keywords == 0:
            return 0.5  # Default neutral score
        
        for keyword in self.strategic_keywords:
            if keyword in text_content:
                alignment_score += 1.0
        
        # Normalize score to 0-1 range
        normalized_score = min(1.0, alignment_score / (total_strategic_keywords * 0.3))
        
        # Boost score for high-priority domains
        high_priority_domains = ["energy", "healthcare", "education", "transportation"]
        domain_boost = 0.1 if any(domain in context.get("domain_classification", []) 
                                 for domain in high_priority_domains) else 0.0
        
        return min(1.0, normalized_score + domain_boost)
    
    def _identify_focus_areas(self, context: Dict[str, Any]) -> List[str]:
        """Identify government focus areas relevant to the dataset."""
        focus_areas = []
        text_content = f"{context['normalized_name']} {context['normalized_description']}".lower()
        
        focus_area_keywords = {
            "digital_transformation": ["digital", "technology", "automation", "ai", "artificial intelligence", "smart"],
            "sustainability": ["renewable", "green", "sustainable", "environment", "carbon", "climate"],
            "economic_diversification": ["economy", "business", "industry", "manufacturing", "commerce"],
            "social_development": ["social", "community", "welfare", "development", "quality of life"],
            "infrastructure": ["infrastructure", "construction", "transport", "utilities", "telecommunications"],
            "innovation": ["innovation", "research", "development", "technology", "startup"],
            "transparency": ["transparency", "open", "public", "accountability", "governance"]
        }
        
        for area, keywords in focus_area_keywords.items():
            if any(keyword in text_content for keyword in keywords):
                focus_areas.append(area)
        
        return focus_areas
    
    def _calculate_content_richness(self, context: Dict[str, Any]) -> float:
        """Calculate the richness of the dataset content."""
        name_length = len(context.get("name", ""))
        desc_length = len(context.get("description", ""))
        keyword_count = len(context.get("keywords", []))
        extracted_keyword_count = len(context.get("extracted_keywords", []))
        
        # Calculate richness score
        richness_score = 0.0
        
        # Name quality (0-0.2)
        if name_length > 10:
            richness_score += 0.2
        elif name_length > 5:
            richness_score += 0.1
        
        # Description quality (0-0.4)
        if desc_length > 200:
            richness_score += 0.4
        elif desc_length > 100:
            richness_score += 0.3
        elif desc_length > 50:
            richness_score += 0.2
        elif desc_length > 20:
            richness_score += 0.1
        
        # Keyword availability (0-0.4)
        total_keywords = keyword_count + extracted_keyword_count
        if total_keywords > 10:
            richness_score += 0.4
        elif total_keywords > 5:
            richness_score += 0.3
        elif total_keywords > 2:
            richness_score += 0.2
        elif total_keywords > 0:
            richness_score += 0.1
        
        return min(1.0, richness_score)
    
    def _calculate_confidence_score(self, context: Dict[str, Any]) -> float:
        """Calculate confidence in the context processing."""
        factors = []
        
        # Content richness factor
        factors.append(context.get("content_richness", 0.5))
        
        # Domain classification confidence
        domain_count = len(context.get("domain_classification", []))
        domain_confidence = min(1.0, domain_count / 3.0) if domain_count > 0 else 0.3
        factors.append(domain_confidence)
        
        # Strategic alignment confidence
        strategic_alignment = context.get("strategic_alignment", 0.5)
        factors.append(strategic_alignment)
        
        # Keywords availability
        total_keywords = len(context.get("keywords", [])) + len(context.get("extracted_keywords", []))
        keyword_confidence = min(1.0, total_keywords / 5.0) if total_keywords > 0 else 0.2
        factors.append(keyword_confidence)
        
        # Calculate weighted average
        return sum(factors) / len(factors)
    
    def _load_domain_keywords(self) -> Dict[str, List[str]]:
        """Load domain-specific keywords for classification."""
        return {
            "energy": [
                "energy", "renewable", "solar", "wind", "hydroelectric", "nuclear",
                "electricity", "power", "grid", "consumption", "efficiency", "carbon",
                "fuel", "oil", "gas", "coal", "biomass", "geothermal"
            ],
            "healthcare": [
                "health", "medical", "hospital", "patient", "disease", "treatment",
                "medicine", "clinical", "healthcare", "wellness", "epidemiology",
                "pharmacy", "surgery", "diagnosis", "therapy"
            ],
            "transportation": [
                "transport", "traffic", "vehicle", "road", "railway", "aviation",
                "shipping", "logistics", "mobility", "infrastructure", "transit",
                "automotive", "public transport", "freight"
            ],
            "education": [
                "education", "school", "university", "student", "teacher", "learning",
                "curriculum", "academic", "training", "knowledge", "skill", "literacy"
            ],
            "environment": [
                "environment", "climate", "weather", "pollution", "ecosystem",
                "biodiversity", "conservation", "sustainability", "green", "clean"
            ],
            "economic": [
                "economy", "finance", "business", "trade", "industry", "commerce",
                "investment", "market", "economic", "financial", "banking", "gdp"
            ],
            "social": [
                "social", "community", "population", "demographic", "welfare",
                "housing", "employment", "poverty", "inequality", "development"
            ]
        }
    
    def _load_strategic_keywords(self) -> List[str]:
        """Load keywords related to national strategic objectives."""
        return [
            "vision 2030", "digital transformation", "smart city", "innovation",
            "sustainability", "diversification", "renewable energy", "efficiency",
            "transparency", "governance", "public service", "economic growth",
            "social development", "infrastructure", "technology", "artificial intelligence",
            "automation", "green initiative", "carbon neutral", "climate change"
        ]
    
    def validate_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the processed context and return validation results.
        
        Args:
            context: Processed context dictionary
        
        Returns:
            Validation results dictionary
        """
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "quality_score": 0.0
        }
        
        # Required fields validation
        required_fields = ["name", "description"]
        for field in required_fields:
            if not context.get(field):
                validation_results["errors"].append(f"Missing required field: {field}")
                validation_results["is_valid"] = False
        
        # Quality checks
        if len(context.get("description", "")) < 20:
            validation_results["warnings"].append("Description is very short")
        
        if not context.get("keywords") and not context.get("extracted_keywords"):
            validation_results["warnings"].append("No keywords available")
        
        if not context.get("domain_classification"):
            validation_results["warnings"].append("No domain classification available")
        
        # Calculate quality score
        quality_factors = [
            context.get("content_richness", 0.0),
            context.get("strategic_alignment", 0.0),
            context.get("processing_metadata", {}).get("confidence_score", 0.0)
        ]
        validation_results["quality_score"] = sum(quality_factors) / len(quality_factors)
        
        return validation_results