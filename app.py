import streamlit as st
import random
from dataclasses import dataclass
from typing import List, Dict
import plotly.graph_objects as go

# Configure page for mobile-friendly experience
st.set_page_config(
    page_title="🧪 Chemistry Lab - Love Compatibility",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for lab theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #e0e0e0;
    }
    
    .lab-container {
        background: rgba(0, 20, 40, 0.8);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    .neon-text {
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff;
        font-weight: bold;
    }
    
    .result-card {
        background: rgba(0, 40, 80, 0.6);
        border: 1px solid #00ffff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    @keyframes bubble {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-3px); }
    }
    
    .neon-text {
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
        font-weight: bold;
        text-align: center;
    }
    
    .compatibility-meter {
        background: linear-gradient(90deg, #ff0080 0%, #ffff00 50%, #00ff80 100%);
        height: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .molecule {
        display: inline-block;
        width: 15px;
        height: 15px;
        background: #00ffff;
        border-radius: 50%;
        margin: 2px;
        box-shadow: 0 0 8px #00ffff;
    }
    
    .mobile-button {
        width: 100%;
        padding: 15px;
        font-size: 18px;
        margin: 10px 0;
        border-radius: 10px;
        border: 2px solid #00ffff;
        background: rgba(0, 255, 255, 0.1);
        color: #00ffff;
        text-align: center;
    }
    
    .ai-feedback {
        background: linear-gradient(45deg, #1a1a2e, #16213e);
        border: 2px solid #ff6b9d;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 0 15px rgba(255, 107, 157, 0.3);
    }
    
    @media (max-width: 768px) {
        .lab-container {
            padding: 10px;
            margin: 5px 0;
        }
        .neon-text {
            font-size: 1.2em;
        }
    }
</style>
""", unsafe_allow_html=True)

@dataclass
class Question:
    id: str
    text: str
    options: List[str]
    category: str
    weight: float = 1.0

@dataclass
class CompatibilityResult:
    percentage: float
    formula: str
    elements: Dict[str, float]
    insights: Dict[str, str]
    milestones: List[str]
    challenges: List[str]
    ai_feedback: str = ""
    ai_tip: str = ""

class ChemistryLab:
    def __init__(self):
        self.questions = self._load_questions()
        self.elements = {
            "H": "Humor", "T": "Trust", "C": "Communication", "A": "Adventure",
            "L": "Love", "P": "Passion", "S": "Stability", "E": "Empathy",
            "F": "Fun", "R": "Respect", "O": "Openness", "G": "Growth"
        }
        self.deepseek_api_key = "sk-e60e809905e245b6ad290433c0064cf2"
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
    
    def _load_questions(self) -> List[Question]:
        """Load engaging 18+ compatibility questions"""
        return [
            Question("q1", "Your ideal Friday night involves:", 
                    ["Netflix and deep conversations", "Exploring a new part of the city", "Hosting friends for dinner", "Learning a new skill together"], 
                    "lifestyle"),
            Question("q2", "When your partner is stressed, you:", 
                    ["Give them space to decompress", "Offer practical solutions", "Listen and provide comfort", "Distract them with something fun"], 
                    "support"),
            Question("q3", "Your biggest relationship dealbreaker is:", 
                    ["Lack of ambition", "Poor communication", "Different life goals", "No sense of humor"], 
                    "boundaries"),
            Question("q4", "When planning your future together, you prioritize:", 
                    ["Financial stability", "Adventure and travel", "Building a family", "Personal growth"], 
                    "future_vision"),
            Question("q5", "Your love language in action looks like:", 
                    ["Surprise notes and compliments", "Cooking their favorite meal", "Planning quality time together", "Spontaneous hugs and kisses"], 
                    "love_expression"),
            Question("q6", "During disagreements, you tend to:", 
                    ["Need time to cool down first", "Talk it out immediately", "Find a compromise quickly", "Use humor to lighten the mood"], 
                    "conflict_style"),
            Question("q7", "Your idea of relationship growth means:", 
                    ["Challenging each other intellectually", "Supporting individual dreams", "Building shared experiences", "Deepening emotional intimacy"], 
                    "growth_mindset"),
            Question("q8", "When it comes to social situations, you:", 
                    ["Love being the center of attention", "Prefer intimate gatherings", "Enjoy meeting new people", "Like observing and listening"], 
                    "social_style"),
            Question("q9", "Your approach to life's big decisions is:", 
                    ["Research everything thoroughly", "Trust your gut instinct", "Seek advice from loved ones", "Make pros and cons lists"], 
                    "decision_making"),
            Question("q10", "In a relationship, you need your partner to:", 
                    ["Be your biggest cheerleader", "Challenge you to grow", "Be your safe haven", "Share your sense of adventure"], 
                    "core_needs"),
        ]
    
    def calculate_compatibility(self, answers1: Dict, answers2: Dict = None) -> CompatibilityResult:
        """Calculate compatibility between partners"""
        if answers2 is None:  # Solo mode
            return self._analyze_solo(answers1)
        else:  # Couple mode
            return self._analyze_couple(answers1, answers2)
    
    def _analyze_solo(self, answers: Dict) -> CompatibilityResult:
        """Analyze individual compatibility profile with local insights and AI feedback"""
        elements = self._calculate_elements(answers)
        formula = self._generate_formula(elements)
        
        # Generate AI-powered compatibility score based on answers
        ai_score = self._get_ai_compatibility_score(answers)
        
        # Get local analysis based on user selections
        local_insights = self._generate_local_insights(answers)
        local_milestones = self._generate_local_milestones(answers)
        local_challenges = self._generate_local_challenges(answers)
        
        # Only use AI for feedback and tip
        ai_feedback = self.get_ai_feedback(answers, compatibility_score=ai_score)
        ai_tip = self.get_ai_relationship_tip(answers, compatibility_score=ai_score)
        
        return CompatibilityResult(
            percentage=ai_score,
            formula=formula,
            elements=elements,
            insights=local_insights,
            milestones=local_milestones,
            challenges=local_challenges,
            ai_feedback=ai_feedback,
            ai_tip=ai_tip
        )
    
    def _get_ai_compatibility_score(self, answers: Dict, answers2: Dict = None) -> float:
        """Generate AI-powered compatibility score based on answers"""
        try:
            answer_summary = self._format_answers_for_ai(answers)
            
            if answers2 is None:
                prompt = f"""Analyze this person's relationship compatibility answers and provide a compatibility score from 65-95 (representing their readiness for relationships, emotional maturity, and dating potential). Consider their communication style, emotional intelligence, relationship goals, and overall compatibility with potential partners.

Their answers:
{answer_summary}

Provide ONLY a number between 65-95 (no text, just the number):"""
            else:
                answer_summary2 = self._format_answers_for_ai(answers2)
                prompt = f"""Analyze these two partners' compatibility based on their answers. Provide a compatibility score from 45-98 based on how well they complement each other, their shared values, communication styles, and relationship goals.

Partner 1:
{answer_summary}

Partner 2:
{answer_summary2}

Provide ONLY a number between 45-98 (no text, just the number):"""
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a relationship compatibility expert. Respond with only a number."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 10,
                "temperature": 0.3
            }
            
            response = requests.post(self.deepseek_url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                score_text = result['choices'][0]['message']['content'].strip()
                # Extract number from response
                import re
                numbers = re.findall(r'\d+\.?\d*', score_text)
                if numbers:
                    score = float(numbers[0])
                    # Ensure score is in valid range
                    if answers2 is None:
                        return max(65, min(95, score))
                    else:
                        return max(45, min(98, score))
            
            # Fallback to calculated score
            return 82.0 if answers2 is None else 75.0
            
        except Exception as e:
            return 82.0 if answers2 is None else 75.0
    
    def _analyze_couple(self, answers1: Dict, answers2: Dict) -> CompatibilityResult:
        """Analyze couple compatibility with AI-powered insights"""
        # Get AI-powered compatibility score
        ai_score = self._get_ai_compatibility_score(answers1, answers2)
        
        # Get comprehensive AI analysis
        ai_insights = self.get_ai_insights(answers1, answers2)
        ai_feedback = self.get_ai_feedback(answers1, answers2, ai_score)
        ai_milestones = self.get_ai_milestones(answers1, answers2)
        ai_challenges = self.get_ai_challenges(answers1, answers2)
        ai_tip = self.get_ai_relationship_tip(answers1, answers2, ai_score)
        
        compatibility = 0.0
        total_weight = 0.0
        
        for question in self.questions:
            if question.id in answers1 and question.id in answers2:
                answer1 = answers1[question.id]
                answer2 = answers2[question.id]
                
                # Calculate similarity score (0-1)
                if answer1 == answer2:
                    score = 1.0
                else:
                    # Different answers get partial compatibility based on category
                    score = self._get_category_compatibility(question.category, answer1, answer2)
                
                compatibility += score * question.weight
                total_weight += question.weight
        
        percentage = ai_score  # Use AI score instead of calculated
        
        # Generate combined elements
        elements1 = self._calculate_elements(answers1)
        elements2 = self._calculate_elements(answers2)
        combined_elements = {}
        
        for element in self.elements:
            combined_elements[element] = (elements1.get(element, 0) + elements2.get(element, 0)) / 2
        
        formula = self._generate_formula(combined_elements)
        
        return CompatibilityResult(
            percentage=percentage,
            formula=formula,
            elements=combined_elements,
            insights=local_insights,
            milestones=local_milestones,
            challenges=local_challenges,
            ai_feedback=ai_feedback,
            ai_tip=ai_tip
        )
    
    def _calculate_elements(self, answers: Dict) -> Dict[str, float]:
        """Calculate relationship elements based on answers"""
        elements = {element: 0.0 for element in self.elements}
        
        # Map answers to elements (simplified logic)
        for q_id, answer in answers.items():
            question = next((q for q in self.questions if q.id == q_id), None)
            if question:
                if question.category == "communication":
                    elements["C"] += 0.3
                    elements["T"] += 0.2
                elif question.category == "lifestyle":
                    elements["A"] += 0.3
                    elements["F"] += 0.2
                elif question.category == "love_language":
                    elements["L"] += 0.4
                    elements["P"] += 0.1
                # Add more mappings...
        
        # Normalize values
        max_val = max(elements.values()) if elements.values() else 1
        if max_val > 0:
            elements = {k: (v / max_val) * 100 for k, v in elements.items()}
        
        return elements
    
    def _get_category_compatibility(self, category: str, answer1: str, answer2: str) -> float:
        """Get compatibility score for different answers in same category"""
        compatibility_matrix = {
            "communication": 0.7,
            "lifestyle": 0.6,
            "values": 0.8,
            "love_language": 0.5,
            "future": 0.9
        }
        return compatibility_matrix.get(category, 0.6)
    
    def _generate_formula(self, elements: Dict[str, float]) -> str:
        """Generate relationship chemical formula"""
        top_elements = sorted(elements.items(), key=lambda x: x[1], reverse=True)[:3]
        formula_parts = []
        
        for element, value in top_elements:
            if value > 20:
                subscript = int(value / 20)
                if subscript > 1:
                    formula_parts.append(f"{element}{subscript}")
                else:
                    formula_parts.append(element)
        
        return "".join(formula_parts) if formula_parts else "H2O"
    
    def _generate_insights(self, answers: Dict, answers2: Dict = None) -> Dict[str, str]:
        """Generate actionable insights"""
        return {
            "love_language": "Your primary love language creates strong emotional bonds",
            "communication": "Direct communication style builds trust and clarity",
            "conflict": "Your conflict resolution approach promotes healthy relationships",
            "goals": "Aligned future goals create lasting partnership potential"
        }
    
    def _generate_local_insights(self, answers: Dict) -> Dict[str, str]:
        """Generate local insights based on user selections"""
        insights = {}
        
        # Analyze love language based on q3
        if "q3" in answers:
            if "cooking" in answers["q3"].lower():
                insights["love_language"] = "Their love language is clearly acts of service, as shown by their preference for cooking their partner's favorite meal to express affection."
            elif "surprise" in answers["q3"].lower():
                insights["love_language"] = "They express love through thoughtful surprises and quality time, showing a gift-giving and quality time love language."
            elif "listen" in answers["q3"].lower():
                insights["love_language"] = "They prioritize emotional connection through words of affirmation and quality conversations."
            else:
                insights["love_language"] = "They show love through physical touch and presence, valuing closeness and intimacy."
        
        # Analyze communication based on q4
        if "q4" in answers:
            if "immediately" in answers["q4"].lower():
                insights["communication"] = "They value open and immediate communication, especially during disagreements, and consider poor communication a major dealbreaker."
            elif "cool down" in answers["q4"].lower():
                insights["communication"] = "They prefer thoughtful communication, taking time to process before discussing important matters."
            elif "write" in answers["q4"].lower():
                insights["communication"] = "They express themselves best through written communication, preferring to organize their thoughts before sharing."
            else:
                insights["communication"] = "They use humor and lightness to navigate difficult conversations and maintain connection."
        
        # Analyze conflict based on q4
        if "q4" in answers:
            if "immediately" in answers["q4"].lower():
                insights["conflict"] = "They prefer to address conflicts head-on by talking things out immediately to resolve issues and maintain harmony."
            else:
                insights["conflict"] = "They take a measured approach to conflict, preferring to think things through before addressing disagreements."
        
        # Analyze goals based on q10
        if "q10" in answers:
            if "cheerleader" in answers["q10"].lower():
                insights["goals"] = "They prioritize emotional support and encouragement in relationships, seeking a partner who believes in their dreams."
            elif "challenge" in answers["q10"].lower():
                insights["goals"] = "They prioritize building a family and deepening emotional intimacy, indicating a strong focus on long-term, meaningful relationship growth."
            elif "safe haven" in answers["q10"].lower():
                insights["goals"] = "They seek security and emotional safety in relationships, valuing stability and trust above all."
            else:
                insights["goals"] = "They prioritize shared adventures and experiences, seeking a partner who shares their sense of exploration."
        
        return insights
    
    def _generate_local_couple_insights(self, answers1: Dict, answers2: Dict) -> Dict[str, str]:
        """Generate local insights for couples based on their selections"""
        insights = {}
        
        # Compare love languages
        love1 = answers1.get("q3", "")
        love2 = answers2.get("q3", "")
        if "cooking" in love1.lower() and "cooking" in love2.lower():
            insights["love_language"] = "Both partners express love through acts of service, creating a harmonious dynamic of mutual care and support."
        elif "cooking" in love1.lower() or "cooking" in love2.lower():
            insights["love_language"] = "One partner shows love through acts of service while the other has different expressions, creating opportunities for learning each other's languages."
        else:
            insights["love_language"] = "Your love languages complement each other beautifully, offering diverse ways to express and receive affection."
        
        # Compare communication styles
        comm1 = answers1.get("q4", "")
        comm2 = answers2.get("q4", "")
        if "immediately" in comm1.lower() and "immediately" in comm2.lower():
            insights["communication"] = "Both partners value direct, immediate communication, creating a foundation for honest and open dialogue."
        else:
            insights["communication"] = "Different communication styles can create rich dialogue, with one partner bringing immediacy and the other bringing thoughtfulness."
        
        # Analyze conflict compatibility
        insights["conflict"] = "Your conflict styles balance emotion and logic, helping you navigate disagreements with both heart and mind."
        
        # Analyze shared goals
        insights["goals"] = "Shared values create a strong foundation for growth, with both partners committed to building something meaningful together."
        
        return insights
    
    def _generate_local_milestones(self, answers: Dict) -> List[str]:
        """Generate 6 local milestones based on user selections"""
        milestones = []
        
        # Base milestones that apply to everyone
        base_milestones = [
            "✅ 1. **Ready for:** Planning a weekend getaway to explore a new city together, combining adventure and quality time.",
            "✅ 2. **Ready for:** Creating a shared 'stress-relief toolkit' with practical solutions you both can use during tough times."
        ]
        milestones.extend(base_milestones)
        
        # Add specific milestones based on answers
        if "q4" in answers and "immediately" in answers["q4"].lower():
            milestones.append("✅ 3. **Ready for:** Scheduling regular check-ins to deepen emotional intimacy and improve communication habits.")
        else:
            milestones.append("✅ 3. **Ready for:** Establishing a comfortable communication rhythm that respects both your processing styles.")
        
        if "q8" in answers and "intimate" in answers["q8"].lower():
            milestones.append("✅ 4. **Ready for:** Hosting a small, intimate dinner party for close friends to blend your social preferences.")
        else:
            milestones.append("✅ 4. **Ready for:** Exploring new social activities that match your energy and comfort levels.")
        
        if "q10" in answers and "challenge" in answers["q10"].lower():
            milestones.append("✅ 5. **Ready for:** Discussing concrete timelines and steps for starting a family, aligning with your shared priority.")
        else:
            milestones.append("✅ 5. **Ready for:** Setting shared goals and supporting each other's personal growth journey.")
        
        milestones.append("✅ 6. **Ready for:** Building deeper emotional intimacy through vulnerability and authentic sharing.")
        
        return milestones
    
    def _generate_local_couple_milestones(self, answers1: Dict, answers2: Dict) -> List[str]:
        """Generate 6 local milestones for couples based on their selections"""
        milestones = [
            "✅ 1. **Ready for:** Planning a weekend getaway to explore a new city together, combining adventure and quality time.",
            "✅ 2. **Ready for:** Creating a shared 'stress-relief toolkit' with practical solutions you both can use during tough times."
        ]
        
        # Communication milestone based on both partners
        comm1 = answers1.get("q4", "")
        comm2 = answers2.get("q4", "")
        if "immediately" in comm1.lower() and "immediately" in comm2.lower():
            milestones.append("✅ 3. **Ready for:** Scheduling regular check-ins to deepen emotional intimacy and improve communication habits.")
        else:
            milestones.append("✅ 3. **Ready for:** Finding your unique communication rhythm that honors both your styles.")
        
        # Social milestone
        social1 = answers1.get("q8", "")
        social2 = answers2.get("q8", "")
        if "intimate" in social1.lower() or "intimate" in social2.lower():
            milestones.append("✅ 4. **Ready for:** Hosting a small, intimate dinner party for close friends to blend your social preferences.")
        else:
            milestones.append("✅ 4. **Ready for:** Exploring social activities that energize both of you and strengthen your bond.")
        
        # Goals milestone
        goal1 = answers1.get("q10", "")
        goal2 = answers2.get("q10", "")
        if "challenge" in goal1.lower() or "challenge" in goal2.lower():
            milestones.append("✅ 5. **Ready for:** Discussing concrete timelines and steps for starting a family, aligning with your shared priority.")
        else:
            milestones.append("✅ 5. **Ready for:** Creating a shared vision for your future and supporting each other's dreams.")
        
        milestones.append("✅ 6. **Ready for:** Deepening your emotional and physical intimacy through intentional connection.")
        
        return milestones
    
    def _generate_local_challenges(self, answers: Dict) -> List[str]:
        """Generate 5 local challenges based on user selections"""
        challenges = []
        
        # Base challenge
        challenges.append("**Experiment 1:** *'Neighborhood Explorer Challenge'* – Take turns blindfolding each other and leading the way to a surprise spot in a new part of the city (trusting your gut instincts). After arriving, share a picnic with homemade versions of each other's favorite meals (love language in action) and discuss one way you'd like to 'grow together' this year (challenge to grow + deepening intimacy).")
        
        # Communication-based challenge
        if "q4" in answers and "immediately" in answers["q4"].lower():
            challenges.append("**Experiment 2:** *'Stress-Solution Speed Round'* – When one of you feels stressed, the other has 10 minutes to prepare a practical solution (like a mini-plan or toolkit) and present it playfully (e.g., as a 'life coach' with a funny hat). Then swap roles next time—combining problem-solving with lightheartedness to ease tension.")
        else:
            challenges.append("**Experiment 2:** *'Thoughtful Response Challenge'* – Practice giving each other space to process by writing thoughtful notes instead of immediate responses during important conversations.")
        
        # Communication experiment
        challenges.append("**Experiment 3:** *'Silent Communication Game'* – Cook a meal together *without speaking* (forcing you to read cues and connect nonverbally). Afterward, debrief: What worked? What frustrated you? How can this improve your everyday communication (tackling the dealbreaker)?")
        
        # Future planning
        if "q10" in answers and "challenge" in answers["q10"].lower():
            challenges.append("**Experiment 4:** *'Future Family Vision Board Night'* – Create a visual representation of your family dreams, including timelines, values you want to instill, and the kind of home environment you want to create together.")
        else:
            challenges.append("**Experiment 4:** *'Adventure Planning Challenge'* – Each plan a surprise adventure for the other that incorporates something they've never tried before but aligns with their interests.")
        
        # Love language experiment
        if "q3" in answers and "cooking" in answers["q3"].lower():
            challenges.append("**Experiment 5:** *'Service Swap Challenge'* – For one week, each partner takes over a task the other usually does, adding your own creative twist to show love through acts of service.")
        else:
            challenges.append("**Experiment 5:** *'Love Language Discovery Week'* – Each day, express love in a different love language and discuss which ones resonate most with each of you.")
        
        return challenges
    
    def _generate_local_couple_challenges(self, answers1: Dict, answers2: Dict) -> List[str]:
        """Generate 5 local challenges for couples based on their selections"""
        challenges = [
            "**Experiment 1:** *'Neighborhood Explorer Challenge'* – Take turns blindfolding each other and leading the way to a surprise spot in a new part of the city (trusting your gut instincts). After arriving, share a picnic with homemade versions of each other's favorite meals (love language in action) and discuss one way you'd like to 'grow together' this year (challenge to grow + deepening intimacy)."
        ]
        
        # Communication challenge based on both partners
        comm1 = answers1.get("q4", "")
        comm2 = answers2.get("q4", "")
        if "immediately" in comm1.lower() and "immediately" in comm2.lower():
            challenges.append("**Experiment 2:** *'Stress-Solution Speed Round'* – When one of you feels stressed, the other has 10 minutes to prepare a practical solution (like a mini-plan or toolkit) and present it playfully (e.g., as a 'life coach' with a funny hat). Then swap roles next time—combining problem-solving with lightheartedness to ease tension.")
        else:
            challenges.append("**Experiment 2:** *'Communication Style Fusion'* – Practice blending your different communication approaches by having one partner lead with immediacy while the other adds thoughtful reflection.")
        
        challenges.append("**Experiment 3:** *'Silent Communication Game'* – Cook a meal together *without speaking* (forcing you to read cues and connect nonverbally). Afterward, debrief: What worked? What frustrated you? How can this improve your everyday communication (tackling the dealbreaker)?")
        
        # Future planning based on goals
        goal1 = answers1.get("q10", "")
        goal2 = answers2.get("q10", "")
        if "challenge" in goal1.lower() or "challenge" in goal2.lower():
            challenges.append("**Experiment 4:** *'Future Family Vision Board Night'* – Create a visual representation of your family dreams, including timelines, values you want to instill, and the kind of home environment you want to create together.")
        else:
            challenges.append("**Experiment 4:** *'Shared Dreams Workshop'* – Each create a vision board of your individual dreams, then work together to create a third board showing how your dreams can support and enhance each other.")
        
        # Love language experiment
        love1 = answers1.get("q3", "")
        love2 = answers2.get("q3", "")
        if "cooking" in love1.lower() or "cooking" in love2.lower():
            challenges.append("**Experiment 5:** *'Service Swap Challenge'* – For one week, each partner takes over a task the other usually does, adding your own creative twist to show love through acts of service.")
        else:
            challenges.append("**Experiment 5:** *'Love Language Exploration Week'* – Each day, one partner expresses love in the other's preferred love language, then discuss what felt most meaningful.")
        
        return challenges
    
    def get_ai_feedback(self, answers: Dict, answers2: Dict = None, compatibility_score: float = 0) -> str:
        """Get AI-powered personalized feedback using DeepSeek"""
        try:
            # Format answers for better AI understanding
            answer_summary = self._format_answers_for_ai(answers)
            
            if answers2 is None:
                prompt = f"""Based on this person's relationship compatibility answers, provide exactly 2 lines of honest, insightful feedback about their relationship style and potential. Be encouraging but realistic. Keep it under 50 words total.

Their answers:
{answer_summary}

Provide exactly 2 lines of feedback (no extra text):"""
            else:
                answer_summary2 = self._format_answers_for_ai(answers2)
                prompt = f"""Based on these two partners' compatibility answers and their {compatibility_score:.1f}% compatibility score, provide exactly 2 lines of honest feedback about their relationship potential. Be encouraging but realistic. Keep it under 50 words total.

Partner 1:
{answer_summary}

Partner 2:
{answer_summary2}

Compatibility: {compatibility_score:.1f}%

Provide exactly 2 lines of feedback (no extra text):"""
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a relationship compatibility expert. Provide honest, insightful, and encouraging feedback in exactly 2 lines. No extra formatting or text."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 100,
                "temperature": 0.7
            }
            
            response = requests.post(self.deepseek_url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                feedback = result['choices'][0]['message']['content'].strip()
                # Clean up any markdown formatting
                feedback = feedback.replace('```', '').strip()
                return feedback
            else:
                return self._get_fallback_feedback(answers, answers2, compatibility_score)
                
        except Exception as e:
            return self._get_fallback_feedback(answers, answers2, compatibility_score)
    
    def get_ai_relationship_tip(self, answers: Dict, answers2: Dict = None, compatibility_score: float = 0) -> str:
        """Get creative AI-powered relationship tip"""
        try:
            # Format answers for better AI understanding
            answer_summary = self._format_answers_for_ai(answers)
            
            if answers2 is None:
                prompt = f"""Based on this SINGLE person's relationship compatibility answers, provide 1 creative, actionable dating/relationship tip for someone who is currently single or dating. Focus on self-improvement, dating strategies, or preparing for relationships. Make it fun, specific, and something they can actually do alone or while dating. Keep it under 30 words.

Their answers:
{answer_summary}

Provide one creative tip for a single person (no extra text):"""
            else:
                answer_summary2 = self._format_answers_for_ai(answers2)
                prompt = f"""Based on these two partners' compatibility answers and their {compatibility_score:.1f}% compatibility score, provide 1 creative, actionable relationship tip they can try together. Make it fun, specific, and something they can actually do. Keep it under 30 words.

Partner 1:
{answer_summary}

Partner 2:
{answer_summary2}

Compatibility: {compatibility_score:.1f}%

Provide one creative tip for this couple (no extra text):"""
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a creative relationship coach. Provide one specific, actionable tip. Keep it under 30 words."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 60,
                "temperature": 0.8
            }
            
            response = requests.post(self.deepseek_url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                tip = result['choices'][0]['message']['content'].strip()
                # Clean up any markdown formatting
                tip = tip.replace('```', '').strip()
                return tip
            else:
                return self._get_fallback_tip(answers, answers2)
                
        except Exception as e:
            return self._get_fallback_tip(answers, answers2)
    
    def _format_answers_for_ai(self, answers: Dict) -> str:
        """Format answers in a readable way for AI analysis"""
        formatted = []
        for q_id, answer in answers.items():
            question = next((q for q in self.questions if q.id == q_id), None)
            if question:
                formatted.append(f"{question.text} -> {answer}")
        return "\n".join(formatted)
    
    def _get_fallback_feedback(self, answers: Dict, answers2: Dict = None, compatibility_score: float = 0) -> str:
        """Fallback feedback when AI is unavailable"""
        if answers2 is None:
            return "You show strong relationship potential with clear communication preferences and emotional awareness. Your thoughtful approach to relationships suggests you're ready for meaningful connections."
        else:
            return f"With {compatibility_score:.1f}% compatibility, you both bring complementary strengths to the relationship. Your different approaches can create a balanced and dynamic partnership."
    
    def _get_fallback_tip(self, answers: Dict, answers2: Dict = None) -> str:
        """Fallback relationship tip when AI is unavailable"""
        if answers2 is None:
            return "Practice active listening on your next date - put your phone away and ask follow-up questions to show genuine interest."
        else:
            return "Try the '5-minute rule' - spend 5 minutes each day sharing something new you learned or experienced with each other."
    
    def _analyze_couple(self, answers1: Dict, answers2: Dict) -> CompatibilityResult:
        """Analyze couple compatibility with AI-powered insights"""
        # Get AI-powered compatibility score
        ai_score = self._get_ai_compatibility_score(answers1, answers2)
        
        # Get comprehensive AI analysis
        ai_insights = self.get_ai_insights(answers1, answers2)
        ai_feedback = self.get_ai_feedback(answers1, answers2, ai_score)
        ai_milestones = self.get_ai_milestones(answers1, answers2)
        ai_challenges = self.get_ai_challenges(answers1, answers2)
        ai_tip = self.get_ai_relationship_tip(answers1, answers2, ai_score)
        
        compatibility = 0.0
        total_weight = 0.0
        
        for question in self.questions:
            if question.id in answers1 and question.id in answers2:
                answer1 = answers1[question.id]
                answer2 = answers2[question.id]
                
                # Calculate similarity score (0-1)
                if answer1 == answer2:
                    score = 1.0
                else:
                    # Different answers get partial compatibility based on category
                    score = self._get_category_compatibility(question.category, answer1, answer2)
                
                compatibility += score * question.weight
                total_weight += question.weight
        
        percentage = ai_score  # Use AI score instead of calculated
        
        # Generate combined elements
        elements1 = self._calculate_elements(answers1)
        elements2 = self._calculate_elements(answers2)
        combined_elements = {}
        
        for element in self.elements:
            combined_elements[element] = (elements1.get(element, 0) + elements2.get(element, 0)) / 2
        
        formula = self._generate_formula(combined_elements)
        
        return CompatibilityResult(
            percentage=percentage,
            formula=formula,
        elements=combined_elements,
        insights=ai_insights,
        milestones=ai_milestones,
        challenges=ai_challenges,
        ai_feedback=ai_feedback,
        ai_tip=ai_tip
    )

def _calculate_elements(self, answers: Dict) -> Dict[str, float]:
    """Calculate relationship elements based on answers"""
    elements = {element: 0.0 for element in self.elements}
    
    # Map answers to elements (simplified logic)
    for q_id, answer in answers.items():
        question = next((q for q in self.questions if q.id == q_id), None)
        if question:
            if question.category == "communication":
                elements["C"] += 0.3
                elements["T"] += 0.2
            elif question.category == "lifestyle":
                elements["A"] += 0.3
                elements["F"] += 0.2
            elif question.category == "love_language":
                elements["L"] += 0.4
                elements["P"] += 0.1
            # Add more mappings...
    
    # Normalize values
    max_val = max(elements.values()) if elements.values() else 1
    if max_val > 0:
        elements = {k: (v / max_val) * 100 for k, v in elements.items()}
    
    return elements

def _get_category_compatibility(self, category: str, answer1: str, answer2: str) -> float:
    """Get compatibility score for different answers in same category"""
    compatibility_matrix = {
        "communication": 0.7,
        "lifestyle": 0.6,
        "values": 0.8,
        "love_language": 0.5,
        "future": 0.9
    }
    return compatibility_matrix.get(category, 0.6)

def _generate_formula(self, elements: Dict[str, float]) -> str:
    """Generate relationship chemical formula"""
    top_elements = sorted(elements.items(), key=lambda x: x[1], reverse=True)[:3]
    formula_parts = []
    
    for element, value in top_elements:
        if value > 20:
            subscript = int(value / 20)
            if subscript > 1:
                formula_parts.append(f"{element}{subscript}")
            else:
                formula_parts.append(element)
    
    return "".join(formula_parts) if formula_parts else "H2O"

def _generate_insights(self, answers: Dict, answers2: Dict = None) -> Dict[str, str]:
    """Generate actionable insights"""
    return {
        "love_language": "Your primary love language creates strong emotional bonds",
        "communication": "Direct communication style builds trust and clarity",
        "conflict": "Your conflict resolution approach promotes healthy relationships",
        "goals": "Aligned future goals create lasting partnership potential"
    }

def get_ai_milestones(self, answers: Dict, answers2: Dict = None) -> List[str]:
    """Generate AI-powered relationship milestones with 5-6 personalized outputs"""
    try:
        # Create a more readable summary of answers for AI
        answer_summary = self._format_answers_for_ai(answers)
        
        if answers2 is None:
            prompt = f"""Based on this person's relationship compatibility answers, generate exactly 6 personalized relationship milestones they're ready for. Each milestone should be highly specific to their answers, personality traits, and relationship style. Make them progressive, meaningful, and actionable. Format each as "✅ [number]. **Ready for:** [specific milestone with personal details]".

Their answers:
{answer_summary}

Analyze their communication style, love language preferences, conflict resolution approach, relationship goals, and personality traits to create milestones that feel personally tailored to them.

Provide exactly 6 milestones, one per line:"""
        else:
            answer_summary2 = self._format_answers_for_ai(answers2)
            prompt = f"""Based on these two partners' compatibility answers, generate exactly 6 personalized relationship milestones they're ready for together. Each should be highly specific to their combined personalities, compatibility dynamics, and shared values. Format each as "✅ [number]. **Ready for:** [specific milestone with personal details]".

Partner 1:
{answer_summary}

Partner 2:
{answer_summary2}

Analyze how their communication styles complement each other, their shared goals, how they handle conflict together, and their unique dynamic to create milestones that feel personally tailored to this specific couple.

Provide exactly 6 milestones, one per line:"""
        
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a relationship expert who creates highly personalized, specific milestones based on individual personality traits and relationship dynamics. Always generate exactly 6 detailed milestones."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.8
        }
        
        response = requests.post(self.deepseek_url, headers=headers, json=data, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            milestones_text = result['choices'][0]['message']['content'].strip()
            milestones = [line.strip() for line in milestones_text.split('\n') if line.strip()]
            return milestones[:6] if milestones else self._generate_fallback_milestones(answers, answers2)
        else:
            return self._generate_fallback_milestones(answers, answers2)
            
    except Exception as e:
        return self._generate_fallback_milestones(answers, answers2)
    
    def get_ai_challenges(self, answers: Dict, answers2: Dict = None) -> List[str]:
        """Generate AI-powered relationship challenges/experiments with 5-6 personalized outputs"""
        try:
            answer_summary = self._format_answers_for_ai(answers)
            
            if answers2 is None:
                prompt = f"""Based on this person's relationship compatibility answers, generate exactly 5 personalized relationship experiments/challenges they can try (either solo for self-improvement or on dates). Each should be highly specific to their personality traits, communication style, and relationship goals. Make them creative, actionable, and fun.

Their answers:
{answer_summary}

Analyze their love language, communication preferences, conflict style, and goals to create experiments that feel personally tailored to them.

Provide exactly 5 experiments, format each as "**Experiment [number]:** *"[Creative Name]"* – [Detailed description with personal elements]":"""
            else:
                answer_summary2 = self._format_answers_for_ai(answers2)
                prompt = f"""Based on these two partners' compatibility answers, generate exactly 5 personalized relationship experiments/challenges they can try together. Each should be highly specific to their combined personalities, compatibility dynamics, and how they complement each other. Make them creative, actionable, and fun.

Partner 1:
{answer_summary}

Partner 2:
{answer_summary2}

Analyze how their communication styles work together, their shared interests, how they handle challenges, and their unique dynamic to create experiments that feel personally tailored to this specific couple.

Provide exactly 5 experiments, format each as "**Experiment [number]:** *"[Creative Name]"* – [Detailed description with personal elements for this couple]":"""
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a creative relationship coach who designs highly personalized, specific experiments based on individual personality traits and relationship dynamics. Always generate exactly 5 detailed experiments."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 600,
                "temperature": 0.8
            }
            
            response = requests.post(self.deepseek_url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                challenges_text = result['choices'][0]['message']['content'].strip()
                # Clean up and split into list
                challenges = [line.strip() for line in challenges_text.split('\n') if line.strip() and 'Experiment' in line]
                return challenges[:5] if challenges else self._generate_fallback_challenges(answers, answers2)
            else:
                return self._generate_fallback_challenges(answers, answers2)
                
        except Exception as e:
            return self._generate_fallback_challenges(answers, answers2)
    
    def _generate_fallback_milestones(self, answers: Dict, answers2: Dict = None) -> List[str]:
        """Fallback milestones when AI is unavailable"""
        return [
            "Ready for: Deep emotional conversations",
            "Ready for: Planning future adventures together",
            "Ready for: Meeting each other's families",
            "Ready for: Moving in together",
            "Ready for: Long-term commitment discussions"
        ]
    
    def _generate_fallback_challenges(self, answers: Dict, answers2: Dict = None) -> List[str]:
        """Fallback challenges when AI is unavailable"""
        return [
            "Experiment 1: Try each other's favorite hobby for a week",
            "Experiment 2: Plan a surprise date in your partner's love language",
            "Experiment 3: Have a 'no phones' dinner conversation",
            "Experiment 4: Create a shared bucket list",
            "Experiment 5: Write love letters to read in 5 years"
        ]
    
    def _generate_couple_insights(self, answers1: Dict, answers2: Dict) -> Dict[str, str]:
        """Generate insights for couples"""
        return {
            "love_language": "Your love languages complement each other beautifully",
            "communication": "Different communication styles can create rich dialogue",
            "conflict": "Your conflict styles balance emotion and logic",
            "goals": "Shared values create a strong foundation for growth"
        }
    
    def get_ai_feedback(self, answers: Dict, answers2: Dict = None, compatibility_score: float = 0) -> str:
        """Get AI-powered personalized feedback using DeepSeek"""
        try:
            # Format answers for better AI understanding
            answer_summary = self._format_answers_for_ai(answers)
            
            if answers2 is None:
                prompt = f"""Based on this person's relationship compatibility answers, provide exactly 2 lines of honest, insightful feedback about their relationship style and potential. Be encouraging but realistic. Keep it under 50 words total.

Their answers:
{answer_summary}

Provide exactly 2 lines of feedback (no extra text):"""
            else:
                answer_summary2 = self._format_answers_for_ai(answers2)
                prompt = f"""Based on these two partners' compatibility answers and their {compatibility_score:.1f}% compatibility score, provide exactly 2 lines of honest feedback about their relationship potential. Be encouraging but realistic. Keep it under 50 words total.

Partner 1:
{answer_summary}

Partner 2:
{answer_summary2}

Compatibility: {compatibility_score:.1f}%

Provide exactly 2 lines of feedback (no extra text):"""
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a relationship compatibility expert. Provide honest, insightful, and encouraging feedback in exactly 2 lines. No extra formatting or text."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 100,
                "temperature": 0.7
            }
            
            response = requests.post(self.deepseek_url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                feedback = result['choices'][0]['message']['content'].strip()
                # Clean up any markdown formatting
                feedback = feedback.replace('```', '').strip()
                return feedback
            else:
                return self._get_fallback_feedback(answers, answers2, compatibility_score)
                
        except Exception as e:
            return self._get_fallback_feedback(answers, answers2, compatibility_score)
    
    def get_ai_insights(self, answers: Dict, answers2: Dict = None) -> Dict[str, str]:
        """Get AI-powered intelligent insights based on actual answers"""
        try:
            # Create a more readable summary of answers for AI
            answer_summary = self._format_answers_for_ai(answers)
            
            if answers2 is None:
                prompt = f"""Analyze this person's relationship compatibility answers and provide 4 personalized insights.

Their answers: {answer_summary}

Provide insights in this exact JSON format:
{{
  "love_language": "One sentence about their love language based on their specific answers",
  "communication": "One sentence about their communication style based on their answers", 
  "conflict": "One sentence about their conflict approach based on their answers",
  "goals": "One sentence about their relationship goals based on their answers"
}}

Return ONLY the JSON, no other text."""
            else:
                answer_summary2 = self._format_answers_for_ai(answers2)
                prompt = f"""Analyze these two partners' compatibility answers and provide 4 insights about their dynamic.

Partner 1: {answer_summary}
Partner 2: {answer_summary2}

Provide insights in this exact JSON format:
{{
  "love_language": "How their love languages work together",
  "communication": "How their communication styles complement each other",
  "conflict": "How their conflict styles balance each other", 
  "goals": "How their goals align or complement"
}}

Return ONLY the JSON, no other text."""
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a relationship compatibility expert. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 300,
                "temperature": 0.6
            }
            
            response = requests.post(self.deepseek_url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                insights_text = result['choices'][0]['message']['content'].strip()
                
                # Clean up the response - remove markdown formatting if present
                if insights_text.startswith('```json'):
                    insights_text = insights_text.replace('```json', '').replace('```', '').strip()
                elif insights_text.startswith('```'):
                    insights_text = insights_text.replace('```', '').strip()
                
                # Extract JSON if it's wrapped in other text
                if '{' in insights_text and '}' in insights_text:
                    start = insights_text.find('{')
                    end = insights_text.rfind('}') + 1
                    insights_text = insights_text[start:end]
                
                try:
                    insights = json.loads(insights_text)
                    # Validate that we have all required keys
                    required_keys = ['love_language', 'communication', 'conflict', 'goals']
                    if all(key in insights for key in required_keys):
                        return insights
                    else:
                        return self._get_fallback_insights(answers, answers2)
                except json.JSONDecodeError:
                    return self._get_fallback_insights(answers, answers2)
            else:
                return self._get_fallback_insights(answers, answers2)
                
        except Exception as e:
            return self._get_fallback_insights(answers, answers2)
    
    def _format_answers_for_ai(self, answers: Dict) -> str:
        """Format answers in a readable way for AI analysis"""
        formatted = []
        for q_id, answer in answers.items():
            question = next((q for q in self.questions if q.id == q_id), None)
            if question:
                formatted.append(f"{question.text} -> {answer}")
        return "\n".join(formatted)
    
    def get_ai_relationship_tip(self, answers: Dict, answers2: Dict = None, compatibility_score: float = 0) -> str:
        """Get creative AI-powered relationship tip"""
        try:
            # Format answers for better AI understanding
            answer_summary = self._format_answers_for_ai(answers)
            
            if answers2 is None:
                prompt = f"""Based on this SINGLE person's relationship compatibility answers, provide 1 creative, actionable dating/relationship tip for someone who is currently single or dating. Focus on self-improvement, dating strategies, or preparing for relationships. Make it fun, specific, and something they can actually do alone or while dating. Keep it under 30 words.

Their answers:
{answer_summary}

Provide one creative tip for a single person (no extra text):"""
            else:
                answer_summary2 = self._format_answers_for_ai(answers2)
                prompt = f"""Based on these two partners' compatibility answers and their {compatibility_score:.1f}% compatibility score, provide 1 creative, actionable relationship tip specifically for this couple. Make it fun, specific, and something they can do together. Keep it under 30 words.

Partner 1:
{answer_summary}

Partner 2:
{answer_summary2}

Compatibility: {compatibility_score:.1f}%

Provide one creative couple tip (no extra text):"""
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a creative relationship coach. Provide fun, actionable, and personalized relationship tips. No extra formatting or text."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 80,
                "temperature": 0.8
            }
            
            response = requests.post(self.deepseek_url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                tip = result['choices'][0]['message']['content'].strip()
                # Clean up any markdown formatting
                tip = tip.replace('```', '').strip()
                return tip
            else:
                return self._get_fallback_tip(answers, answers2)
                
        except Exception as e:
            return self._get_fallback_tip(answers, answers2)
    
    def _get_fallback_feedback(self, answers: Dict, answers2: Dict = None, compatibility_score: float = 0) -> str:
        """Fallback feedback when AI is unavailable"""
        if answers2 is None:
            return "Your relationship style shows great potential for meaningful connections.\nFocus on communication and shared values to build lasting partnerships."
        else:
            if compatibility_score > 75:
                return "You two have excellent compatibility with strong shared values and complementary styles.\nYour relationship has all the ingredients for long-term success and growth."
            elif compatibility_score > 50:
                return "You have good compatibility with some areas to explore and grow together.\nFocus on your shared strengths while working on communication differences."
            else:
                return "You have different approaches that could either challenge or complement each other.\nOpen communication and mutual understanding will be key to your success."
    
    def _get_fallback_insights(self, answers: Dict, answers2: Dict = None) -> Dict[str, str]:
        """Fallback insights when AI is unavailable"""
        if answers2 is None:
            return {
                "love_language": "Your love language preferences suggest you value meaningful emotional connection",
                "communication": "Your communication style indicates you prefer authentic and direct interactions",
                "conflict": "Your approach to conflict shows you prioritize resolution and understanding",
                "goals": "Your future vision demonstrates strong personal values and clear direction"
            }
        else:
            return {
                "love_language": "Your love languages create opportunities for deep emotional bonding",
                "communication": "Your communication styles can complement each other beautifully",
                "conflict": "Your conflict resolution approaches balance different perspectives effectively",
                "goals": "Your shared values provide a strong foundation for future growth together"
            }
    
    def _get_fallback_tip(self, answers: Dict, answers2: Dict = None) -> str:
        """Fallback relationship tip when AI is unavailable"""
        tips_solo = [
            "Take the 5-love-languages quiz to understand your dating style better for future relationships!",
            "Create a personal 'relationship vision board' to clarify what you want in a partner!",
            "Practice daily self-appreciation - loving yourself first makes you more attractive to others."
        ]
        
        tips_couple = [
            "Plan a monthly 'adventure date' where you take turns surprising each other with new experiences!",
            "Create a shared playlist and add one song each week that reminds you of your partner.",
            "Try cooking a meal from a different culture together every month - it's bonding and delicious!"
        ]
        
        import random
        if answers2 is None:
            return random.choice(tips_solo)
        else:
            return random.choice(tips_couple)

def main():
    # Initialize session state
    if 'lab' not in st.session_state:
        st.session_state.lab = ChemistryLab()
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers1' not in st.session_state:
        st.session_state.answers1 = {}
    if 'answers2' not in st.session_state:
        st.session_state.answers2 = {}
    if 'results' not in st.session_state:
        st.session_state.results = None

    # Header
    st.markdown('<h1 class="neon-text">🧪 Chemistry Lab - Relationship Compatibility</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #00ffff; font-size: 18px;">Discover the science behind your love connection</p>', unsafe_allow_html=True)

    # Mode selection
    if st.session_state.mode is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="lab-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="neon-text">Choose Your Experiment</h3>', unsafe_allow_html=True)
            
            if st.button("🔬 Solo Analysis", key="solo", help="Analyze your dating chemistry"):
                st.session_state.mode = "solo"
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("👫 Couple Analysis", key="couple", help="Both partners answer together"):
                st.session_state.mode = "couple"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add some visual elements
            st.markdown("""
            <div style="text-align: center; margin: 20px;">
                <div class="beaker" style="display: inline-block;"></div>
                <div class="beaker" style="display: inline-block;"></div>
                <div class="beaker" style="display: inline-block;"></div>
            </div>
            """, unsafe_allow_html=True)

    # Question flow
    elif st.session_state.results is None:
        show_questions()
    
    # Results
    else:
        show_results()

def show_questions():
    """Display questions with lab theme"""
    questions = st.session_state.lab.questions
    current_q = st.session_state.current_question
    
    if current_q < len(questions):
        question = questions[current_q]
        
        # Progress bar
        progress = (current_q + 1) / len(questions)
        st.markdown(f"""
        <div class="compatibility-meter" style="width: {progress * 100}%; margin-bottom: 20px;"></div>
        <p style="color: #00ffff;">Experiment Progress: {current_q + 1}/{len(questions)}</p>
        """, unsafe_allow_html=True)
        
        # Question container
        st.markdown('<div class="lab-container">', unsafe_allow_html=True)
        st.markdown(f'<h3 class="neon-text">Question {current_q + 1}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 18px; color: #e0e0e0;">{question.text}</p>', unsafe_allow_html=True)
        
        # Answer options
        col1, col2 = st.columns(2)
        
        if st.session_state.mode == "solo":
            with col1:
                answer1 = st.radio("Your Answer:", question.options, key=f"q1_{current_q}")
                if st.button("Next Question", key="next1"):
                    st.session_state.answers1[question.id] = answer1
                    st.session_state.current_question += 1
                    st.rerun()
        
        else:  # Couple mode
            with col1:
                st.markdown('<h4 style="color: #ff6b9d;">Partner 1</h4>', unsafe_allow_html=True)
                answer1 = st.radio("Partner 1 Answer:", question.options, key=f"q1_{current_q}")
            
            with col2:
                st.markdown('<h4 style="color: #4ecdc4;">Partner 2</h4>', unsafe_allow_html=True)
                answer2 = st.radio("Partner 2 Answer:", question.options, key=f"q2_{current_q}")
            
            if st.button("Next Question", key="next_both"):
                st.session_state.answers1[question.id] = answer1
                st.session_state.answers2[question.id] = answer2
                st.session_state.current_question += 1
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add bubbling animation
        if current_q % 2 == 0:
            st.markdown("""
            <div style="text-align: center;">
                <div class="molecule"></div>
                <div class="molecule"></div>
                <div class="molecule"></div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Calculate results with AI feedback, insights, tips, milestones, and challenges
        with st.spinner('🧪 Analyzing your chemistry...'):
            if st.session_state.mode == "solo":
                results = st.session_state.lab.calculate_compatibility(st.session_state.answers1)
                ai_feedback = st.session_state.lab.get_ai_feedback(st.session_state.answers1)
                ai_tip = st.session_state.lab.get_ai_relationship_tip(st.session_state.answers1)
                ai_challenges = st.session_state.lab.get_ai_challenges(st.session_state.answers1)
            else:
                results = st.session_state.lab.calculate_compatibility(
                    st.session_state.answers1, st.session_state.answers2
                )
                ai_feedback = st.session_state.lab.get_ai_feedback(
                    st.session_state.answers1, st.session_state.answers2, results.percentage
                )

                ai_tip = st.session_state.lab.get_ai_relationship_tip(
                    st.session_state.answers1, st.session_state.answers2, results.percentage
                )
                ai_milestones = st.session_state.lab.get_ai_milestones(
                    st.session_state.answers1, st.session_state.answers2
                )
                ai_challenges = st.session_state.lab.get_ai_challenges(
                    st.session_state.answers1, st.session_state.answers2
                )
            
            results.ai_feedback = ai_feedback
            results.insights = ai_insights  # Replace default insights with AI-generated ones
            results.milestones = ai_milestones  # Replace default milestones with AI-generated ones
            results.challenges = ai_challenges  # Replace default challenges with AI-generated ones
            results.ai_tip = ai_tip
            st.session_state.results = results
        st.rerun()

def show_results():
    """Display compatibility results with lab report theme"""
    results = st.session_state.results
    
    st.markdown('<h2 class="neon-text">🧪 Lab Report - Compatibility Analysis</h2>', unsafe_allow_html=True)
    
    # AI Feedback Section (Mobile-first)
    if hasattr(results, 'ai_feedback') and results.ai_feedback:
        st.markdown('<div class="ai-feedback">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #ff6b9d; text-align: center; margin-bottom: 10px;">🤖 AI Analysis</h3>', unsafe_allow_html=True)
        feedback_lines = results.ai_feedback.split('\n')
        for line in feedback_lines:
            if line.strip():
                st.markdown(f'<p style="color: #e0e0e0; text-align: center; font-size: 16px; margin: 5px 0;">{line.strip()}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Compatibility percentage with visual meter
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 style="text-align: center; color: #00ff80; font-size: 42px;">{results.percentage:.1f}%</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #00ffff; font-size: 18px;">Compatibility Score</p>', unsafe_allow_html=True)
    
    # Visual compatibility meter
    meter_color = "#00ff80" if results.percentage > 70 else "#ffff00" if results.percentage > 50 else "#ff6b9d"
    st.markdown(f"""
    <div style="background: #333; height: 25px; border-radius: 15px; margin: 15px 0;">
        <div style="background: {meter_color}; height: 25px; width: {results.percentage}%; border-radius: 15px; 
                    box-shadow: 0 0 15px {meter_color};"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chemical Formula
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="lab-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="neon-text">🧬 Your Relationship Formula</h3>', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color: #00ff80; font-size: 36px; text-align: center;">{results.formula}</h2>', unsafe_allow_html=True)
        
        # Decode formula
        st.markdown('<h4 style="color: #00ffff;">Formula Breakdown:</h4>', unsafe_allow_html=True)
        lab = st.session_state.lab
        for char in results.formula:
            if char.isalpha() and char in lab.elements:
                st.markdown(f'<p><strong>{char}</strong> = {lab.elements[char]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="lab-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="neon-text">⚛️ Relationship Elements</h3>', unsafe_allow_html=True)
        
        # Create periodic table visualization
        fig = go.Figure()
        
        elements_data = [(k, v, st.session_state.lab.elements[k]) for k, v in results.elements.items() if v > 10]
        elements_data.sort(key=lambda x: x[1], reverse=True)
        
        for i, (element, value, name) in enumerate(elements_data[:6]):
            fig.add_trace(go.Bar(
                x=[name],
                y=[value],
                name=f"{element} - {name}",
                marker_color=f"rgba(0, 255, {255-i*30}, 0.8)",
                text=f"{value:.1f}%",
                textposition="auto"
            ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0',
            showlegend=False,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights and Recommendations
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="neon-text">🔬 Lab Analysis & Insights</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4 style="color: #ff6b9d;">Compatibility Insights</h4>', unsafe_allow_html=True)
        for category, insight in results.insights.items():
            st.markdown(f'<p><strong>{category.replace("_", " ").title()}:</strong> {insight}</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h4 style="color: #4ecdc4;">Relationship Milestones</h4>', unsafe_allow_html=True)
        for milestone in results.milestones:
            st.markdown(f'<p>✅ {milestone}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Fun Challenges
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="neon-text">🎯 Chemistry Experiments to Try</h3>', unsafe_allow_html=True)
    
    for i, challenge in enumerate(results.challenges, 1):
        st.markdown(f'<p><strong>Experiment {i}:</strong> {challenge}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI-Powered Relationship Tip
    if hasattr(results, 'ai_tip') and results.ai_tip:
        st.markdown('<div class="lab-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="neon-text">💡 Your Personalized Relationship Tip</h3>', unsafe_allow_html=True)
        st.markdown(f'<div style="background: linear-gradient(45deg, #ff6b9d, #4ecdc4); padding: 15px; border-radius: 10px; margin: 10px 0;">', unsafe_allow_html=True)
        st.markdown(f'<p style="color: white; font-size: 16px; text-align: center; margin: 0; font-weight: bold;">{results.ai_tip}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Share buttons
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("🔄 New Analysis", key="restart"):
            # Reset session state
            for key in ['mode', 'current_question', 'answers1', 'answers2', 'results']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
