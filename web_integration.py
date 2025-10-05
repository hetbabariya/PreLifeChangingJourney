"""
Web Integration for AI Insights Generator
Flask web server to integrate AI insights with the psychological testing platform
"""

from flask import Flask, request, jsonify, send_from_directory, send_file, make_response
from flask_cors import CORS
import json
import os
from datetime import datetime
from ai_insights_gemini import AIInsightsGenerator
from markdown_pdf_generator import generate_pdf_report

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for frontend integration

# Initialize AI insights generator
ai_generator = None

try:
    ai_generator = AIInsightsGenerator()
    print("AI Insights Generator initialized successfully")
except Exception as e:
    print(f"Warning: AI Insights Generator failed to initialize: {e}")

@app.route('/')
def index():
    """Serve the main testing platform"""
    try:
        return send_file('index.html')
    except FileNotFoundError:
        return "Testing platform not found. Please ensure index.html exists."

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    try:
        return send_from_directory('.', filename)
    except FileNotFoundError:
        return f"File {filename} not found", 404

@app.route('/api/generate-insights', methods=['POST'])
def generate_insights():
    """
    API endpoint to generate AI insights based on test results
    
    Expected JSON payload:
    {
        "testResults": {
            "mbtiScreen": "selected_option_text",
            "intelligenceScreen": "selected_option_text",
            "bigFiveScreen": "selected_option_text",
            "riasecScreen": "selected_option_text",
            "decisionScreen": "selected_option_text",
            "lifeScreen": "selected_option_text",
            "varkScreen": "selected_option_text"
        }
    }
    """
    try:
        # Get test results from request
        data = request.get_json()
        
        if not data or 'testResults' not in data:
            return jsonify({
                'error': 'Invalid request. testResults required.',
                'success': False
            }), 400
        
        test_results = data['testResults']
        
        # Validate that we have test results
        if not test_results:
            return jsonify({
                'error': 'No test results provided.',
                'success': False
            }), 400
        
        # Convert test results to structured format for AI analysis
        structured_results = convert_to_structured_format(test_results)
        
        # Generate insights using AI (no fallbacks)
        if not ai_generator:
            return jsonify({
                'error': 'AI service is not available. Please check your API configuration.',
                'success': False
            }), 503
            
        try:
            insights = ai_generator.generate_insights(structured_results, max_retries=3)
        except Exception as e:
            return jsonify({
                'error': f'Failed to generate AI insights: {str(e)}',
                'success': False,
                'retry_suggested': True
            }), 500
        
        # Save insights to file for debugging
        try:
            with open('latest_insights.json', 'w', encoding='utf-8') as f:
                json.dump(insights, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save insights to file: {e}")
        
        return jsonify({
            'success': True,
            'insights': insights
        })
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        return jsonify({
            'error': f'Failed to generate insights: {str(e)}',
            'success': False
        }), 500

def convert_to_structured_format(test_results):
    """Convert raw test results to structured format for AI analysis"""
    
    # Map test screens to structured categories
    structured = {}
    
    # MBTI Test
    if 'mbtiScreen' in test_results:
        structured['mbti_test'] = {
            'selected_option': test_results['mbtiScreen'],
            'test_type': 'Myers-Briggs Type Indicator'
        }
    
    # Multiple Intelligence Test
    if 'intelligenceScreen' in test_results:
        structured['multiple_intelligence'] = {
            'selected_option': test_results['intelligenceScreen'],
            'test_type': 'Multiple Intelligence Assessment'
        }
    
    # Big Five Test
    if 'bigFiveScreen' in test_results:
        structured['big_five'] = {
            'selected_option': test_results['bigFiveScreen'],
            'test_type': 'Big Five Personality Assessment'
        }
    
    # RIASEC Test
    if 'riasecScreen' in test_results:
        structured['riasec'] = {
            'selected_option': test_results['riasecScreen'],
            'test_type': 'RIASEC Career Interest Inventory'
        }
    
    # Decision Making Test
    if 'decisionScreen' in test_results:
        structured['decision_making'] = {
            'selected_option': test_results['decisionScreen'],
            'test_type': 'Decision Making Style Assessment'
        }
    
    # Life Situation Assessment
    if 'lifeScreen' in test_results:
        structured['life_situation'] = {
            'selected_option': test_results['lifeScreen'],
            'test_type': 'Life Situation Assessment'
        }
    
    # VARK Learning Style
    if 'varkScreen' in test_results:
        structured['learning_style'] = {
            'selected_option': test_results['varkScreen'],
            'test_type': 'VARK Learning Style Assessment'
        }
    
    return structured

def get_fallback_insights(test_results):
    """Provide fallback insights when AI is not available"""
    return {
        "best_field": {
            "field": "Technology & Innovation",
            "reasoning": "Based on your assessment responses, you show strong analytical and problem-solving capabilities that align well with technology fields."
        },
        "roadmap": {
            "short_term": [
                "Complete foundational courses in your area of interest",
                "Build a portfolio of small projects",
                "Join relevant online communities and forums"
            ],
            "mid_term": [
                "Pursue specialized certifications",
                "Gain practical experience through internships or projects",
                "Develop leadership and communication skills"
            ],
            "long_term": [
                "Take on senior roles with increased responsibility",
                "Mentor others and share knowledge",
                "Stay updated with industry trends and innovations"
            ]
        },
        "result_analysis": {
            "strengths": [
                "Strong analytical thinking",
                "Good problem-solving abilities",
                "Adaptable to new situations"
            ],
            "weaknesses": [
                "May need to develop interpersonal skills",
                "Could benefit from more practical experience"
            ],
            "reasoning": "Your responses indicate a preference for logical, structured approaches to problems, which is valuable in many professional contexts."
        },
        "career_recommendations": [
            {
                "role": "Software Developer",
                "explanation": "Your analytical skills and problem-solving approach make you well-suited for programming and software development."
            },
            {
                "role": "Data Analyst",
                "explanation": "Your attention to detail and logical thinking align well with data analysis and interpretation roles."
            },
            {
                "role": "Project Manager",
                "explanation": "Your organizational skills and systematic approach could be valuable in project management positions."
            }
        ],
        "skill_recommendations": {
            "technical_skills": [
                "Programming languages (Python, JavaScript, Java)",
                "Data analysis tools (Excel, SQL, Tableau)",
                "Project management software",
                "Cloud computing basics"
            ],
            "soft_skills": [
                "Communication and presentation",
                "Team collaboration",
                "Time management",
                "Critical thinking"
            ]
        },
        "skill_gaps": [
            "Industry-specific technical knowledge",
            "Professional networking abilities",
            "Advanced communication skills",
            "Leadership experience"
        ],
        "future_plans": {
            "3_year_plan": "Establish yourself as a competent professional in your chosen field with solid technical skills and growing industry knowledge.",
            "5_year_plan": "Take on leadership responsibilities, mentor junior colleagues, and become recognized as a subject matter expert.",
            "10_year_plan": "Achieve senior leadership position, drive strategic initiatives, and contribute to industry innovation and best practices."
        },
        "daily_habits": [
            "Spend 30-60 minutes daily learning new skills or technologies",
            "Read industry news and trends for 15 minutes",
            "Practice problem-solving with coding challenges or case studies",
            "Network with one new professional contact weekly",
            "Reflect on daily accomplishments and areas for improvement"
        ],
        "certifications": [
            {
                "name": "Google Career Certificates",
                "provider": "Google",
                "direct_enrollment_link": "https://grow.google/certificates/",
                "why_recommended": "Industry-recognized credentials that provide practical skills for in-demand careers."
            },
            {
                "name": "AWS Cloud Practitioner",
                "provider": "Amazon Web Services",
                "direct_enrollment_link": "https://aws.amazon.com/certification/certified-cloud-practitioner/",
                "why_recommended": "Essential cloud computing knowledge that's valuable across many tech roles."
            },
            {
                "name": "Microsoft Azure Fundamentals",
                "provider": "Microsoft",
                "direct_enrollment_link": "https://docs.microsoft.com/en-us/learn/certifications/azure-fundamentals/",
                "why_recommended": "Foundational cloud knowledge from a major cloud provider."
            },
            {
                "name": "Coursera Professional Certificates",
                "provider": "Coursera",
                "direct_enrollment_link": "https://www.coursera.org/professional-certificates",
                "why_recommended": "Comprehensive programs designed with industry partners for job-ready skills."
            }
        ]
    }

@app.route('/api/download-report', methods=['POST'])
def download_report():
    """
    Generate and download PDF report
    
    Expected JSON payload:
    {
        "testResults": {...},
        "aiInsights": {...} (optional)
    }
    """
    try:
        # Get data from request
        data = request.get_json()
        
        if not data or 'testResults' not in data:
            return jsonify({
                'error': 'Invalid request. testResults required.',
                'success': False
            }), 400
        
        test_results = data['testResults']
        ai_insights = data.get('aiInsights', None)
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"psychological_report_{timestamp}.pdf"
        
        # Generate PDF report
        pdf_path = generate_pdf_report(
            test_results=test_results,
            ai_insights=ai_insights,
            filename=filename
        )
        
        # Create response with PDF file
        response = make_response(send_file(
            pdf_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        ))
        
        # Clean up the temporary file after sending
        return response
        
    except Exception as e:
        print(f"Error in download_report: {e}")
        return jsonify({
            'error': f'Failed to generate PDF report: {str(e)}',
            'success': False
        }), 500

@app.route('/api/generate-markdown', methods=['POST'])
def generate_markdown():
    """Generate markdown content for the report"""
    try:
        data = request.get_json()
        test_results = data.get('testResults', {})
        ai_insights = data.get('aiInsights')
        
        # Generate markdown content
        from markdown_pdf_generator import MarkdownPDFGenerator
        generator = MarkdownPDFGenerator()
        markdown_content = generator.generate_markdown(test_results, ai_insights)
        
        return jsonify({
            'success': True,
            'markdown': markdown_content
        })
        
    except Exception as e:
        print(f"Error generating markdown: {e}")
        return jsonify({
            'error': f'Failed to generate markdown: {str(e)}',
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai_generator_available': ai_generator is not None
    })

if __name__ == '__main__':
    print("Starting AI Insights Web Server...")
    print("Make sure to set GEMINI_API_KEY in your .env file")
    
    # Get port from environment variable (for deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"Server will be available at: http://localhost:{port}")
    
    # Run the Flask app
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
