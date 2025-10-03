"""
Insights Engine Flask Application
Main application entry point for the AI-Powered Government Data Intelligence Platform
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import logging
import os
from datetime import datetime

from app.router import ExpertRouter
from app.context_engine import ContextEngine
from app.data_loader import DataLoader
from app.publisher import OpenDataPublisher


def create_app(config_name='development'):
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__, 
                static_folder='static', 
                template_folder='templates')
    
    # Enable CORS for frontend integration
    CORS(app)
    
    # Load configuration
    app.config.from_object(f'config.{config_name.title()}Config')
    
    # Setup logging
    setup_logging(app)
    
    # Initialize components
    expert_router = ExpertRouter()
    context_engine = ContextEngine()
    data_loader = DataLoader()
    publisher = OpenDataPublisher()
    
    # Load reference data
    try:
        data_loader.create_sample_data_files()  # Create sample files if needed
        reference_data = data_loader.load_all_reference_data()
        app.logger.info(f"Loaded reference data: {list(reference_data.keys())}")
    except Exception as e:
        app.logger.error(f"Failed to load reference data: {str(e)}")
    
    # Routes
    @app.route('/')
    def index():
        """Serve the main interface."""
        return send_from_directory('../', 'index.html')
    
    @app.route('/usecase.html')
    def usecase_page():
        """Serve the use case generation page."""
        return send_from_directory('../', 'usecase.html')
    
    @app.route('/publishing.html')
    def publishing_page():
        """Serve the publishing recommendations page."""
        return send_from_directory('../', 'publishing.html')
    
    @app.route('/style.css')
    def styles():
        """Serve the stylesheet."""
        return send_from_directory('../', 'style.css')
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {
                "expert_router": "active",
                "context_engine": "active",
                "data_loader": "active",
                "publisher": "active"
            }
        })
    
    @app.route('/api/experts', methods=['GET'])
    def get_experts():
        """Get information about available experts."""
        try:
            experts_info = expert_router.get_available_experts()
            return jsonify({
                "experts": experts_info,
                "total_count": len(experts_info),
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            app.logger.error(f"Error getting experts info: {str(e)}")
            return jsonify({"error": "Failed to retrieve experts information"}), 500
    
    @app.route('/api/use-cases/generate', methods=['POST'])
    def generate_use_cases():
        """Generate use cases from dataset metadata."""
        try:
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
            app.logger.info(f"Processing dataset: {input_data['name']}")
            enriched_context = context_engine.process_context(input_data)
            
            # Validate context
            validation_results = context_engine.validate_context(enriched_context)
            
            if not validation_results['is_valid']:
                return jsonify({
                    "error": "Context validation failed",
                    "validation_errors": validation_results['errors']
                }), 400
            
            # Generate use cases
            results = expert_router.generate_use_cases(enriched_context)
            
            # Save routing log
            try:
                expert_router.save_routing_log(results['routing_log'])
            except Exception as e:
                app.logger.warning(f"Failed to save routing log: {str(e)}")
            
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
            
            app.logger.info(f"Generated {len(results['use_cases'])} use cases for dataset: {input_data['name']}")
            return jsonify(response)
            
        except Exception as e:
            app.logger.error(f"Error generating use cases: {str(e)}")
            return jsonify({
                "error": "Failed to generate use cases",
                "details": str(e)
            }), 500
    
    @app.route('/api/publishing/analyze', methods=['POST'])
    def analyze_publishing_opportunities():
        """Analyze publishing opportunities for government entity."""
        try:
            # Get entity scope
            entity_scope = request.get_json()
            
            if not entity_scope:
                return jsonify({"error": "No entity scope provided"}), 400
            
            # Analyze opportunities
            app.logger.info(f"Analyzing publishing opportunities for domain: {entity_scope.get('domain', 'unknown')}")
            analysis_results = publisher.analyze_publishing_opportunities(entity_scope)
            
            # Generate publishing plan if recommendations exist
            publishing_plan = None
            if analysis_results['recommendations']:
                entity_capacity = entity_scope.get('capacity', {"datasets_per_quarter": 2})
                publishing_plan = publisher.generate_publishing_plan(
                    analysis_results['recommendations'], 
                    entity_capacity
                )
            
            response = {
                "success": True,
                "analysis_results": analysis_results,
                "publishing_plan": publishing_plan,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            app.logger.info(f"Generated {len(analysis_results['recommendations'])} publishing recommendations")
            return jsonify(response)
            
        except Exception as e:
            app.logger.error(f"Error analyzing publishing opportunities: {str(e)}")
            return jsonify({
                "error": "Failed to analyze publishing opportunities",
                "details": str(e)
            }), 500
    
    @app.route('/api/publishing/evaluate', methods=['POST'])
    def evaluate_dataset_publishing():
        """Evaluate a specific dataset for publishing impact."""
        try:
            # Get evaluation request
            eval_request = request.get_json()
            
            if not eval_request:
                return jsonify({"error": "No evaluation request provided"}), 400
            
            dataset_metadata = eval_request.get('dataset_metadata', {})
            entity_scope = eval_request.get('entity_scope', {})
            
            if not dataset_metadata:
                return jsonify({"error": "No dataset metadata provided"}), 400
            
            # Evaluate publishing impact
            app.logger.info(f"Evaluating dataset: {dataset_metadata.get('name', 'unknown')}")
            evaluation_results = publisher.evaluate_publishing_impact(dataset_metadata, entity_scope)
            
            response = {
                "success": True,
                "evaluation": evaluation_results,
                "evaluation_timestamp": datetime.now().isoformat()
            }
            
            return jsonify(response)
            
        except Exception as e:
            app.logger.error(f"Error evaluating dataset: {str(e)}")
            return jsonify({
                "error": "Failed to evaluate dataset",
                "details": str(e)
            }), 500
    
    @app.route('/api/data/status', methods=['GET'])
    def data_status():
        """Get status of reference data files."""
        try:
            status = data_loader.get_data_file_status()
            return jsonify({
                "data_status": status,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            app.logger.error(f"Error getting data status: {str(e)}")
            return jsonify({"error": "Failed to get data status"}), 500
    
    @app.route('/api/statistics', methods=['GET'])
    def get_statistics():
        """Get system statistics and performance metrics."""
        try:
            routing_stats = expert_router.get_routing_statistics()
            
            statistics = {
                "system_info": {
                    "version": "1.0.0",
                    "uptime": "Available since startup",
                    "total_components": 4
                },
                "expert_system": routing_stats,
                "data_loader": {
                    "loaded_categories": len(data_loader.get_loaded_data()),
                    "status": "active"
                },
                "timestamp": datetime.now().isoformat()
            }
            
            return jsonify(statistics)
            
        except Exception as e:
            app.logger.error(f"Error getting statistics: {str(e)}")
            return jsonify({"error": "Failed to get statistics"}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({"error": "Endpoint not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        app.logger.error(f"Internal server error: {str(error)}")
        return jsonify({"error": "Internal server error"}), 500
    
    return app


def setup_logging(app):
    """Setup application logging."""
    if not app.debug:
        # Create logs directory
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Setup file handler
        file_handler = logging.FileHandler('logs/insights_engine.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Insights Engine startup')


if __name__ == '__main__':
    # Create and run the application
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)