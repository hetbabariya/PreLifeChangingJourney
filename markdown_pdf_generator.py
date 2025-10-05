"""
Gujarati PDF Report Generator
Generates professional PDF reports with Gujarati language support using ReportLab
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import re

class MarkdownPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Setup custom styles for the PDF report"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#667eea'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            spaceBefore=15,
            textColor=HexColor('#667eea'),
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#4c51bf'),
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            textColor=HexColor('#2d3748'),
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=16
        ))
        
        # Highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=HexColor('#667eea'),
            fontName='Helvetica-Bold'
        ))
        
        # Field name style
        self.styles.add(ParagraphStyle(
            name='FieldName',
            parent=self.styles['Normal'],
            fontSize=16,
            spaceAfter=15,
            textColor=HexColor('#2d3748'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
        
        # Match percentage style
        self.styles.add(ParagraphStyle(
            name='MatchPercentage',
            parent=self.styles['Normal'],
            fontSize=18,
            spaceAfter=15,
            textColor=HexColor('#f6ad55'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))

    def clean_text(self, text):
        """Clean text for markdown compatibility - preserve Gujarati"""
        if not text:
            return ""
        
        text = str(text)
        
        # Keep Gujarati text as is - don't translate to English
        # Just clean up any problematic characters for markdown
        
        # Remove or replace problematic characters that might break markdown
        text = text.replace('\n', ' ')  # Replace newlines with spaces
        text = text.replace('\r', ' ')  # Replace carriage returns
        text = text.replace('\t', ' ')  # Replace tabs with spaces
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def generate_markdown(self, test_results, ai_insights=None):
        """Generate markdown content"""
        markdown_content = []
        
        # Header in Gujarati
        markdown_content.append("# વ્યાપક મનોવૈજ્ઞાનિક મૂલ્યાંકન રિપોર્ટ")
        markdown_content.append("")
        markdown_content.append(f"**રિપોર્ટ બનાવવાની તારીખ:** {datetime.now().strftime('%B %d, %Y')}")
        markdown_content.append("**મૂલ્યાંકનનો પ્રકાર:** AI-આધારિત મનોવૈજ્ઞાનિક પ્રોફાઇલ")
        markdown_content.append("")
        markdown_content.append("---")
        markdown_content.append("")
        
        # AI Insights Section in Gujarati
        if ai_insights:
            markdown_content.append("## 🤖 AI-આધારિત કારકિર્દી માર્ગદર્શન")
            markdown_content.append("")
            markdown_content.append("*તમારા મનોવૈજ્ઞાનિક મૂલ્યાંકન પર આધારિત વ્યક્તિગત ભલામણો*")
            markdown_content.append("")
            
            # Best Career Field in Gujarati
            if 'best_field' in ai_insights:
                best_field = ai_insights['best_field']
                
                markdown_content.append("### 🎯 શ્રેષ્ઠ કારકિર્દી ક્ષેત્ર")
                markdown_content.append("")
                
                field_name = self.clean_text(best_field.get('field', 'N/A'))
                markdown_content.append(f"**{field_name}**")
                markdown_content.append("")
                
                if 'match_percentage' in best_field:
                    markdown_content.append(f"**મેચ પર્સેન્ટેજ: {best_field['match_percentage']}%**")
                    markdown_content.append("")
                
                reasoning = self.clean_text(best_field.get('reasoning', ''))
                if reasoning:
                    markdown_content.append("**કારણ:**")
                    markdown_content.append(reasoning)
                    markdown_content.append("")
                
                # Additional details in Gujarati
                if 'gujarat_opportunities' in best_field:
                    opportunities = self.clean_text(best_field['gujarat_opportunities'])
                    markdown_content.append("**ગુજરાતમાં તકો:**")
                    markdown_content.append(opportunities)
                    markdown_content.append("")
                
                if 'salary_expectations' in best_field:
                    salary = self.clean_text(best_field['salary_expectations'])
                    markdown_content.append("**પગારની અપેક્ષાઓ:**")
                    markdown_content.append(salary)
                    markdown_content.append("")
                
                if 'specific_companies' in best_field:
                    companies = ', '.join([self.clean_text(comp) for comp in best_field['specific_companies']])
                    markdown_content.append("**ભલામણ કરેલી કંપનીઓ:**")
                    markdown_content.append(companies)
                    markdown_content.append("")
                
                if 'growth_potential' in best_field:
                    growth = self.clean_text(best_field['growth_potential'])
                    markdown_content.append("**વૃદ્ધિની સંભાવના:**")
                    markdown_content.append(growth)
                    markdown_content.append("")
                
                if 'entry_requirements' in best_field:
                    entry_req = self.clean_text(best_field['entry_requirements'])
                    markdown_content.append("**પ્રવેશ આવશ્યકતાઓ:**")
                    markdown_content.append(entry_req)
                    markdown_content.append("")
            
            # Career Recommendations in Gujarati
            if 'career_recommendations' in ai_insights:
                markdown_content.append("### 💼 કારકિર્દી ભલામણો")
                markdown_content.append("")
                
                for i, career in enumerate(ai_insights['career_recommendations']):
                    job_role = self.clean_text(career.get('job_role', 'N/A'))
                    industry = self.clean_text(career.get('industry', 'N/A'))
                    explanation = self.clean_text(career.get('explanation', ''))
                    
                    markdown_content.append(f"#### {i+1}. {job_role}")
                    markdown_content.append(f"*ઉદ્યોગ: {industry}*")
                    markdown_content.append("")
                    if explanation:
                        markdown_content.append("**વિગત:**")
                        markdown_content.append(explanation)
                        markdown_content.append("")
                    
                    if 'salary_range' in career:
                        salary = self.clean_text(career['salary_range'])
                        markdown_content.append(f"**પગાર શ્રેણી:** {salary}")
                        markdown_content.append("")
                    
                    if 'required_skills' in career:
                        skills = ', '.join([self.clean_text(skill) for skill in career['required_skills']])
                        markdown_content.append(f"**જરૂરી કુશળતા:** {skills}")
                        markdown_content.append("")
                    
                    if 'growth_potential' in career:
                        growth = self.clean_text(career['growth_potential'])
                        markdown_content.append(f"**વૃદ્ધિની સંભાવના:** {growth}")
                        markdown_content.append("")
                    
                    if 'gujarat_companies' in career:
                        companies = ', '.join([self.clean_text(comp) for comp in career['gujarat_companies']])
                        markdown_content.append(f"**ગુજરાતની કંપનીઓ:** {companies}")
                        markdown_content.append("")
            
            # Skills & Learning Roadmap in Gujarati
            if 'skill_recommendations' in ai_insights:
                markdown_content.append("### 🛠️ કુશળતા અને શીખવાનો રોડમેપ")
                markdown_content.append("")
                
                skills = ai_insights['skill_recommendations']
                
                # Technical Skills
                if 'technical_skills' in skills:
                    markdown_content.append("#### તકનીકી કુશળતાઓ પર ધ્યાન આપો:")
                    markdown_content.append("")
                    for skill_obj in skills['technical_skills']:
                        if isinstance(skill_obj, dict):
                            skill_name = self.clean_text(skill_obj.get('skill', ''))
                            importance = self.clean_text(skill_obj.get('importance', ''))
                            if skill_name:
                                markdown_content.append(f"- **{skill_name}** ({importance})")
                        else:
                            skill_name = self.clean_text(str(skill_obj))
                            if skill_name:
                                markdown_content.append(f"- {skill_name}")
                    markdown_content.append("")
                
                # Soft Skills
                if 'soft_skills' in skills:
                    markdown_content.append("#### સોફ્ટ સ્કિલ્સ વિકસાવો:")
                    markdown_content.append("")
                    for skill_obj in skills['soft_skills']:
                        if isinstance(skill_obj, dict):
                            skill_name = self.clean_text(skill_obj.get('skill', ''))
                            importance = self.clean_text(skill_obj.get('importance', ''))
                            if skill_name:
                                markdown_content.append(f"- **{skill_name}** ({importance})")
                        else:
                            skill_name = self.clean_text(str(skill_obj))
                            if skill_name:
                                markdown_content.append(f"- {skill_name}")
                    markdown_content.append("")
            
            # Learning Roadmap in Gujarati
            if 'roadmap' in ai_insights:
                markdown_content.append("### 🗺️ શીખવાનો રોડમેપ")
                markdown_content.append("")
                
                roadmap = ai_insights['roadmap']
                
                # Short Term
                if 'short_term' in roadmap:
                    short_term = roadmap['short_term']
                    duration = self.clean_text(short_term.get('duration', '1-3 months'))
                    
                    markdown_content.append(f"#### ટૂંકા ગાળાની યોજના ({duration})")
                    markdown_content.append("")
                    
                    if 'goals' in short_term and short_term['goals']:
                        markdown_content.append("**લક્ષ્યો:**")
                        for goal in short_term['goals']:
                            clean_goal = self.clean_text(goal)
                            if clean_goal:  # Only add non-empty goals
                                markdown_content.append(f"- {clean_goal}")
                        markdown_content.append("")
                    
                    if 'specific_actions' in short_term and short_term['specific_actions']:
                        markdown_content.append("**કાર્યો:**")
                        for action in short_term['specific_actions']:
                            clean_action = self.clean_text(action)
                            if clean_action:  # Only add non-empty actions
                                markdown_content.append(f"- {clean_action}")
                        markdown_content.append("")
                
                # Mid Term
                if 'mid_term' in roadmap:
                    mid_term = roadmap['mid_term']
                    duration = self.clean_text(mid_term.get('duration', '6-12 months'))
                    
                    markdown_content.append(f"#### મધ્યમ ગાળાની યોજના ({duration})")
                    markdown_content.append("")
                    
                    if 'goals' in mid_term and mid_term['goals']:
                        markdown_content.append("**લક્ષ્યો:**")
                        for goal in mid_term['goals']:
                            clean_goal = self.clean_text(goal)
                            if clean_goal:  # Only add non-empty goals
                                markdown_content.append(f"- {clean_goal}")
                        markdown_content.append("")
                    
                    if 'milestones' in mid_term and mid_term['milestones']:
                        markdown_content.append("**માઇલસ્ટોન્સ:**")
                        for milestone in mid_term['milestones']:
                            clean_milestone = self.clean_text(milestone)
                            if clean_milestone:  # Only add non-empty milestones
                                markdown_content.append(f"- {clean_milestone}")
                        markdown_content.append("")
                
                # Long Term
                if 'long_term' in roadmap:
                    long_term = roadmap['long_term']
                    duration = self.clean_text(long_term.get('duration', '1-2 years'))
                    
                    markdown_content.append(f"#### લાંબા ગાળાની યોજના ({duration})")
                    markdown_content.append("")
                    
                    if 'goals' in long_term and long_term['goals']:
                        markdown_content.append("**લક્ષ્યો:**")
                        for goal in long_term['goals']:
                            clean_goal = self.clean_text(goal)
                            if clean_goal:  # Only add non-empty goals
                                markdown_content.append(f"- {clean_goal}")
                        markdown_content.append("")
                    
                    if 'entrepreneurship_opportunities' in long_term:
                        entrepreneurship = self.clean_text(long_term['entrepreneurship_opportunities'])
                        markdown_content.append(f"**ઉદ્યોગસાહસિકતાની તકો:** {entrepreneurship}")
                        markdown_content.append("")
            
            # Strengths & Weaknesses in Gujarati
            if 'result_analysis' in ai_insights:
                markdown_content.append("### 📊 શક્તિઓ અને સુધારાના ક્ષેત્રો")
                markdown_content.append("")
                
                analysis = ai_insights['result_analysis']
                
                if 'strengths' in analysis and analysis['strengths']:
                    markdown_content.append("#### તમારી શક્તિઓ:")
                    markdown_content.append("")
                    for strength_obj in analysis['strengths']:
                        if isinstance(strength_obj, dict):
                            strength_name = self.clean_text(strength_obj.get('strength', ''))
                            reasoning = self.clean_text(strength_obj.get('reasoning', ''))
                            career_app = self.clean_text(strength_obj.get('career_application', ''))
                            
                            if strength_name:  # Only add if we have a strength name
                                markdown_content.append(f"**{strength_name}**")
                                markdown_content.append("")
                                if reasoning:
                                    markdown_content.append(f"**કારણ:** {reasoning}")
                                    markdown_content.append("")
                                if career_app:
                                    markdown_content.append(f"*કારકિર્દીમાં ઉપયોગ: {career_app}*")
                                    markdown_content.append("")
                        else:
                            strength_name = self.clean_text(str(strength_obj))
                            if strength_name:  # Only add non-empty strengths
                                markdown_content.append(f"- {strength_name}")
                                markdown_content.append("")
                
                if 'weaknesses' in analysis and analysis['weaknesses']:
                    markdown_content.append("#### સુધારાના ક્ષેત્રો:")
                    markdown_content.append("")
                    for weakness_obj in analysis['weaknesses']:
                        if isinstance(weakness_obj, dict):
                            weakness_name = self.clean_text(weakness_obj.get('weakness', ''))
                            reasoning = self.clean_text(weakness_obj.get('reasoning', ''))
                            improvement = self.clean_text(weakness_obj.get('improvement_strategy', ''))
                            
                            if weakness_name:  # Only add if we have a weakness name
                                markdown_content.append(f"**{weakness_name}**")
                                markdown_content.append("")
                                if reasoning:
                                    markdown_content.append(f"**કારણ:** {reasoning}")
                                    markdown_content.append("")
                                if improvement:
                                    markdown_content.append(f"*સુધારાની વ્યૂહરચના: {improvement}*")
                                    markdown_content.append("")
                        else:
                            weakness_name = self.clean_text(str(weakness_obj))
                            if weakness_name:  # Only add non-empty weaknesses
                                markdown_content.append(f"- {weakness_name}")
                                markdown_content.append("")
            
            # Future Plans
            if 'future_plans' in ai_insights:
                markdown_content.append("### 🚀 Future Growth Plans")
                markdown_content.append("")
                
                plans = ai_insights['future_plans']
                
                if '3_year_plan' in plans:
                    plan_3 = plans['3_year_plan']
                    markdown_content.append("#### 3-Year Plan:")
                    if isinstance(plan_3, dict):
                        position = self.clean_text(plan_3.get('career_position', ''))
                        markdown_content.append(f"**Expected Position:** {position}")
                        if 'key_achievements' in plan_3:
                            achievements = ', '.join([self.clean_text(a) for a in plan_3['key_achievements']])
                            markdown_content.append(f"**Key Achievements:** {achievements}")
                    else:
                        plan_text = self.clean_text(str(plan_3))
                        markdown_content.append(plan_text)
                    markdown_content.append("")
                
                if '5_year_plan' in plans:
                    plan_5 = plans['5_year_plan']
                    markdown_content.append("#### 5-Year Plan:")
                    if isinstance(plan_5, dict):
                        position = self.clean_text(plan_5.get('career_position', ''))
                        markdown_content.append(f"**Senior Position:** {position}")
                        if 'expertise_areas' in plan_5:
                            expertise = ', '.join([self.clean_text(e) for e in plan_5['expertise_areas']])
                            markdown_content.append(f"**Expertise Areas:** {expertise}")
                    else:
                        plan_text = self.clean_text(str(plan_5))
                        markdown_content.append(plan_text)
                    markdown_content.append("")
                
                if '10_year_plan' in plans:
                    plan_10 = plans['10_year_plan']
                    markdown_content.append("#### 10-Year Vision:")
                    if isinstance(plan_10, dict):
                        vision = self.clean_text(plan_10.get('career_vision', ''))
                        markdown_content.append(f"**Career Vision:** {vision}")
                        if 'entrepreneurial_potential' in plan_10:
                            entrepreneurial = self.clean_text(plan_10['entrepreneurial_potential'])
                            markdown_content.append(f"**Entrepreneurial Potential:** {entrepreneurial}")
                    else:
                        plan_text = self.clean_text(str(plan_10))
                        markdown_content.append(plan_text)
                    markdown_content.append("")
            
            # Daily Habits
            if 'daily_habits' in ai_insights:
                markdown_content.append("### 📅 દૈનિક સફળતાની આદતો")
                markdown_content.append("")
                
                for habit_obj in ai_insights['daily_habits']:
                    if isinstance(habit_obj, dict):
                        habit_name = self.clean_text(habit_obj.get('habit', ''))
                        purpose = self.clean_text(habit_obj.get('purpose', ''))
                        implementation = self.clean_text(habit_obj.get('implementation', ''))
                        
                        if habit_name:  # Only add if we have a habit name
                            markdown_content.append(f"**{habit_name}**")
                            markdown_content.append("")
                            if purpose:
                                markdown_content.append(f"*હેતુ:* {purpose}")
                                markdown_content.append("")
                            if implementation:
                                markdown_content.append(f"*અમલીકરણ:* {implementation}")
                                markdown_content.append("")
                    else:
                        habit_name = self.clean_text(str(habit_obj))
                        if habit_name:  # Only add non-empty habits
                            markdown_content.append(f"- {habit_name}")
                            markdown_content.append("")
            
            # Certifications in Gujarati
            if 'certifications' in ai_insights:
                markdown_content.append("### 🏆 ભલામણ કરેલ પ્રમાણપત્રો")
                markdown_content.append("")
                
                for cert in ai_insights['certifications']:
                    cert_name = self.clean_text(cert.get('name', ''))
                    provider = self.clean_text(cert.get('provider', ''))
                    why_recommended = self.clean_text(cert.get('why_recommended', ''))
                    
                    if cert_name:  # Only add if we have a cert name
                        markdown_content.append(f"#### {cert_name}")
                        if provider:
                            markdown_content.append(f"*પ્રદાતા: {provider}*")
                        markdown_content.append("")
                        if why_recommended:
                            markdown_content.append(f"**કેમ ભલામણ કરેલ:** {why_recommended}")
                            markdown_content.append("")
                        
                        if 'difficulty_level' in cert:
                            level = self.clean_text(cert['difficulty_level'])
                            if level:
                                markdown_content.append(f"**સ્તર:** {level}")
                        
                        if 'estimated_duration' in cert:
                            duration = self.clean_text(cert['estimated_duration'])
                            if duration:
                                markdown_content.append(f"**અવધિ:** {duration}")
                        
                        if 'direct_enrollment_link' in cert:
                            markdown_content.append(f"**નોંધણી:** {cert['direct_enrollment_link']}")
                        
                        markdown_content.append("")
        
        # Test Results Section in Gujarati
        markdown_content.append("## 📋 વિગતવાર મૂલ્યાંકન પરિણામો")
        markdown_content.append("")
        
        test_names = {
            'mbtiScreen': 'MBTI વ્યક્તિત્વ પ્રકાર',
            'riasecScreen': 'RIASEC કારકિર્દી રુચિ',
            'varkScreen': 'VARK શીખવાની શૈલી',
            'intelligenceScreen': 'બહુવિધ બુદ્ધિ',
            'decisionScreen': 'નિર્ણય લેવાની શૈલી',
            'lifeScreen': 'જીવનની પ્રાથમિકતાઓ',
            'bigFiveScreen': 'બિગ ફાઇવ વ્યક્તિત્વ'
        }
        
        for test_id, result in test_results.items():
            test_name = test_names.get(test_id, test_id)
            clean_result = self.clean_text(str(result))
            if clean_result and clean_result != 'None':  # Only add non-empty results
                markdown_content.append(f"### {test_name}")
                markdown_content.append(f"**પરિણામ:** {clean_result}")
                markdown_content.append("")
        
        # Footer in Gujarati
        markdown_content.append("---")
        markdown_content.append("")
        markdown_content.append("## મહત્વપૂર્ણ નોંધો")
        markdown_content.append("")
        markdown_content.append("- આ મૂલ્યાંકન સ્વ-રિપોર્ટ કરેલી પસંદગીઓ પર આધારિત છે અને અન્ય પરિબળો સાથે ધ્યાનમાં લેવું જોઈએ")
        markdown_content.append("- પરિણામો સમય સાથે બદલાઈ શકે છે કારણ કે તમે વધો છો અને નવા અનુભવો વિકસાવો છો")
        markdown_content.append("- આ અંતર્દૃષ્ટિનો ઉપયોગ સ્વ-ચિંતન અને વિકાસ માટે પ્રારંભિક બિંદુ તરીકે કરો")
        markdown_content.append("- મુખ્ય જીવન અથવા કારકિર્દીના નિર્ણયો માટે વ્યાવસાયિક માર્ગદર્શન લેવાનું વિચારો")
        markdown_content.append("- આ સાધન માત્ર શૈક્ષણિક અને સ્વ-જાગૃતિના હેતુઓ માટે છે")
        markdown_content.append("")
        markdown_content.append(f"*રિપોર્ટ બનાવવાની તારીખ: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")
        markdown_content.append("")
        markdown_content.append("**AI-આધારિત મનોવૈજ્ઞાનિક પરીક્ષણ પ્લેટફોર્મ**")
        
        return "\n".join(markdown_content)

    def generate_pdf(self, test_results, ai_insights=None, filename=None):
        """Generate PDF using ReportLab directly"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"psychological_report_{timestamp}.pdf"
        
        # Create the PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4, 
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Build the story
        story = []
        
        # Add header
        story.extend(self._create_header())
        
        # Add AI insights if available
        if ai_insights:
            story.extend(self._create_ai_insights_section(ai_insights))
            story.append(PageBreak())
        
        # Add test results
        story.extend(self._create_test_results_section(test_results))
        
        # Add footer
        story.extend(self._create_footer())
        
        # Build the PDF
        doc.build(story)
        
        return filename

    def _create_header(self):
        """Create the report header"""
        story = []
        
        # Title
        story.append(Paragraph("Comprehensive Psychological Assessment Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Report info
        report_date = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", self.styles['CustomBody']))
        story.append(Paragraph("<b>Assessment Type:</b> AI-Powered Psychological Profile", self.styles['CustomBody']))
        story.append(Spacer(1, 30))
        
        return story

    def _create_ai_insights_section(self, ai_insights):
        """Create AI insights section using ReportLab"""
        story = []
        
        # AI Insights Header
        story.append(Paragraph("AI-Powered Career Insights", self.styles['CustomSubtitle']))
        story.append(Paragraph("Personalized recommendations based on your psychological assessment", self.styles['CustomBody']))
        story.append(Spacer(1, 25))
        
        # Best Career Field
        if 'best_field' in ai_insights:
            best_field = ai_insights['best_field']
            
            story.append(Paragraph("Best Career Field", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            
            # Field name
            field_name = self.clean_text(best_field.get('field', 'N/A'))
            story.append(Paragraph(f"<b>{field_name}</b>", self.styles['FieldName']))
            
            # Match percentage
            if 'match_percentage' in best_field:
                story.append(Paragraph(f"Match Percentage: {best_field['match_percentage']}%", self.styles['MatchPercentage']))
            
            # Reasoning
            reasoning = self.clean_text(best_field.get('reasoning', ''))
            if reasoning:
                story.append(Paragraph(reasoning, self.styles['CustomBody']))
            story.append(Spacer(1, 15))
            
            # Additional details
            if 'gujarat_opportunities' in best_field:
                story.append(Paragraph("<b>Opportunities in Gujarat:</b>", self.styles['Highlight']))
                opportunities = self.clean_text(best_field['gujarat_opportunities'])
                story.append(Paragraph(opportunities, self.styles['CustomBody']))
                story.append(Spacer(1, 8))
            
            if 'salary_expectations' in best_field:
                story.append(Paragraph("<b>Salary Expectations:</b>", self.styles['Highlight']))
                salary = self.clean_text(best_field['salary_expectations'])
                story.append(Paragraph(salary, self.styles['CustomBody']))
                story.append(Spacer(1, 8))
            
            if 'specific_companies' in best_field:
                story.append(Paragraph("<b>Recommended Companies:</b>", self.styles['Highlight']))
                companies = ', '.join(best_field['specific_companies'])
                story.append(Paragraph(companies, self.styles['CustomBody']))
                story.append(Spacer(1, 8))
            
            story.append(Spacer(1, 20))
        
        # Career Recommendations
        if 'career_recommendations' in ai_insights:
            story.append(Paragraph("Career Recommendations", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            
            for i, career in enumerate(ai_insights['career_recommendations']):
                job_role = self.clean_text(career.get('job_role', 'N/A'))
                industry = self.clean_text(career.get('industry', 'N/A'))
                explanation = self.clean_text(career.get('explanation', ''))
                
                story.append(Paragraph(f"<b>{i+1}. {job_role}</b>", self.styles['Highlight']))
                story.append(Paragraph(f"<i>Industry: {industry}</i>", self.styles['CustomBody']))
                
                if explanation:
                    story.append(Paragraph(explanation, self.styles['CustomBody']))
                
                if 'salary_range' in career:
                    salary = self.clean_text(career['salary_range'])
                    story.append(Paragraph(f"<b>Salary Range:</b> {salary}", self.styles['CustomBody']))
                
                if 'required_skills' in career:
                    skills = ', '.join(career['required_skills'])
                    story.append(Paragraph(f"<b>Required Skills:</b> {skills}", self.styles['CustomBody']))
                
                story.append(Spacer(1, 15))
        
        # Skills & Learning Roadmap
        if 'skill_recommendations' in ai_insights:
            story.append(Paragraph("Skills & Learning Roadmap", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            
            skills = ai_insights['skill_recommendations']
            
            # Technical Skills
            if 'technical_skills' in skills:
                story.append(Paragraph("<b>Technical Skills to Focus On:</b>", self.styles['Highlight']))
                for skill_obj in skills['technical_skills']:
                    if isinstance(skill_obj, dict):
                        skill_name = self.clean_text(skill_obj.get('skill', ''))
                        importance = skill_obj.get('importance', '')
                        story.append(Paragraph(f"• {skill_name} ({importance})", self.styles['CustomBody']))
                    else:
                        skill_name = self.clean_text(str(skill_obj))
                        story.append(Paragraph(f"• {skill_name}", self.styles['CustomBody']))
                story.append(Spacer(1, 10))
            
            # Soft Skills
            if 'soft_skills' in skills:
                story.append(Paragraph("<b>Soft Skills to Develop:</b>", self.styles['Highlight']))
                for skill_obj in skills['soft_skills']:
                    if isinstance(skill_obj, dict):
                        skill_name = self.clean_text(skill_obj.get('skill', ''))
                        importance = skill_obj.get('importance', '')
                        story.append(Paragraph(f"• {skill_name} ({importance})", self.styles['CustomBody']))
                    else:
                        skill_name = self.clean_text(str(skill_obj))
                        story.append(Paragraph(f"• {skill_name}", self.styles['CustomBody']))
                story.append(Spacer(1, 15))
        
        # Learning Roadmap
        if 'roadmap' in ai_insights:
            story.append(Paragraph("Learning Roadmap", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            
            roadmap = ai_insights['roadmap']
            
            # Short Term
            if 'short_term' in roadmap:
                short_term = roadmap['short_term']
                duration = self.clean_text(short_term.get('duration', '1-3 months'))
                
                story.append(Paragraph(f"<b>Short Term ({duration}):</b>", self.styles['Highlight']))
                
                if 'goals' in short_term:
                    story.append(Paragraph("Goals:", self.styles['CustomBody']))
                    for goal in short_term['goals']:
                        clean_goal = self.clean_text(goal)
                        story.append(Paragraph(f"• {clean_goal}", self.styles['CustomBody']))
                
                if 'specific_actions' in short_term:
                    story.append(Paragraph("Actions:", self.styles['CustomBody']))
                    for action in short_term['specific_actions']:
                        clean_action = self.clean_text(action)
                        story.append(Paragraph(f"• {clean_action}", self.styles['CustomBody']))
                
                story.append(Spacer(1, 10))
            
            # Mid Term
            if 'mid_term' in roadmap:
                mid_term = roadmap['mid_term']
                duration = self.clean_text(mid_term.get('duration', '6-12 months'))
                
                story.append(Paragraph(f"<b>Mid Term ({duration}):</b>", self.styles['Highlight']))
                
                if 'goals' in mid_term:
                    story.append(Paragraph("Goals:", self.styles['CustomBody']))
                    for goal in mid_term['goals']:
                        clean_goal = self.clean_text(goal)
                        story.append(Paragraph(f"• {clean_goal}", self.styles['CustomBody']))
                
                if 'milestones' in mid_term:
                    story.append(Paragraph("Milestones:", self.styles['CustomBody']))
                    for milestone in mid_term['milestones']:
                        clean_milestone = self.clean_text(milestone)
                        story.append(Paragraph(f"• {clean_milestone}", self.styles['CustomBody']))
                
                story.append(Spacer(1, 10))
            
            # Long Term
            if 'long_term' in roadmap:
                long_term = roadmap['long_term']
                duration = self.clean_text(long_term.get('duration', '1-2 years'))
                
                story.append(Paragraph(f"<b>Long Term ({duration}):</b>", self.styles['Highlight']))
                
                if 'goals' in long_term:
                    story.append(Paragraph("Goals:", self.styles['CustomBody']))
                    for goal in long_term['goals']:
                        clean_goal = self.clean_text(goal)
                        story.append(Paragraph(f"• {clean_goal}", self.styles['CustomBody']))
                
                if 'entrepreneurship_opportunities' in long_term:
                    entrepreneurship = self.clean_text(long_term['entrepreneurship_opportunities'])
                    story.append(Paragraph(f"Entrepreneurship Opportunities: {entrepreneurship}", self.styles['CustomBody']))
                
                story.append(Spacer(1, 15))
        
        # Strengths & Weaknesses
        if 'result_analysis' in ai_insights:
            story.append(Paragraph("Strengths & Areas for Improvement", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            
            analysis = ai_insights['result_analysis']
            
            if 'strengths' in analysis:
                story.append(Paragraph("<b>Your Strengths:</b>", self.styles['Highlight']))
                for strength_obj in analysis['strengths']:
                    if isinstance(strength_obj, dict):
                        strength_name = self.clean_text(strength_obj.get('strength', ''))
                        story.append(Paragraph(f"• <b>{strength_name}</b>", self.styles['CustomBody']))
                        reasoning = self.clean_text(strength_obj.get('reasoning', ''))
                        if reasoning:
                            story.append(Paragraph(f"  {reasoning}", self.styles['CustomBody']))
                        career_app = self.clean_text(strength_obj.get('career_application', ''))
                        if career_app:
                            story.append(Paragraph(f"  <i>Career Application: {career_app}</i>", self.styles['CustomBody']))
                    else:
                        strength_name = self.clean_text(str(strength_obj))
                        story.append(Paragraph(f"• {strength_name}", self.styles['CustomBody']))
                story.append(Spacer(1, 10))
            
            if 'weaknesses' in analysis:
                story.append(Paragraph("<b>Areas for Growth:</b>", self.styles['Highlight']))
                for weakness_obj in analysis['weaknesses']:
                    if isinstance(weakness_obj, dict):
                        weakness_name = self.clean_text(weakness_obj.get('weakness', ''))
                        story.append(Paragraph(f"• <b>{weakness_name}</b>", self.styles['CustomBody']))
                        reasoning = self.clean_text(weakness_obj.get('reasoning', ''))
                        if reasoning:
                            story.append(Paragraph(f"  {reasoning}", self.styles['CustomBody']))
                        improvement = self.clean_text(weakness_obj.get('improvement_strategy', ''))
                        if improvement:
                            story.append(Paragraph(f"  <i>Improvement Strategy: {improvement}</i>", self.styles['CustomBody']))
                    else:
                        weakness_name = self.clean_text(str(weakness_obj))
                        story.append(Paragraph(f"• {weakness_name}", self.styles['CustomBody']))
                story.append(Spacer(1, 15))
        
        # Future Plans
        if 'future_plans' in ai_insights:
            story.append(Paragraph("Future Growth Plans", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            
            plans = ai_insights['future_plans']
            
            if '3_year_plan' in plans:
                plan_3 = plans['3_year_plan']
                story.append(Paragraph("<b>3-Year Plan:</b>", self.styles['Highlight']))
                if isinstance(plan_3, dict):
                    position = self.clean_text(plan_3.get('career_position', ''))
                    story.append(Paragraph(f"Expected Position: {position}", self.styles['CustomBody']))
                    if 'key_achievements' in plan_3:
                        achievements = ', '.join([self.clean_text(a) for a in plan_3['key_achievements']])
                        story.append(Paragraph(f"Key Achievements: {achievements}", self.styles['CustomBody']))
                else:
                    plan_text = self.clean_text(str(plan_3))
                    story.append(Paragraph(plan_text, self.styles['CustomBody']))
                story.append(Spacer(1, 10))
            
            if '5_year_plan' in plans:
                plan_5 = plans['5_year_plan']
                story.append(Paragraph("<b>5-Year Plan:</b>", self.styles['Highlight']))
                if isinstance(plan_5, dict):
                    position = self.clean_text(plan_5.get('career_position', ''))
                    story.append(Paragraph(f"Senior Position: {position}", self.styles['CustomBody']))
                    if 'expertise_areas' in plan_5:
                        expertise = ', '.join([self.clean_text(e) for e in plan_5['expertise_areas']])
                        story.append(Paragraph(f"Expertise Areas: {expertise}", self.styles['CustomBody']))
                else:
                    plan_text = self.clean_text(str(plan_5))
                    story.append(Paragraph(plan_text, self.styles['CustomBody']))
                story.append(Spacer(1, 10))
            
            if '10_year_plan' in plans:
                plan_10 = plans['10_year_plan']
                story.append(Paragraph("<b>10-Year Vision:</b>", self.styles['Highlight']))
                if isinstance(plan_10, dict):
                    vision = self.clean_text(plan_10.get('career_vision', ''))
                    story.append(Paragraph(f"Career Vision: {vision}", self.styles['CustomBody']))
                    if 'entrepreneurial_potential' in plan_10:
                        entrepreneurial = self.clean_text(plan_10['entrepreneurial_potential'])
                        story.append(Paragraph(f"Entrepreneurial Potential: {entrepreneurial}", self.styles['CustomBody']))
                else:
                    plan_text = self.clean_text(str(plan_10))
                    story.append(Paragraph(plan_text, self.styles['CustomBody']))
                story.append(Spacer(1, 15))
        
        # Daily Habits
        if 'daily_habits' in ai_insights:
            story.append(Paragraph("Daily Success Habits", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            
            for habit_obj in ai_insights['daily_habits']:
                if isinstance(habit_obj, dict):
                    habit_name = self.clean_text(habit_obj.get('habit', ''))
                    story.append(Paragraph(f"• <b>{habit_name}</b>", self.styles['Highlight']))
                    purpose = self.clean_text(habit_obj.get('purpose', ''))
                    if purpose:
                        story.append(Paragraph(f"  Purpose: {purpose}", self.styles['CustomBody']))
                    implementation = self.clean_text(habit_obj.get('implementation', ''))
                    if implementation:
                        story.append(Paragraph(f"  Implementation: {implementation}", self.styles['CustomBody']))
                else:
                    habit_name = self.clean_text(str(habit_obj))
                    story.append(Paragraph(f"• {habit_name}", self.styles['CustomBody']))
            story.append(Spacer(1, 15))
        
        # Certifications
        if 'certifications' in ai_insights:
            story.append(Paragraph("Recommended Certifications", self.styles['SectionHeader']))
            story.append(Spacer(1, 10))
            
            for cert in ai_insights['certifications']:
                cert_name = self.clean_text(cert.get('name', ''))
                provider = self.clean_text(cert.get('provider', ''))
                story.append(Paragraph(f"<b>{cert_name}</b> - {provider}", self.styles['Highlight']))
                
                why_recommended = self.clean_text(cert.get('why_recommended', ''))
                if why_recommended:
                    story.append(Paragraph(why_recommended, self.styles['CustomBody']))
                
                if 'difficulty_level' in cert:
                    level = self.clean_text(cert['difficulty_level'])
                    story.append(Paragraph(f"Level: {level}", self.styles['CustomBody']))
                
                if 'estimated_duration' in cert:
                    duration = self.clean_text(cert['estimated_duration'])
                    story.append(Paragraph(f"Duration: {duration}", self.styles['CustomBody']))
                
                if 'direct_enrollment_link' in cert:
                    story.append(Paragraph(f"<i>Enrollment: {cert['direct_enrollment_link']}</i>", self.styles['CustomBody']))
                
                story.append(Spacer(1, 12))
        
        return story

    def _create_test_results_section(self, test_results):
        """Create test results section"""
        story = []
        
        story.append(Paragraph("Detailed Assessment Results", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 20))
        
        test_names = {
            'mbtiScreen': 'MBTI Personality Type',
            'riasecScreen': 'RIASEC Career Interest',
            'varkScreen': 'VARK Learning Style',
            'intelligenceScreen': 'Multiple Intelligence',
            'decisionScreen': 'Decision Making Style',
            'lifeScreen': 'Life Priorities',
            'bigFiveScreen': 'Big Five Personality'
        }
        
        for test_id, result in test_results.items():
            test_name = test_names.get(test_id, test_id)
            clean_result = self.clean_text(str(result))
            story.append(Paragraph(f"<b>{test_name}:</b>", self.styles['Highlight']))
            story.append(Paragraph(clean_result, self.styles['CustomBody']))
            story.append(Spacer(1, 15))
        
        return story

    def _create_footer(self):
        """Create the report footer"""
        story = []
        
        story.append(Spacer(1, 30))
        story.append(Paragraph("Important Notes", self.styles['SectionHeader']))
        story.append(Paragraph("• This assessment is based on self-reported preferences and should be considered alongside other factors", self.styles['CustomBody']))
        story.append(Paragraph("• Results may change over time as you grow and develop new experiences", self.styles['CustomBody']))
        story.append(Paragraph("• Use these insights as a starting point for self-reflection and development", self.styles['CustomBody']))
        story.append(Paragraph("• Consider seeking professional guidance for major life or career decisions", self.styles['CustomBody']))
        story.append(Paragraph("• This tool is for educational and self-awareness purposes only", self.styles['CustomBody']))
        
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", self.styles['CustomBody']))
        story.append(Paragraph("AI-Powered Psychological Testing Platform", self.styles['CustomBody']))
        
        return story

def generate_pdf_report(test_results, ai_insights=None, filename=None):
    """Generate PDF report using markdown approach"""
    generator = MarkdownPDFGenerator()
    return generator.generate_pdf(test_results, ai_insights, filename)
