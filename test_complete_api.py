import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import ChemistryLab

def test_complete_ai_integration():
    """Test all AI functions including new milestones and challenges"""
    print("🧪 Testing Complete Chemistry Lab AI Integration...")
    
    # Initialize the lab
    lab = ChemistryLab()
    
    # Sample answers for testing
    test_answers = {
        'q1': 'Netflix and deep conversations',
        'q2': 'Listen and provide comfort',
        'q3': 'Poor communication',
        'q4': 'Personal growth',
        'q5': 'Planning quality time together'
    }
    
    print("\n1. Testing AI Insights...")
    try:
        insights = lab.get_ai_insights(test_answers)
        print(f"✅ AI Insights: {insights}")
    except Exception as e:
        print(f"❌ AI Insights Error: {e}")
    
    print("\n2. Testing AI Milestones...")
    try:
        milestones = lab.get_ai_milestones(test_answers)
        print(f"✅ AI Milestones: {milestones}")
    except Exception as e:
        print(f"❌ AI Milestones Error: {e}")
    
    print("\n3. Testing AI Challenges...")
    try:
        challenges = lab.get_ai_challenges(test_answers)
        print(f"✅ AI Challenges: {challenges}")
    except Exception as e:
        print(f"❌ AI Challenges Error: {e}")
    
    print("\n4. Testing AI Tip...")
    try:
        tip = lab.get_ai_relationship_tip(test_answers)
        print(f"✅ AI Tip: {tip}")
    except Exception as e:
        print(f"❌ AI Tip Error: {e}")
    
    print("\n🎉 Complete AI integration test finished!")

if __name__ == "__main__":
    test_complete_ai_integration()
