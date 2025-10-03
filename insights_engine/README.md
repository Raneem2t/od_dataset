# 🧠 Insights Engine

**AI-Powered Government Data Intelligence Platform**

A sophisticated system designed to assist government entities with two core functions:
1. **Use Case Generation**: Transform dataset metadata into strategic use cases aligned with national objectives
2. **Open Data Publishing Recommendations**: Analyze global datasets and recommend strategic publishing opportunities

## 🌟 Features

### Use Case Generation
- **Mixture of Experts (MoE)** routing system with domain specialists
- **Context-aware processing** of dataset metadata
- **Strategic alignment** with Vision 2030 and national objectives
- **AI-powered analysis** with confidence scoring
- **Automated expert selection** based on domain relevance

### Open Data Publishing
- **Global dataset analysis** from 1.8M+ repository
- **Strategic matching** against entity scope and goals
- **Impact assessment** and priority scoring
- **Publishing plan generation** with resource estimates
- **Risk mitigation** strategies

### Technical Excellence
- **Modular architecture** with clean separation of concerns
- **RESTful API** with comprehensive endpoints
- **Professional web interface** with responsive design
- **Comprehensive logging** and audit trails
- **Configurable expert system** with extensible design

## 🏗️ Architecture

```
insights_engine/
├── app/
│   ├── experts/              # Domain expert classes
│   │   ├── base_expert.py    # Abstract base class
│   │   ├── energy_efficiency.py
│   │   └── transportation.py
│   ├── router.py             # Expert routing system
│   ├── context_engine.py     # Context processing
│   ├── data_loader.py        # Reference data management
│   └── publisher.py          # Open data recommendations
├── static/                   # Static web assets
├── templates/               # HTML templates
├── data/                    # Reference data files
├── logs/                    # Application logs
├── app.py                   # Flask application
├── config.py                # Configuration settings
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- (Optional) Redis for caching

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd insights_engine
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the interface:**
   - Web Interface: http://localhost:5000
   - API Documentation: http://localhost:5000/api/health

## 🔧 Configuration

### Environment Variables
```bash
# Optional API Keys
OPENAI_API_KEY=your_openai_api_key

# Flask Configuration
SECRET_KEY=your_secret_key
FLASK_ENV=development

# Redis (for production caching)
REDIS_URL=redis://localhost:6379/0
```

### Expert System Configuration
Experts can be configured in `config.py`:
```python
EXPERT_CONFIGURATIONS = {
    'energy_efficiency': {
        'enabled': True,
        'min_keyword_matches': 2,
        'strategic_weight': 0.8
    }
}
```

## 📊 API Endpoints

### Core Endpoints

#### Health Check
```http
GET /api/health
```

#### Generate Use Cases
```http
POST /api/use-cases/generate
Content-Type: application/json

{
  "name": "Renewable Energy Production Statistics",
  "description": "Monthly statistics of renewable energy production...",
  "keywords": ["renewable energy", "solar power", "sustainability"]
}
```

#### Analyze Publishing Opportunities
```http
POST /api/publishing/analyze
Content-Type: application/json

{
  "domain": "energy",
  "strategic_objectives": ["Vision 2030 energy diversification"],
  "capacity": {"datasets_per_quarter": 2}
}
```

#### Get Available Experts
```http
GET /api/experts
```

#### System Statistics
```http
GET /api/statistics
```

## 🎯 Expert System

### Available Experts

#### Energy Efficiency Expert
- **Domain**: Energy & Sustainability
- **Capabilities**: Renewable energy analysis, grid optimization, carbon footprint reduction
- **Strategic Focus**: Vision 2030 energy diversification, Saudi Green Initiative

#### Transportation Expert
- **Domain**: Transportation & Mobility
- **Capabilities**: Traffic optimization, smart mobility, logistics planning
- **Strategic Focus**: NEOM development, smart cities, logistics hub strategy

### Adding New Experts

1. **Create expert class:**
   ```python
   from app.experts.base_expert import BaseExpert
   
   class NewDomainExpert(BaseExpert):
       def __init__(self):
           super().__init__(
               name="New Domain Expert",
               domain="New Domain",
               capabilities=["capability1", "capability2"]
           )
       
       def can_handle(self, context):
           # Implementation
           pass
       
       def generate_use_case(self, context):
           # Implementation
           pass
   ```

2. **Register in router:**
   ```python
   # In app/router.py
   from .experts.new_domain import NewDomainExpert
   
   def _initialize_experts(self):
       self.experts = [
           EnergyEfficiencyExpert(),
           TransportationExpert(),
           NewDomainExpert()  # Add here
       ]
   ```

## 📈 Data Flow

### Use Case Generation Flow
1. **Input Processing**: Receive dataset metadata
2. **Context Enrichment**: Extract keywords, classify domains, assess alignment
3. **Expert Routing**: Select relevant domain experts
4. **Use Case Generation**: Generate strategic use cases
5. **Validation**: Validate output structure and quality
6. **Response**: Return use cases with routing information

### Publishing Recommendation Flow
1. **Scope Analysis**: Analyze entity domain and strategic objectives
2. **Global Matching**: Match against 1.8M+ global dataset repository
3. **Strategic Scoring**: Score datasets by strategic alignment
4. **Impact Assessment**: Evaluate publishing impact and risks
5. **Plan Generation**: Create phased implementation plan

## 🧪 Testing

### Run Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Coverage report
pytest --cov=app tests/
```

### Manual Testing
```bash
# Test use case generation
curl -X POST http://localhost:5000/api/use-cases/generate \\
     -H "Content-Type: application/json" \\
     -d '{"name":"Solar Energy Data","description":"Solar panel production data","keywords":["solar","renewable"]}'

# Test expert information
curl http://localhost:5000/api/experts
```

## 🔒 Security Considerations

- **Data Privacy**: No sensitive data is stored permanently
- **Input Validation**: All API inputs are validated
- **Error Handling**: Comprehensive error handling without data leakage
- **Logging**: Secure logging with no sensitive information
- **CORS**: Configurable CORS policies for different environments

## 📋 Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Setup
- Configure production database
- Setup Redis for caching
- Configure proper logging
- Setup monitoring and health checks

## 🔍 Monitoring

### Health Checks
- **Application**: `/api/health`
- **Database**: Connection status
- **Cache**: Redis connectivity
- **External APIs**: OpenAI API status

### Logging
- **Application Logs**: `logs/insights_engine.log`
- **Routing Logs**: `logs/routing_log_*.json`
- **Audit Logs**: Comprehensive audit trail

### Metrics
- Use case generation rate
- Expert routing statistics
- API response times
- Error rates

## 🤝 Contributing

### Development Guidelines
1. Follow PEP 8 style guidelines
2. Write comprehensive tests
3. Update documentation
4. Use type hints
5. Add logging for important operations

### Code Quality
```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## 📚 Reference Data

The system expects reference data files in the `data/` directory:
- **Expert Configurations**: Expert roles and capabilities
- **Strategic Framework**: National strategic objectives
- **Domain Mappings**: Keyword mappings for classification
- **Templates**: Use case and output templates
- **Examples**: Sample inputs and outputs

If reference files are not available, the system will create sample files automatically.

## 🆘 Troubleshooting

### Common Issues

#### "No experts available"
- Check expert configuration in `config.py`
- Verify expert classes are properly imported
- Check logs for initialization errors

#### "Context validation failed"
- Ensure required fields (name, description) are provided
- Check input data format
- Verify context processing configuration

#### "Failed to load reference data"
- Check `data/` directory exists
- Verify file permissions
- Review data loader logs

### Debug Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

## 📄 License

Government Internal Use - Restricted Distribution

## 📞 Support

For technical support and questions:
- **Documentation**: Check this README and inline code documentation
- **Logs**: Review application logs in `logs/` directory
- **Configuration**: Verify settings in `config.py`
- **Testing**: Run test suite to verify functionality

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Compatibility**: Python 3.8+, Flask 2.3+