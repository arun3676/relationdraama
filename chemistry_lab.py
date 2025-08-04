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
    
    .molecule {
        display: inline-block;
        margin: 5px;
        padding: 8px 12px;
        background: rgba(0, 255, 255, 0.2);
        border: 1px solid #00ffff;
        border-radius: 20px;
        font-size: 14px;
        animation: glow 2s infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 5px rgba(0, 255, 255, 0.5); }
        to { box-shadow: 0 0 15px rgba(0, 255, 255, 0.8); }
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
    personal_trait: str

class ChemistryLab:
    def __init__(self):
        self.questions = self._load_questions()
        self.elements = {
            "H": "Humor", 
            "T": "Trust", 
            "P": "Passion",
            "L": "Love",
            "C": "Communication",
            "S": "Stability",
            "A": "Adventure",
            "E": "Empathy",
            "G": "Growth",
            "R": "Respect",
            "F": "Fun"
        }
    
    def _load_questions(self) -> List[Question]:
        """Load engaging compatibility questions"""
        return [
            # Question 1 - Physical Affection
            Question(
                id="q1",
                text="How do you best show affection after a long day?",
                options=[
                    "A long, warm hug",
                    "A passionate kiss",
                    "Making them a favorite drink or snack",
                    "Asking about their day and truly listening"
                ],
                category="affection",
                weight=1.3
            ),
            
            # Question 2 - Conflict Approach
            Question(
                id="q2",
                text="When you hurt your partner's feelings, you tend to:",
                options=[
                    "Apologize quickly and seek forgiveness",
                    "Explain your intentions to clarify the misunderstanding",
                    "Give them space before re-engaging",
                    "Feel guilty and withdraw for a while"
                ],
                category="conflict",
                weight=1.5
            ),

            # Question 3 - Financial Disagreements
            Question(
                id="q3",
                text="A surprise, large expense comes up. Your reaction is:",
                options=[
                    "'We'll tackle it together, let's make a plan.'",
                    "'Why didn't we budget for this?' (Stress)",
                    "'It's only money, we'll figure it out.' (Casual)",
                    "To quietly research solutions on your own first"
                ],
                category="finance",
                weight=1.4
            ),

            # Question 4 - Social Energy
            Question(
                id="q4",
                text="It's Saturday night. You'd rather:",
                options=[
                    "Host a small get-together with close friends",
                    "Go to a loud concert or busy bar",
                    "Stay in for a movie marathon, just you two",
                    "Have a quiet dinner out at a nice restaurant"
                ],
                category="social",
                weight=1.1
            ),

            # Question 5 - Future Planning
            Question(
                id="q5",
                text="When you think about the future, you focus most on:",
                options=[
                    "Our shared career and financial goals",
                    "The adventures we'll have and places we'll see",
                    "Building a comfortable and stable home life",
                    "Our growth as individuals within the relationship"
                ],
                category="future",
                weight=1.2
            ),

            # Question 6 - Annoyances
            Question(
                id="q6",
                text="What's a minor annoyance that secretly gets to you?",
                options=[
                    "Leaving wet towels on the bed",
                    "Being consistently 10 minutes late",
                    "Loud chewing or eating habits",
                    "Leaving dishes in the sink for 'later'"
                ],
                category="habits",
                weight=1.0
            ),

            # Question 7 - Intimacy
            Question(
                id="q7",
                text="What's the key to great intimacy for you?",
                options=[
                    "Emotional vulnerability and deep talks",
                    "Spontaneous physical connection",
                    "Shared humor and playful teasing",
                    "Feeling safe and completely accepted"
                ],
                category="intimacy",
                weight=1.5
            ),

            # Question 8 - Support Style
            Question(
                id="q8",
                text="When your partner is stressed, your instinct is to:",
                options=[
                    "Offer practical solutions and a plan",
                    "Provide physical comfort like a back rub",
                    "Listen without judgment and validate their feelings",
                    "Distract them with a fun activity or joke"
                ],
                category="support",
                weight=1.4
            )
        ]
    
    def calculate_compatibility(self, answers1: Dict, answers2: Dict = None) -> CompatibilityResult:
        """Calculate compatibility between partners"""
        if answers2 is None:
            return self._analyze_solo(answers1)
        else:
            return self._analyze_couple(answers1, answers2)
    
    def _analyze_solo(self, answers: Dict) -> CompatibilityResult:
        """Analyze individual compatibility profile"""
        elements = self._calculate_elements(answers)
        formula = self._generate_formula(elements)
        
        # Generate a self-compatibility score
        percentage = min(95, max(65, sum(elements.values()) * 15 + random.randint(-10, 10)))
        
        # Dynamically select the top 3 insights based on the user's strongest elements
        top_elements = sorted(elements.items(), key=lambda x: x[1], reverse=True)[:3]
        top_element_keys = [item[0] for item in top_elements]

        # Map elements to insight-generating functions
        insight_mapping = {
            'L': ("Love Language", self._get_love_language_insight),
            'C': ("Communication Style", self._get_communication_insight),
            'A': ("Adventure Level", self._get_adventure_insight),
            'S': ("Relationship Values", self._get_values_insight),
            'H': ("Sense of Humor", self._get_humor_insight),
            'T': ("Trust Tendency", self._get_trust_insight),
            'P': ("Passion Index", self._get_passion_insight),
            'E': ("Empathy", self._get_communication_insight), # Fallback
            'G': ("Growth", self._get_values_insight) # Fallback
        }

        insights = {}
        for key in top_element_keys:
            if key in insight_mapping:
                title, func = insight_mapping[key]
                if title not in insights: # Avoid duplicate insight types
                    insights[title] = func(answers)

        # If less than 3 insights, fill with defaults
        default_insights_order = ['L', 'C', 'A', 'S', 'H', 'T', 'P']
        idx = 0
        while len(insights) < 3 and idx < len(default_insights_order):
            key = default_insights_order[idx]
            if key in insight_mapping:
                title, func = insight_mapping[key]
                if title not in insights:
                    insights[title] = func(answers)
            idx += 1

        # Always include Relationship Values insight
        if 'Relationship Values' not in insights:
            insights['Relationship Values'] = self._get_values_insight(answers)

        milestones, challenges = self._generate_solo_milestones_challenges(elements)
        personal_trait = self._generate_personal_trait(elements)
        
        return CompatibilityResult(
            percentage=percentage,
            formula=formula,
            elements=elements,
            insights=insights,
            milestones=milestones,
            challenges=challenges,
            personal_trait=personal_trait
        )
    
    def _analyze_couple(self, answers1: Dict, answers2: Dict) -> CompatibilityResult:
        """Analyze couple compatibility"""
        elements1 = self._calculate_elements(answers1)
        elements2 = self._calculate_elements(answers2)
        
        # Calculate compatibility based on answer alignment
        compatibility_score = 0
        total_weight = 0
        
        for question in self.questions:
            if question.id in answers1 and question.id in answers2:
                answer1 = answers1[question.id]
                answer2 = answers2[question.id]
                
                if answer1 == answer2:
                    compatibility_score += question.weight * 20
                else:
                    compatibility_score += question.weight * 8
                
                total_weight += question.weight
        
        percentage = min(99, max(40, (compatibility_score / total_weight) if total_weight > 0 else 70))
        
        # Combine elements for couple formula
        combined_elements = {}
        for element in elements1:
            combined_elements[element] = (elements1[element] + elements2[element]) / 2
        
        formula = self._generate_formula(combined_elements)
        
        # Dynamically select the top 3 insights based on the couple's strongest combined elements
        top_elements = sorted(combined_elements.items(), key=lambda x: x[1], reverse=True)[:3]
        top_element_keys = [item[0] for item in top_elements]

        # Map elements to insight-generating functions
        insight_mapping = {
            'L': ("Love Languages", self._get_couple_love_language_insight),
            'C': ("Communication Match", self._get_couple_communication_insight),
            'A': ("Lifestyle Compatibility", self._get_couple_lifestyle_insight),
            'S': ("Shared Values", self._get_couple_values_insight),
            'H': ("Humor Blend", self._get_couple_humor_insight),
            'T': ("Trust Alignment", self._get_couple_trust_insight),
            'P': ("Passion Synergy", self._get_couple_passion_insight),
            'E': ("Empathy", self._get_couple_communication_insight), # Fallback
            'G': ("Growth", self._get_couple_values_insight) # Fallback
        }

        insights = {}
        for key in top_element_keys:
            if key in insight_mapping:
                title, func = insight_mapping[key]
                if title not in insights: # Avoid duplicate insight types
                    insights[title] = func(answers1, answers2)

        # If less than 3 insights, fill with defaults
        default_insights_order = ['L', 'C', 'A', 'S', 'H', 'T', 'P']
        idx = 0
        while len(insights) < 3 and idx < len(default_insights_order):
            key = default_insights_order[idx]
            if key in insight_mapping:
                title, func = insight_mapping[key]
                if title not in insights:
                    insights[title] = func(answers1, answers2)
            idx += 1

        # Always include Relationship Values insight
        if 'Relationship Values' not in insights:
            insights['Relationship Values'] = self._get_couple_values_insight(answers1, answers2)

        milestones, challenges = self._generate_milestones_challenges(combined_elements)
        personal_trait = self._generate_personal_trait(combined_elements)
        
        return CompatibilityResult(
            percentage=percentage,
            formula=formula,
            elements=combined_elements,
            insights=insights,
            milestones=milestones,
            challenges=challenges,
            personal_trait=personal_trait
        )
    
    def _calculate_elements(self, answers: Dict) -> Dict[str, float]:
        """Calculate relationship elements based on answers"""
        elements = {key: 0.0 for key in self.elements.keys()}
        
        # Map answers to elements
        for question_id, answer in answers.items():
            # Map answers from new questions to elements
            if question_id == "q1":  # Affection
                if "hug" in answer: elements["L"] += 0.4; elements["T"] += 0.3
                elif "kiss" in answer: elements["P"] += 0.5; elements["L"] += 0.2
                elif "snack" in answer: elements["S"] += 0.4; elements["L"] += 0.2
                elif "listening" in answer: elements["C"] += 0.5; elements["E"] += 0.3

            elif question_id == "q2":  # Conflict Approach
                if "Apologize" in answer: elements["C"] += 0.4; elements["R"] += 0.3
                elif "Explain" in answer: elements["C"] += 0.4; elements["G"] += 0.2
                elif "space" in answer: elements["S"] += 0.4; elements["R"] += 0.2
                elif "withdraw" in answer: elements["E"] += 0.4; elements["S"] += 0.1

            elif question_id == "q3":  # Financial Disagreements
                if "tackle it together" in answer: elements["S"] += 0.4; elements["T"] += 0.4
                elif "Stress" in answer: elements["S"] -= 0.2; elements["E"] += 0.2
                elif "Casual" in answer: elements["F"] += 0.4; elements["A"] += 0.2
                elif "research" in answer: elements["G"] += 0.4; elements["S"] += 0.2

            elif question_id == "q4":  # Social Energy
                if "close friends" in answer: elements["F"] += 0.3; elements["C"] += 0.3
                elif "concert or busy bar" in answer: elements["A"] += 0.4; elements["P"] += 0.2
                elif "movie marathon" in answer: elements["L"] += 0.4; elements["S"] += 0.3
                elif "quiet dinner" in answer: elements["C"] += 0.4; elements["L"] += 0.3

            elif question_id == "q5":  # Future Planning
                if "career and financial" in answer: elements["S"] += 0.5; elements["G"] += 0.3
                elif "adventures" in answer: elements["A"] += 0.5; elements["F"] += 0.3
                elif "home life" in answer: elements["S"] += 0.5; elements["L"] += 0.3
                elif "individuals" in answer: elements["G"] += 0.4; elements["R"] += 0.3

            elif question_id == "q6":  # Annoyances (minor impact)
                if "towels" in answer: elements["R"] -= 0.1
                elif "late" in answer: elements["R"] -= 0.1; elements["T"] -= 0.1
                elif "chewing" in answer: elements["R"] -= 0.1
                elif "dishes" in answer: elements["S"] -= 0.1; elements["R"] -= 0.1

            elif question_id == "q7":  # Intimacy
                if "vulnerability" in answer: elements["T"] += 0.5; elements["E"] += 0.4
                elif "physical connection" in answer: elements["P"] += 0.5; elements["L"] += 0.3
                elif "humor" in answer: elements["H"] += 0.5; elements["F"] += 0.3
                elif "safe" in answer: elements["T"] += 0.5; elements["S"] += 0.4

            elif question_id == "q8":  # Support Style
                if "solutions" in answer: elements["S"] += 0.4; elements["G"] += 0.2
                elif "comfort" in answer: elements["L"] += 0.4; elements["E"] += 0.4
                elif "Listen" in answer: elements["C"] += 0.5; elements["E"] += 0.4
                elif "Distract" in answer: elements["F"] += 0.4; elements["H"] += 0.3
        
        return elements
    
    def _generate_formula(self, elements: Dict[str, float]) -> str:
        """Generate relationship chemical formula"""
        # Get top 3 elements
        sorted_elements = sorted(elements.items(), key=lambda x: x[1], reverse=True)[:3]
        
        formula_parts = []
        for element, value in sorted_elements:
            if value > 0.1:
                subscript = max(1, int(value * 8))
                formula_parts.append(f"{element}{subscript if subscript > 1 else ''}")
        
        return "".join(formula_parts) if formula_parts else "H2O"
    
    def _get_love_language_insight(self, answers: Dict) -> str:
        """Get love language insight for individual"""
        q3_answer = answers.get("q3", "")
        if "Quality time" in q3_answer:
            return "You value presence and undivided attention in relationships."
        elif "Physical" in q3_answer:
            return "Physical touch and closeness are essential for your emotional connection."
        elif "Words" in q3_answer:
            return "You thrive on verbal appreciation and emotional expression."
        else:
            return "You feel loved through thoughtful actions and gestures."
    
    def _get_communication_insight(self, answers: Dict) -> str:
        """Get communication insight for individual"""
        q2_answer = answers.get("q2", "")
        if "Talk it out" in q2_answer:
            return "You prefer direct, immediate communication to resolve conflicts."
        elif "cool down" in q2_answer:
            return "You value thoughtful reflection before addressing disagreements."
        elif "humor" in q2_answer:
            return "You use humor as a bridge to navigate relationship challenges."
        else:
            return "You process emotions through writing and structured thinking."
    
    def _get_adventure_insight(self, answers: Dict) -> str:
        """Get adventure insight for individual"""
        q4_answer = answers.get("q4", "")
        if "Backpacking" in q4_answer:
            return "You crave authentic, adventurous experiences with your partner."
        elif "Luxury" in q4_answer:
            return "You appreciate comfort and luxury in your romantic getaways."
        elif "Road trip" in q4_answer:
            return "You love spontaneous adventures and discovering new places together."
        else:
            return "You're drawn to cultural experiences and meaningful exploration."
    
    def _get_values_insight(self, answers: Dict) -> str:
        """Get values insight for individual"""
        q5_answer = answers.get("q5", "")
        if "future" in q5_answer:
            return "Building a stable, long-term partnership is your primary focus."
        elif "chemistry" in q5_answer:
            return "Passion and romantic connection drive your relationship priorities."
        elif "friends" in q5_answer:
            return "Friendship and companionship form the foundation of your ideal relationship."
        else:
            return "You value personal growth and individual development within the relationship above all else."

    # ---------- New insight helpers ----------
    def _get_humor_insight(self, answers: Dict) -> str:
        """Sense of humor insight"""
        q2_answer = answers.get("q2", "")
        if "humor" in q2_answer:
            return "You naturally defuse tension with laughter and playfulness."
        else:
            return "You prefer a more straightforward approach to conflict, sprinkling humor occasionally."

    def _get_trust_insight(self, answers: Dict) -> str:
        """Trust tendency insight"""
        q5_answer = answers.get("q5", "")
        if "future" in q5_answer or "friends" in q5_answer:
            return "You place high importance on reliability and mutual trust."
        else:
            return "You build trust gradually, valuing openness and growth."

    def _generate_personal_trait(self, elements: Dict[str, float]) -> str:
        """Generate a high-level personal relationship trait based on strongest element"""
        top_element = max(elements.items(), key=lambda x: x[1])[0]
        trait_mapping = {
            'S': "Rock-solid steady partner",
            'G': "Curious self-improver",
            'T': "Reliably transparent soul",
            'L': "Warm-hearted romantic",
            'C': "Thoughtful communicator",
            'E': "Compassionate listener",
            'A': "Adventure-seeking spirit",
            'P': "Passion igniter",
            'H': "Playful humorist",
            'R': "Respectful collaborator",
            'F': "Fun-loving companion"
        }
        return trait_mapping.get(top_element, "Adaptable partner")

    def _get_passion_insight(self, answers: Dict) -> str:
        """Determine user's passion inclination from lifestyle and values answers"""
        q1_answer = answers.get("q1", "").lower()
        q5_answer = answers.get("q5", "").lower()

        # High-energy passion cues
        if "dancing" in q1_answer or "chemistry" in q5_answer:
            return "You thrive on high-energy, spontaneous passion in your relationship."

        # Warm steady passion cues
        if "cooking" in q1_answer or "future" in q5_answer:
            return "Your passion burns steadily, focused on building a lasting bond."

        # Exploratory passion cues
        if "exploring" in q1_answer or "individuals" in q5_answer:
            return "You express passion through shared growth and new adventures."

        return "Your passion reveals itself in the small, meaningful moments you create together."

    # ---------- Milestones & Challenges ----------
    def _generate_solo_milestones_challenges(self, elements: Dict[str, float]):
        """Solo milestones/challenges (no partner yet)"""
        top = sorted(elements.items(), key=lambda x: x[1], reverse=True)[:3]
        import hashlib, random
        seed = int(hashlib.sha256(str(elements).encode()).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)
        milestones=[]; challenges=[]
        variants = {
            'P': [
                ("You’ll be the partner who keeps passion burning through creative surprises", "Sketch a list of future \"spark dates\" to bring that creativity into a relationship"),
                ("Your energy turns everyday moments into passionate memories", "Draft a surprise-note idea bank for a future partner")
            ],
            'L': [
                ("You’ll nurture your partner with steady acts of care and affirmation", "Practice articulating affirmations so they flow naturally later"),
                ("Love will be your super-power, expressed through small daily gestures", "List five thoughtful habits you’d share with someone")
            ],
            'C': [
                ("Your knack for heartfelt messages will become a keepsake in your future relationship", "Start a private note where you capture little moments you’d love to share someday"),
                ("Deep conversations will be your relationship glue", "Keep a conversation-starter journal for future date nights")
            ],
            'T': [
                ("Trust will be your relationship cornerstone—know and live your values", "Practice vulnerability now so openness feels natural with a partner"),
                ("You’ll model honesty and reliability", "Share a truthful story about yourself with someone you trust")
            ],
            'A': [
                ("You’ll infuse the relationship with adventurous energy and fresh experiences", "Brainstorm bucket-list trips you’d love to share"),
                ("Exploration will be your love language", "Plan a micro-adventure you could invite a partner on")
            ],
            'G': [
                ("Your growth mindset will inspire your partner to evolve alongside you", "Curate growth resources you’d enjoy exploring together"),
                ("Your commitment to growth will naturally inspire the person you end up with", "Sketch a simple vision board of what thriving together could look like")
            ]
        }
        for k,_ in top:
            if k in variants:
                m,c = rng.choice(variants[k])
                milestones.append(m)
                challenges.append(c)
            elif k=='L':
                milestones.append("You’ll nurture your partner with steady acts of care and affirmation")
                challenges.append("Practice articulating those affirmations so they flow naturally later")
            elif k=='C':
                milestones.append("Your future partner will appreciate your thoughtful written reflections")
                challenges.append("Hone that skill by journaling feelings you’d someday share with them")
            elif k=='T':
                milestones.append("Trust will be your relationship cornerstone—know and live your values")
                challenges.append("Practice vulnerability now so openness feels natural with a partner")
            elif k=='A':
                milestones.append("You’ll infuse the relationship with adventurous energy and fresh experiences")
                challenges.append("Brainstorm future shared adventures and note what excites you most")
            elif k=='G':
                milestones.append("Your growth mindset will inspire your partner to evolve alongside you")
                challenges.append("Curate growth resources you’d enjoy exploring together later")
        return milestones[:3], challenges[:3]

    def _generate_milestones_challenges(self, elements: Dict[str, float]):
        """Generate three milestones and challenges based on dominant elements"""
        top = sorted(elements.items(), key=lambda x: x[1], reverse=True)[:3]
        keys = [k for k,_ in top]
        milestones = []
        challenges = []
        for k in keys:
            if k == 'G':
                milestones.append("Set an individual growth goal and share progress monthly")
                challenges.append("Read a personal-development book together and discuss")
            elif k == 'A':
                milestones.append("Plan a new adventure weekend every quarter")
                challenges.append("Do something spontaneous this month that scares you both a little")
            elif k == 'T':
                milestones.append("Schedule a trust-building check-in night each week")
                challenges.append("Share one vulnerability you've never discussed before")
            elif k == 'C':
                milestones.append("Create a communication ritual (e.g., Sunday reflections)")
                challenges.append("Practice active-listening drills for 5 minutes daily")
            elif k == 'P':
                milestones.append("Design a monthly date that fuels passion and excitement")
                challenges.append("Try a new intimacy activity together this week")
            elif k == 'L':
                milestones.append("Identify and honor each other's primary love language every day")
                challenges.append("Plan a 'love-language swap' day to step into each other's shoes")
            elif k == 'S':
                milestones.append("Draft a shared long-term stability plan (finances, home, etc.)")
                challenges.append("Do a budget review and align on priorities")
            elif k == 'H':
                milestones.append("Create a shared humor scrapbook of inside jokes")
                challenges.append("Have a nightly laughter session—tell or find a joke together")
            elif k == 'F':
                milestones.append("Schedule regular fun days with zero serious agenda")
                challenges.append("Try a playful hobby you've never done before")
            elif k == 'E':
                milestones.append("Practice weekly empathy reflection—how did we support each other?")
                challenges.append("Role-play each other's perspective in a past conflict")
            elif k == 'R':
                milestones.append("Define and agree on core relationship boundaries and respect rules")
                challenges.append("Notice and appreciate 3 respectful actions daily")
        # ensure max 3
        return milestones[:3], challenges[:3]

    # ---------- Couple insight helpers ----------
    def _compare_answers(self, a1: str, a2: str) -> str:
        """Utility to categorize answer similarity"""
        if a1 == a2:
            return "match"
        return "different"

    def _get_couple_love_language_insight(self, ans1: Dict, ans2: Dict) -> str:
        comp = self._compare_answers(ans1.get("q1", ""), ans2.get("q1", ""))
        if comp == "match":
            return "You both show affection in similar ways—easy to make each other feel loved."
        return "Your affection styles differ; see this as an opportunity to learn each other's love languages."

    def _get_couple_communication_insight(self, ans1: Dict, ans2: Dict) -> str:
        comp = self._compare_answers(ans1.get("q2", ""), ans2.get("q2", ""))
        if comp == "match":
            return "You tackle conflicts with a shared communication approach, reducing misunderstandings."
        return "Different conflict styles—set ground rules so each feels heard."

    def _get_couple_lifestyle_insight(self, ans1: Dict, ans2: Dict) -> str:
        comp = self._compare_answers(ans1.get("q4", ""), ans2.get("q4", ""))
        if comp == "match":
            return "Your weekend energy aligns—planning dates will be effortless."
        return "You recharge differently on weekends; balance cozy nights with outings so both feel satisfied."

    def _get_couple_values_insight(self, ans1: Dict, ans2: Dict) -> str:
        comp = self._compare_answers(ans1.get("q5", ""), ans2.get("q5", ""))
        if comp == "match":
            return "Shared long-term priorities give your relationship strong direction."
        return "Different future focuses—use them to complement and support each other's dreams."

    def _get_couple_humor_insight(self, ans1: Dict, ans2: Dict) -> str:
        if "humor" in ans1.get("q7", "").lower() and "humor" in ans2.get("q7", "").lower():
            return "Laughter is a mutual love language—you'll keep things light even in tough times."
        elif "humor" in ans1.get("q7", "").lower() or "humor" in ans2.get("q7", "").lower():
            return "One partner brings the jokes—lean into that playfulness together."
        return "Neither of you relies heavily on humor, so be intentional about keeping joy alive."

    def _get_couple_trust_insight(self, ans1: Dict, ans2: Dict) -> str:
        if "vulnerability" in ans1.get("q7", "").lower() and "vulnerability" in ans2.get("q7", "").lower():
            return "Mutual emotional openness creates a deep trust foundation."
        return "Build trust by recognizing each other's comfort zones for sharing feelings."

    def _get_couple_passion_insight(self, ans1: Dict, ans2: Dict) -> str:
        if "kiss" in ans1.get("q1", "").lower() or "kiss" in ans2.get("q1", "").lower():
            return "High physical passion detected—keep nurturing that spark!"
        return "Your passion shows in subtle ways; focus on emotional and intellectual intimacy too."

def _inject_mobile_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Audiowide&display=swap');
    html, body {background: linear-gradient(180deg,#0f0f23 0%, #1a1a3c 100%); color:#ffffff; font-family:'Poppins',sans-serif; overflow-x:hidden; margin:0; padding:0;}
    .lab-container{width:92%;max-width:420px;margin:0 auto;}
    .lab-container:empty{display:none;}
    .logo-text{font-family:'Audiowide', cursive; font-size:2.2rem; letter-spacing:1px; margin:8px 0 4px; display:flex; align-items:center; gap:6px;}
    .neon-text{font-weight:700;text-shadow:0 0 4px #00ffff,0 0 12px #00ffff; margin:0;}
    .stButton>button{background:#744bff;border:none;border-radius:12px;padding:12px 20px;color:#fff;font-weight:600;box-shadow:0 4px 10px rgba(0,0,0,0.3);} 
    .stButton>button:hover{background:#8d63ff}
    .stRadio>div{background:#6b5ba4;border-radius:14px;padding:8px 12px;box-shadow:inset 0 0 8px rgba(0,0,0,0.4);} 
    .stRadio>div label{color:#fff;font-size:0.9em;}
    .stRadio>div:hover{background:#7a6bc0}
    iframe{max-width:100%;}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def main():
    _inject_mobile_css()
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="logo-text">🧪ChemistryLab</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #00ffff;">Discover Your Love Compatibility</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'lab' not in st.session_state:
        st.session_state.lab = ChemistryLab()
    
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    
    if 'answers1' not in st.session_state:
        st.session_state.answers1 = {}
    
    if 'answers2' not in st.session_state:
        st.session_state.answers2 = {}
    
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    # Mode selection
    if st.session_state.mode is None:
        st.markdown('<div class="lab-container">', unsafe_allow_html=True)
        st.markdown('<h4 class="neon-text">Choose Your Experiment</h4>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔬 Solo Analysis", use_container_width=True):
                st.session_state.mode = "solo"
                st.rerun()
        
        with col2:
            if st.button("💕 Couple Chemistry", use_container_width=True):
                st.session_state.mode = "couple"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Show questions or results
    if st.session_state.results is None:
        show_questions()
    else:
        show_results()

def show_questions():
    """Display questions with lab theme"""
    lab = st.session_state.lab
    questions = lab.questions
    current_q = st.session_state.current_question
    
    if current_q >= len(questions):
        # All questions answered, calculate results
        if st.session_state.mode == "solo":
            st.session_state.results = lab.calculate_compatibility(st.session_state.answers1)
        else:
            st.session_state.results = lab.calculate_compatibility(st.session_state.answers1, st.session_state.answers2)
        st.rerun()
        return
    
    question = questions[current_q]
    
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    
    # Progress bar
    progress = (current_q + 1) / len(questions)
    st.progress(progress)
    st.markdown(f'<p style="color: #00ffff;">Question {current_q + 1} of {len(questions)}</p>', unsafe_allow_html=True)
    
    # Question
    st.markdown(f'<h4 class="neon-text">{question.text}</h4>', unsafe_allow_html=True)
    
    # Handle couple mode - show both partners
    if st.session_state.mode == "couple":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h5 style="color: #ff6b6b;">Partner 1</h5>', unsafe_allow_html=True)
            answer1 = st.radio(
                "Choose your answer:",
                question.options,
                key=f"q{current_q}_p1",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown('<h5 style="color: #4ecdc4;">Partner 2</h5>', unsafe_allow_html=True)
            answer2 = st.radio(
                "Choose your answer:",
                question.options,
                key=f"q{current_q}_p2",
                label_visibility="collapsed"
            )
        
        if st.button("Next Question ➡️", use_container_width=True):
            st.session_state.answers1[question.id] = answer1
            st.session_state.answers2[question.id] = answer2
            st.session_state.current_question += 1
            st.rerun()
    
    else:
        # Solo mode
        answer = st.radio(
            "Choose your answer:",
            question.options,
            key=f"q{current_q}_solo",
            label_visibility="collapsed"
        )
        
        if st.button("Next Question ➡️", use_container_width=True):
            st.session_state.answers1[question.id] = answer
            st.session_state.current_question += 1
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_results():
    """Display compatibility results with lab report theme"""
    results = st.session_state.results
    
    # Header
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="neon-text">🧪 Lab Results</h2>', unsafe_allow_html=True)
    
    # Compatibility Score
    st.markdown(f'<h1 style="color: #00ff00; text-align: center; font-size: 3em;">{results.percentage:.0f}%</h1>', unsafe_allow_html=True)
    st.markdown(f'<h4 style="color: #00ffff; text-align: center;">Compatibility Formula: {results.formula}</h4>', unsafe_allow_html=True)
    
    # Visual meter
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = results.percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Compatibility Level"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#00ffff"},
            'steps': [
                {'range': [0, 50], 'color': "#ff4444"},
                {'range': [50, 75], 'color': "#ffaa00"},
                {'range': [75, 100], 'color': "#00ff00"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Final dynamic summary based on top elements
    top3 = sorted(results.elements.items(), key=lambda x: x[1], reverse=True)[:3]
    if top3:
        lab_instance = st.session_state.lab
        descriptors = [lab_instance.elements.get(code, code) for code, _ in top3]
        import random, hashlib
        seed = int(hashlib.sha256(str(descriptors).encode()).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)
        if len(descriptors) == 1:
            templates_one = [
                "At your heart, you lead with {d1} in every connection you nurture.",
                "Your signature relationship vibe? Pure {d1}.",
                "You naturally radiate {d1}, and partners feel it instantly."
            ]
            summary_sentence = templates_one[rng.randrange(len(templates_one))].format(d1=descriptors[0].lower())
        elif len(descriptors) == 2:
            templates_two = [
                "You're craving a partnership that dances between {d1} and {d2}—and you make it look effortless.",
                "Expect a beautiful tug-of-war where {d1} meets {d2} in perfect sync.",
                "Your best bond blends your love of {d1} with a flair for {d2}."
            ]
            summary_sentence = templates_two[rng.randrange(len(templates_two))].format(d1=descriptors[0].lower(), d2=descriptors[1].lower())
        else:
            templates_three = [
                "Your ideal chemistry mixes {d1}, {d2}, and a splash of {d3}—shaken, not stirred.",
                "Picture a tri-beam where {d1}, {d2}, and {d3} light up every moment you share.",
                "You've got a secret recipe: equal parts {d1}, {d2}, and {d3}. Yum!"
            ]
            summary_sentence = templates_three[rng.randrange(len(templates_three))].format(d1=descriptors[0].lower(), d2=descriptors[1].lower(), d3=descriptors[2].lower())
        st.markdown(
            f"<p style='color:#00ffff; font-size:1.2em; text-align:center;'>{summary_sentence}</p>",
            unsafe_allow_html=True,
        )

    # Elements breakdown
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="neon-text">🔬 Chemical Elements</h4>', unsafe_allow_html=True)
    
    # Show top elements as molecules
    sorted_elements = sorted(results.elements.items(), key=lambda x: x[1], reverse=True)[:6]
    
    cols = st.columns(3)
    for i, (element, value) in enumerate(sorted_elements):
        with cols[i % 3]:
            element_name = st.session_state.lab.elements[element]
            st.markdown(f'<div class="molecule">{element} - {element_name}<br>{value:.1f}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Personal Trait
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="neon-text">💖 Personal Relationship Trait</h4>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-card">{results.personal_trait}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="neon-text">💡 Lab Analysis</h4>', unsafe_allow_html=True)
    
    for category, insight in results.insights.items():
        st.markdown(f'<div class="result-card"><strong>{category}:</strong> {insight}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Milestones
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="neon-text">🎯 Relationship Milestones</h4>', unsafe_allow_html=True)
    
    for i, milestone in enumerate(results.milestones, 1):
        st.markdown(f'<div class="result-card">{i}. {milestone}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Challenges
    st.markdown('<div class="lab-container">', unsafe_allow_html=True)
    st.markdown('<h4 class="neon-text">⚡ Growth Challenges</h4>', unsafe_allow_html=True)
    
    for i, challenge in enumerate(results.challenges, 1):
        st.markdown(f'<div class="result-card">{i}. {challenge}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Restart button
    if st.button("🔄 New Experiment", use_container_width=True):
        # Reset all session state
        for key in list(st.session_state.keys()):
            if key != 'lab':
                del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()
