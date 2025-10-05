"""
AI Insights Generator using Gemini 2.0 Flash
Generates personalized career insights based on psychological test results
"""

import json
import os
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIInsightsGenerator:
    def __init__(self):
        """Initialize the AI Insights Generator with Gemini 2.0 Flash model"""
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Initialize Gemini 2.0 Flash model
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # System prompt for generating insights
        self.system_prompt = """
You are a world-class career counselor, psychologist, and life coach with 20+ years of experience.  
You deeply understand:
- MBTI, Big Five, RIASEC, VARK, and intelligence types  
- Indian and Gujarati job market, business, and education systems  
- Modern AI, IT, business, and entrepreneurship careers  

All responses must be **in Gujarati (ગુજરાતી)** and **in valid JSON** — no extra text.

### YOUR TASK:
Generate a complete **Gujarati AI Career Insight Report** in JSON format with deep, actionable, personalized recommendations.

The report must include **exactly** the following fields:

```json
{
  "best_field": {
    "field": "તમારા વ્યક્તિત્વ માટે શ્રેષ્ઠ કારકિર્દી ક્ષેત્ર",
    "reasoning": "પરિણામોના આધારે વિગતવાર સમજૂતી",
    "match_percentage": 95,
    "gujarat_opportunities": "ગુજરાતમાં આ ક્ષેત્રની તકો",
    "indian_market_outlook": "ભારતમાં આ ક્ષેત્રની સંભાવના",
    "specific_companies": ["કંપની 1", "કંપની 2"],
    "salary_expectations": "અંદાજિત પગાર શ્રેણી",
    "growth_potential": "કારકિર્દી વૃદ્ધિની સંભાવના",
    "entry_requirements": "પ્રવેશ માટે જરૂરી અભ્યાસ/કુશળતા"
  },
  "roadmap": {
    "short_term": {
      "duration": "1–3 મહિના",
      "goals": ["લક્ષ્ય 1", "લક્ષ્ય 2"],
      "skills_to_develop": ["કુશળતા 1", "કુશળતા 2"],
      "resources": ["સંસાધન 1", "સંસાધન 2"],
      "specific_actions": ["કાર્ય 1", "કાર્ય 2"]
    },
    "mid_term": {
      "duration": "6–12 મહિના",
      "goals": ["લક્ષ્ય 1", "લક્ષ્ય 2"],
      "skills_to_develop": ["અદ્યતન કુશળતા 1", "અદ્યતન કુશળતા 2"],
      "milestones": ["પડાવ 1", "પડાવ 2"]
    },
    "long_term": {
      "duration": "1–2 વર્ષ",
      "goals": ["લાંબા ગાળાનું લક્ષ્ય 1", "લાંબા ગાળાનું લક્ષ્ય 2"],
      "expertise_areas": ["નિપુણતા ક્ષેત્ર 1", "નિપુણતા ક્ષેત્ર 2"],
      "entrepreneurship_opportunities": "ગુજરાતમાં ઉદ્યોગસાહસિક તકો"
    }
  },
  "result_analysis": {
    "strengths": [
      {
        "strength": "મુખ્ય શક્તિ",
        "reasoning": "પરિણામ પરથી આ શક્તિ કેવી રીતે દેખાય છે",
        "career_application": "કારકિર્દીમાં તેનો ઉપયોગ કેવી રીતે કરવો"
      }
    ],
    "weaknesses": [
      {
        "weakness": "સુધારાની જરૂરિયાત ધરાવતું ક્ષેત્ર",
        "reasoning": "આ નબળાઈ કેમ મહત્વપૂર્ણ છે",
        "improvement_strategy": "તે સુધારવા માટે ભલામણ કરેલી રીત"
      }
    ]
  },
  "career_recommendations": [
    {
      "job_role": "ચોક્કસ નોકરીનું પદ",
      "industry": "ઉદ્યોગ ક્ષેત્ર",
      "explanation": "આ ભૂમિકા વ્યક્તિત્વ સાથે કેવી રીતે મેળ ખાય છે",
      "growth_potential": "ઉચ્ચ/મધ્યમ/નીચું",
      "salary_range": "₹X થી ₹Y પ્રતિ મહિનો",
      "gujarat_companies": ["કંપની 1", "કંપની 2"],
      "required_skills": ["કુશળતા 1", "કુશળતા 2"]
    }
  ],
  "skill_recommendations": {
    "technical_skills": [
      {
        "skill": "તકનીકી કુશળતા",
        "importance": "ઉચ્ચ/મધ્યમ/નીચું",
        "learning_resources": ["https://example.com/course1"]
      }
    ],
    "soft_skills": [
      {
        "skill": "સોફ્ટ સ્કિલ",
        "importance": "ઉચ્ચ/મધ્યમ/નીચું",
        "development_approach": "તે વિકસાવવા માટે ભલામણ કરેલી રીત"
      }
    ]
  },
  "skill_gaps": [
    {
      "gap": "ખૂટતી કુશળતા",
      "impact": "આ ખાડો કારકિર્દી પર કેવી અસર કરે છે",
      "priority": "ઉચ્ચ/મધ્યમ/નીચું",
      "learning_path": "તે શીખવા માટેનો માર્ગ",
      "free_resources": ["https://freecourse.com"]
    }
  ],
  "future_plans": {
    "3_year_plan": {
      "career_position": "અપેક્ષિત ભૂમિકા",
      "key_achievements": ["પ્રાપ્તિ 1", "પ્રાપ્તિ 2"]
    },
    "5_year_plan": {
      "career_position": "વરિષ્ઠ ભૂમિકા",
      "expertise_areas": ["ક્ષેત્ર 1", "ક્ષેત્ર 2"]
    },
    "10_year_plan": {
      "career_vision": "લાંબા ગાળાની દ્રષ્ટિ",
      "entrepreneurial_potential": "પોતાનો વ્યવસાય શરૂ કરવાની સંભાવના"
    }
  },
  "daily_habits": [
    {
      "habit": "દૈનિક આદત",
      "purpose": "આ આદતનું મહત્વ",
      "implementation": "તે કેવી રીતે અમલમાં મૂકવી"
    }
  ],
  "certifications": [
    {
      "name": "પ્રમાણપત્રનું નામ",
      "provider": "Coursera / Google / AWS",
      "direct_enrollment_link": "https://coursera.org/learn/example",
      "why_recommended": "આ પ્રમાણપત્ર તમારા ક્ષેત્ર માટે ઉપયોગી છે",
      "difficulty_level": "શરૂઆત / મધ્યમ / અદ્યતન",
      "estimated_duration": "2 મહિના"
    }
  ],
  "additional_insights": {
    "work_environment": "યોગ્ય કામનું વાતાવરણ",
    "stress_management": "તણાવ સંચાલન માટેની રીતો",
    "gujarat_specific_advice": "ગુજરાતના સંદર્ભમાં ખાસ સલાહ"
  }
}
```

### Rules:
- Output only valid JSON in the exact format above
- All text must be in Gujarati (ગુજરાતી)
- Be specific about Gujarat and Indian job market
- Include real company names and certification links
- Provide actionable, practical advice
- No text outside JSON
"""

    def format_test_results(self, test_results: Dict[str, Any]) -> str:
        """Format test results into a readable string for the AI model"""
        formatted_results = "PSYCHOLOGICAL TEST RESULTS:\n\n"
        
        for test_name, result in test_results.items():
            formatted_results += f"=== {test_name.upper()} ===\n"
            if isinstance(result, dict):
                for key, value in result.items():
                    formatted_results += f"{key}: {value}\n"
            else:
                formatted_results += f"Result: {result}\n"
            formatted_results += "\n"
        
        return formatted_results

    def generate_insights(self, test_results: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
        """
        Generate AI insights based on test results with retry logic
        
        Args:
            test_results: Dictionary containing test results from various psychological tests
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dictionary containing AI-generated insights in JSON format
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                print(f"Generating AI insights (attempt {attempt + 1}/{max_retries})...")
                
                # Format test results
                formatted_results = self.format_test_results(test_results)
                
                # Create the complete prompt
                full_prompt = f"{self.system_prompt}\n\nHere are the test results:\n\n{formatted_results}"
                
                # Generate insights using Gemini with specific parameters
                response = self.model.generate_content(
                    full_prompt,
                    generation_config={
                        'temperature': 0.7,
                        'top_p': 0.8,
                        'top_k': 40,
                        'max_output_tokens': 4000,
                    }
                )
                
                if not response.text:
                    raise ValueError("Empty response from AI model")
                
                # Clean the response text
                response_text = response.text.strip()
                
                # Remove any markdown code blocks if present
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                response_text = response_text.strip()
                
                # Parse the JSON response
                insights_json = json.loads(response_text)
                
                # Validate that we have the required fields
                required_fields = ['best_field', 'roadmap', 'result_analysis', 'career_recommendations']
                for field in required_fields:
                    if field not in insights_json:
                        raise ValueError(f"Missing required field: {field}")
                
                print("AI insights generated successfully!")
                return insights_json
                
            except json.JSONDecodeError as e:
                last_error = f"JSON parsing error: {e}"
                print(f"Attempt {attempt + 1} failed: {last_error}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    continue
                    
            except Exception as e:
                last_error = f"Generation error: {e}"
                print(f"Attempt {attempt + 1} failed: {last_error}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    continue
        
        # If all attempts failed, raise an exception instead of returning fallback
        raise Exception(f"Failed to generate AI insights after {max_retries} attempts. Last error: {last_error}")

    def _get_fallback_insights(self) -> Dict[str, Any]:
        """Provide fallback insights in case of API failure"""
        return {
            "best_field": {
                "field": "ટેકનોલોજી અને IT",
                "reasoning": "તમારા મૂલ્યાંકન પરિણામોના આધારે, ટેકનોલોજી ક્ષેત્ર વૃદ્ધિ અને શિક્ષણ માટે વિવિધ તકો પ્રદાન કરે છે.",
                "match_percentage": 85,
                "gujarat_opportunities": "ગુજરાતમાં અમદાવાદ, સુરત, અને ગાંધીનગરમાં IT કંપનીઓ વધી રહી છે",
                "indian_market_outlook": "ભારતમાં IT ક્ષેત્ર ઝડપથી વિકસી રહ્યું છે અને રોજગારની તકો વધી રહી છે",
                "specific_companies": ["TCS", "Infosys", "Wipro", "HCL"],
                "salary_expectations": "₹25,000 થી ₹80,000 પ્રતિ મહિનો (અનુભવ પ્રમાણે)",
                "growth_potential": "ઉચ્ચ વૃદ્ધિની સંભાવના",
                "entry_requirements": "કોમ્પ્યુટર સાયન્સ અથવા સંબંધિત ક્ષેત્રમાં ડિગ્રી"
            },
            "roadmap": {
                "short_term": {
                    "duration": "1–3 મહિના",
                    "goals": ["મૂળભૂત પ્રોગ્રામિંગ શીખો", "પોર્ટફોલિયો બનાવો"],
                    "skills_to_develop": ["HTML/CSS", "JavaScript", "Python"],
                    "resources": ["Coursera", "YouTube", "FreeCodeCamp"],
                    "specific_actions": ["દરરોજ 2 કલાક કોડિંગ પ્રેક્ટિસ", "ઓનલાઈન કોર્સ પૂર્ણ કરો"]
                },
                "mid_term": {
                    "duration": "6–12 મહિના",
                    "goals": ["અદ્યતન પ્રોગ્રામિંગ શીખો", "પ્રોજેક્ટ બનાવો"],
                    "skills_to_develop": ["React", "Node.js", "Database Management"],
                    "milestones": ["3 પ્રોજેક્ટ પૂર્ણ કરો", "GitHub પર કોડ અપલોડ કરો"]
                },
                "long_term": {
                    "duration": "1–2 વર્ષ",
                    "goals": ["નોકરી મેળવો", "નિપુણતા વિકસાવો"],
                    "expertise_areas": ["Full Stack Development", "Cloud Computing"],
                    "entrepreneurship_opportunities": "ગુજરાતમાં સ્ટાર્ટઅપ ઇકોસિસ્ટમ વિકસી રહ્યું છે"
                }
            },
            "result_analysis": {
                "strengths": [
                    {
                        "strength": "વિશ્લેષણાત્મક વિચારસરણી",
                        "reasoning": "તમારા પરિણામો દર્શાવે છે કે તમે સમસ્યાઓનું વિશ્લેષણ કરવામાં સારા છો",
                        "career_application": "પ્રોગ્રામિંગ અને ડેટા એનાલિસિસમાં ઉપયોગી"
                    }
                ],
                "weaknesses": [
                    {
                        "weakness": "તકનીકી કુશળતાની જરૂર",
                        "reasoning": "આધુનિક કારકિર્દી માટે તકનીકી જ્ઞાન જરૂરી છે",
                        "improvement_strategy": "ઓનલાઈન કોર્સ અને પ્રેક્ટિકલ પ્રોજેક્ટ દ્વારા શીખો"
                    }
                ]
            },
            "career_recommendations": [
                {
                    "job_role": "સોફ્ટવેર ડેવલપર",
                    "industry": "IT અને ટેકનોલોજી",
                    "explanation": "તમારી વિશ્લેષણાત્મક કુશળતા પ્રોગ્રામિંગ માટે યોગ્ય છે",
                    "growth_potential": "ઉચ્ચ",
                    "salary_range": "₹30,000 થી ₹1,00,000 પ્રતિ મહિનો",
                    "gujarat_companies": ["TCS Gandhinagar", "Infosys Ahmedabad"],
                    "required_skills": ["Java", "Python", "Problem Solving"]
                }
            ],
            "skill_recommendations": {
                "technical_skills": [
                    {
                        "skill": "પ્રોગ્રામિંગ (Python/Java)",
                        "importance": "ઉચ્ચ",
                        "learning_resources": ["https://www.coursera.org/learn/python"]
                    }
                ],
                "soft_skills": [
                    {
                        "skill": "સંવાદ કુશળતા",
                        "importance": "ઉચ્ચ",
                        "development_approach": "ટીમ પ્રોજેક્ટ અને પ્રેઝન્ટેશન દ્વારા"
                    }
                ]
            },
            "skill_gaps": [
                {
                    "gap": "પ્રેક્ટિકલ પ્રોગ્રામિંગ અનુભવ",
                    "impact": "નોકરી મેળવવામાં મુશ્કેલી",
                    "priority": "ઉચ્ચ",
                    "learning_path": "ઓનલાઈન કોર્સ અને પ્રોજેક્ટ બિલ્ડિંગ",
                    "free_resources": ["https://www.freecodecamp.org"]
                }
            ],
            "future_plans": {
                "3_year_plan": {
                    "career_position": "સિનિયર સોફ્ટવેર ડેવલપર",
                    "key_achievements": ["ટીમ લીડ બનવું", "મુખ્ય પ્રોજેક્ટ હેન્ડલ કરવું"]
                },
                "5_year_plan": {
                    "career_position": "ટેકનિકલ આર્કિટેક્ટ",
                    "expertise_areas": ["Cloud Computing", "System Design"]
                },
                "10_year_plan": {
                    "career_vision": "ટેકનોલોજી કંપનીના CTO અથવા પોતાનું સ્ટાર્ટઅપ",
                    "entrepreneurial_potential": "ગુજરાતમાં ટેક સ્ટાર્ટઅપ શરૂ કરવાની સારી સંભાવના"
                }
            },
            "daily_habits": [
                {
                    "habit": "દરરોજ 1 કલાક કોડિંગ પ્રેક્ટિસ",
                    "purpose": "તકનીકી કુશળતા સુધારવા માટે",
                    "implementation": "સવારે અથવા સાંજે નિયમિત સમય નક્કી કરો"
                }
            ],
            "certifications": [
                {
                    "name": "Google IT Support Certificate",
                    "provider": "Google",
                    "direct_enrollment_link": "https://grow.google/certificates/it-support/",
                    "why_recommended": "IT ક્ષેત્રમાં પ્રવેશ માટે ઉત્તમ પ્રમાણપત્ર",
                    "difficulty_level": "શરૂઆત",
                    "estimated_duration": "3-6 મહિના"
                }
            ],
            "additional_insights": {
                "work_environment": "સહયોગી ટીમ વાતાવરણ, લવચીક કામના કલાકો",
                "stress_management": "નિયમિત વિરામ, યોગ, અને સમય વ્યવસ્થાપન",
                "gujarat_specific_advice": "ગુજરાતમાં GIFT City અને અમદાવાદના IT હબમાં તકો શોધો"
            }
        }

    def save_insights_to_file(self, insights: Dict[str, Any], filename: str = "ai_insights_report.json"):
        """Save generated insights to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(insights, f, indent=2, ensure_ascii=False)
            print(f"Insights saved to {filename}")
        except Exception as e:
            print(f"Error saving insights to file: {e}")

def main():
    """Main function to demonstrate usage"""
    # Example test results (replace with actual test data)
    sample_test_results = {
        "mbti_test": {
            "personality_type": "INTJ",
            "dominant_function": "Introverted Intuition",
            "auxiliary_function": "Extraverted Thinking"
        },
        "big_five": {
            "openness": 85,
            "conscientiousness": 78,
            "extraversion": 45,
            "agreeableness": 62,
            "neuroticism": 35
        },
        "multiple_intelligence": {
            "logical_mathematical": 88,
            "linguistic": 72,
            "spatial": 65,
            "musical": 45,
            "bodily_kinesthetic": 55,
            "interpersonal": 58,
            "intrapersonal": 82,
            "naturalistic": 48
        },
        "riasec": {
            "realistic": 45,
            "investigative": 85,
            "artistic": 62,
            "social": 48,
            "enterprising": 55,
            "conventional": 68
        },
        "decision_making": {
            "style": "Analytical",
            "confidence": 78,
            "risk_tolerance": "Moderate"
        },
        "learning_style": {
            "visual": 75,
            "auditory": 55,
            "reading_writing": 82,
            "kinesthetic": 48
        }
    }
    
    try:
        # Initialize the AI insights generator
        ai_generator = AIInsightsGenerator()
        
        # Generate insights
        print("Generating AI insights...")
        insights = ai_generator.generate_insights(sample_test_results)
        
        # Display insights
        print("\n" + "="*50)
        print("AI INSIGHTS GENERATED SUCCESSFULLY")
        print("="*50)
        print(json.dumps(insights, indent=2))
        
        # Save to file
        ai_generator.save_insights_to_file(insights)
        
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
