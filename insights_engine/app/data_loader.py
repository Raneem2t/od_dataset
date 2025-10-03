"""
Data Loader - Loads and manages reference data files for the Insights Engine
"""

import json
import os
from typing import Dict, Any, List, Optional
import logging


class DataLoader:
    """
    Loads and manages reference data files including expert configurations,
    templates, and strategic frameworks.
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.logger = logging.getLogger('data_loader')
        self._loaded_data = {}
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    
    def load_expert_configurations(self) -> Dict[str, Any]:
        """Load expert roles, responsibilities, and capabilities."""
        config_files = [
            "01_Expert_Roles_and_Responsibilities.txt",
            "02_Expert_Capabilities.txt"
        ]
        
        configurations = {}
        for filename in config_files:
            try:
                content = self._load_text_file(filename)
                if content:
                    key = filename.split('_', 1)[1].replace('.txt', '').lower()
                    configurations[key] = content
            except Exception as e:
                self.logger.warning(f"Could not load {filename}: {str(e)}")
        
        return configurations
    
    def load_strategic_framework(self) -> Dict[str, Any]:
        """Load strategy and objectives framework."""
        try:
            content = self._load_text_file("03_Strategy_and_Objectives.txt")
            return {"strategic_framework": content} if content else {}
        except Exception as e:
            self.logger.warning(f"Could not load strategic framework: {str(e)}")
            return {}
    
    def load_templates(self) -> Dict[str, Any]:
        """Load use case and output templates."""
        templates = {}
        
        template_files = [
            "04_UseCase_Template.txt",
            "11_Prompt_Template_for_LLM.txt"
        ]
        
        for filename in template_files:
            try:
                content = self._load_text_file(filename)
                if content:
                    key = filename.split('_', 1)[1].replace('.txt', '').replace('_', '').lower()
                    templates[key] = content
            except Exception as e:
                self.logger.warning(f"Could not load template {filename}: {str(e)}")
        
        return templates
    
    def load_domain_mappings(self) -> Dict[str, Any]:
        """Load domain keyword mappings and classification rules."""
        mappings = {}
        
        try:
            # Load domain keyword mapping
            domain_keywords = self._load_json_file("06_Domain_Keyword_Mapping.json")
            if domain_keywords:
                mappings["domain_keywords"] = domain_keywords
        except Exception as e:
            self.logger.warning(f"Could not load domain keywords: {str(e)}")
        
        try:
            # Load classification rules
            classification_rules = self._load_text_file("07_Dataset_Classification_Rules.txt")
            if classification_rules:
                mappings["classification_rules"] = classification_rules
        except Exception as e:
            self.logger.warning(f"Could not load classification rules: {str(e)}")
        
        return mappings
    
    def load_workflow_configurations(self) -> Dict[str, Any]:
        """Load workflow and routing configurations."""
        workflows = {}
        
        workflow_files = [
            "09_Context_Engineering_Workflow.txt",
            "10_Router_Workflow_and_Logic.txt",
            "03_Publishing_Strategy_Routing.txt"
        ]
        
        for filename in workflow_files:
            try:
                content = self._load_text_file(filename)
                if content:
                    key = filename.split('_', 1)[1].replace('.txt', '').replace('_', '').lower()
                    workflows[key] = content
            except Exception as e:
                self.logger.warning(f"Could not load workflow {filename}: {str(e)}")
        
        return workflows
    
    def load_log_formats(self) -> Dict[str, Any]:
        """Load log format templates."""
        log_formats = {}
        
        log_format_files = [
            "12_Routing_Log_Format.json",
            "13_Output_Audit_Log_Format.json",
            "06_Publishing_Output_Log_Format.json"
        ]
        
        for filename in log_format_files:
            try:
                content = self._load_json_file(filename)
                if content:
                    key = filename.split('_', 1)[1].replace('.json', '').replace('_', '').lower()
                    log_formats[key] = content
            except Exception as e:
                self.logger.warning(f"Could not load log format {filename}: {str(e)}")
        
        return log_formats
    
    def load_publishing_configurations(self) -> Dict[str, Any]:
        """Load open data publishing configurations."""
        publishing_config = {}
        
        publishing_files = [
            "00_Model_Overview_OpenData.txt",
            "01_Publishing_Recommendation_Template.txt",
            "02_Publishing_Evaluation_Criteria.txt",
            "04_Publishing_Matching_Logic.txt"
        ]
        
        for filename in publishing_files:
            try:
                content = self._load_text_file(filename)
                if content:
                    key = filename.split('_', 1)[1].replace('.txt', '').replace('_', '').lower()
                    publishing_config[key] = content
            except Exception as e:
                self.logger.warning(f"Could not load publishing config {filename}: {str(e)}")
        
        return publishing_config
    
    def load_example_data(self) -> Dict[str, Any]:
        """Load example inputs and outputs."""
        examples = {}
        
        example_files = [
            "05_Example_Input_Metadata.json",
            "05_Example_Recommendation_Input.json"
        ]
        
        for filename in example_files:
            try:
                content = self._load_json_file(filename)
                if content:
                    key = filename.split('_', 1)[1].replace('.json', '').replace('_', '').lower()
                    examples[key] = content
            except Exception as e:
                self.logger.warning(f"Could not load example {filename}: {str(e)}")
        
        return examples
    
    def load_all_reference_data(self) -> Dict[str, Any]:
        """Load all reference data files."""
        all_data = {}
        
        loaders = [
            ("expert_configurations", self.load_expert_configurations),
            ("strategic_framework", self.load_strategic_framework),
            ("templates", self.load_templates),
            ("domain_mappings", self.load_domain_mappings),
            ("workflow_configurations", self.load_workflow_configurations),
            ("log_formats", self.load_log_formats),
            ("publishing_configurations", self.load_publishing_configurations),
            ("example_data", self.load_example_data)
        ]
        
        for key, loader_func in loaders:
            try:
                data = loader_func()
                if data:
                    all_data[key] = data
                    self.logger.info(f"Loaded {key}: {len(data)} items")
            except Exception as e:
                self.logger.error(f"Failed to load {key}: {str(e)}")
        
        self._loaded_data = all_data
        return all_data
    
    def get_loaded_data(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Get loaded data by category or all data."""
        if category:
            return self._loaded_data.get(category, {})
        return self._loaded_data
    
    def create_sample_data_files(self):
        """Create sample data files for testing when reference files are not available."""
        sample_files = {
            "06_Domain_Keyword_Mapping.json": {
                "energy": ["renewable", "solar", "wind", "efficiency", "grid", "power"],
                "transportation": ["traffic", "mobility", "vehicle", "transit", "logistics"],
                "healthcare": ["medical", "health", "hospital", "patient", "treatment"],
                "education": ["school", "university", "student", "learning", "academic"],
                "environment": ["climate", "pollution", "conservation", "sustainability"],
                "economic": ["economy", "finance", "trade", "business", "investment"]
            },
            "05_Example_Input_Metadata.json": {
                "name": "Renewable Energy Production Statistics",
                "description": "Monthly statistics of renewable energy production across Saudi Arabia including solar, wind, and other clean energy sources.",
                "keywords": ["renewable energy", "solar power", "wind energy", "clean energy", "sustainability"]
            },
            "12_Routing_Log_Format.json": {
                "timestamp": "ISO datetime",
                "dataset_name": "string",
                "routing_decisions": [
                    {
                        "expert_name": "string",
                        "expert_domain": "string",
                        "can_handle": "boolean",
                        "alignment_score": "float",
                        "decision_timestamp": "ISO datetime"
                    }
                ],
                "selected_experts": [
                    {
                        "name": "string",
                        "domain": "string",
                        "capabilities": ["array of strings"]
                    }
                ],
                "routing_strategy": "string"
            }
        }
        
        for filename, content in sample_files.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(content, f, indent=2, ensure_ascii=False)
                    self.logger.info(f"Created sample file: {filename}")
                except Exception as e:
                    self.logger.error(f"Failed to create sample file {filename}: {str(e)}")
    
    def _load_text_file(self, filename: str) -> Optional[str]:
        """Load content from a text file."""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            self.logger.error(f"Error reading {filename}: {str(e)}")
            return None
    
    def _load_json_file(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load content from a JSON file."""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error reading {filename}: {str(e)}")
            return None
    
    def save_data(self, data: Dict[str, Any], filename: str, is_json: bool = True):
        """Save data to a file."""
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if is_json:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    f.write(str(data))
            
            self.logger.info(f"Saved data to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save data to {filename}: {str(e)}")
    
    def get_data_file_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all expected data files."""
        expected_files = {
            "text_files": [
                "00_Model_Overview.txt",
                "01_Expert_Roles_and_Responsibilities.txt",
                "02_Expert_Capabilities.txt",
                "03_Strategy_and_Objectives.txt",
                "04_UseCase_Template.txt",
                "07_Dataset_Classification_Rules.txt",
                "08_Contextual_Constraints.txt",
                "09_Context_Engineering_Workflow.txt",
                "10_Router_Workflow_and_Logic.txt",
                "11_Prompt_Template_for_LLM.txt",
                "00_Model_Overview_OpenData.txt",
                "01_Publishing_Recommendation_Template.txt",
                "02_Publishing_Evaluation_Criteria.txt",
                "03_Publishing_Strategy_Routing.txt",
                "04_Publishing_Matching_Logic.txt"
            ],
            "json_files": [
                "05_Example_Input_Metadata.json",
                "06_Domain_Keyword_Mapping.json",
                "12_Routing_Log_Format.json",
                "13_Output_Audit_Log_Format.json",
                "05_Example_Recommendation_Input.json",
                "06_Publishing_Output_Log_Format.json"
            ]
        }
        
        status = {
            "total_files": 0,
            "existing_files": 0,
            "missing_files": [],
            "file_details": {}
        }
        
        for file_type, files in expected_files.items():
            for filename in files:
                status["total_files"] += 1
                filepath = os.path.join(self.data_dir, filename)
                
                if os.path.exists(filepath):
                    status["existing_files"] += 1
                    try:
                        file_size = os.path.getsize(filepath)
                        status["file_details"][filename] = {
                            "exists": True,
                            "size": file_size,
                            "type": file_type
                        }
                    except Exception as e:
                        status["file_details"][filename] = {
                            "exists": True,
                            "error": str(e),
                            "type": file_type
                        }
                else:
                    status["missing_files"].append(filename)
                    status["file_details"][filename] = {
                        "exists": False,
                        "type": file_type
                    }
        
        return status