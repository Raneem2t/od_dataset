#!/usr/bin/env python3
"""
Simple run script for Insights Engine
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
from datetime import datetime

from app.router import ExpertRouter
from app.context_engine import ContextEngine
from app.data_loader import DataLoader
from app.publisher import OpenDataPublisher

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configure app
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'insights-engine-secret-key-2024'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
try:
    expert_router = ExpertRouter()
    context_engine = ContextEngine()
    data_loader = DataLoader()
    publisher = OpenDataPublisher()
    
    # Create sample data files
    data_loader.create_sample_data_files()
    logger.info("Insights Engine components initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize components: {str(e)}")
    expert_router = None
    context_engine = None
    data_loader = None
    publisher = None

# Routes
@app.route('/')
def index():
    """Serve the main interface."""
    return send_from_directory('.', 'index.html')

@app.route('/usecase.html')
def usecase_page():
    """Serve the use case generation page."""
    return send_from_directory('.', 'usecase.html')

@app.route('/publishing.html')
def publishing_page():
    """Serve the publishing recommendations page."""
    return send_from_directory('.', 'publishing.html')

@app.route('/style.css')
def styles():
    """Serve the stylesheet."""
    return send_from_directory('.', 'style.css')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "components": {
            "expert_router": "active" if expert_router else "error",
            "context_engine": "active" if context_engine else "error",
            "data_loader": "active" if data_loader else "error",
            "publisher": "active" if publisher else "error"
        }
    })

@app.route('/api/experts', methods=['GET'])
def get_experts():
    """Get information about available experts."""
    try:
        if not expert_router:
            return jsonify({"error": "Expert router not initialized"}), 500
            
        experts_info = expert_router.get_available_experts()
        return jsonify({
            "experts": experts_info,
            "total_count": len(experts_info),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting experts info: {str(e)}")
        return jsonify({"error": "Failed to retrieve experts information"}), 500

@app.route('/api/use-cases/generate', methods=['POST'])
def generate_use_cases():
    """Generate use cases from dataset metadata."""
    try:
        if not expert_router or not context_engine:
            return jsonify({"error": "System components not initialized"}), 500
        
        # Get input data
        input_data = request.get_json()
        
        if not input_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validate required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if not input_data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Process context
        logger.info(f"Processing dataset: {input_data['name']}")
        enriched_context = context_engine.process_context(input_data)
        
        # Generate use cases
        results = expert_router.generate_use_cases(enriched_context)
        
        # Prepare response
        response = {
            "success": True,
            "use_cases": results['use_cases'],
            "routing_info": {
                "experts_used": len(results['routing_log']['selected_experts']),
                "selected_experts": [expert['name'] for expert in results['routing_log']['selected_experts']],
                "routing_strategy": results['routing_log']['routing_strategy']
            },
            "context_info": {
                "domain_classification": enriched_context.get('domain_classification', []),
                "strategic_alignment": enriched_context.get('strategic_alignment', 0.0),
                "content_richness": enriched_context.get('content_richness', 0.0)
            },
            "generation_timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Generated {len(results['use_cases'])} use cases for dataset: {input_data['name']}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error generating use cases: {str(e)}")
        return jsonify({
            "error": "Failed to generate use cases",
            "details": str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics."""
    try:
        stats = {
            "system_info": {
                "version": "1.0.0",
                "status": "running",
                "components_initialized": bool(expert_router and context_engine and data_loader)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        if expert_router:
            stats["expert_system"] = expert_router.get_routing_statistics()
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({"error": "Failed to get statistics"}), 500

if __name__ == '__main__':
    print("🧠 Starting Insights Engine...")
    print("📍 Access the application at: http://127.0.0.1:8080")
    print("🔧 API Health Check: http://127.0.0.1:8080/api/health")
    print("👥 Available Experts: http://127.0.0.1:8080/api/experts")
    
    app.run(debug=True, host='127.0.0.1', port=8080)