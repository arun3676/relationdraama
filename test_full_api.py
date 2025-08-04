import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import ChemistryLab

def test_all_api_functions():
    """Test all AI-powered functions in the Chemistry Lab"""
    print("🧪 Testing Chemistry Lab AI Integration...")
    
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
    
    test_answers2 = {
        'q1': 'Exploring a new part of the city',
        'q2': 'Offer practical solutions',
        'q3': 'Different life goals',
        'q4': 'Adventure and travel',
        'q5': 'Spontaneous hugs and kisses'
    }
    
    print("\n1. Testing AI Feedback (Solo)...")
    try:
        feedback_solo = lab.get_ai_feedback(test_answers)
        print(f"✅ Solo Feedback: {feedback_solo}")
    except Exception as e:
        print(f"❌ Solo Feedback Error: {e}")
    
    print("\n2. Testing AI Feedback (Couple)...")
    try:
        feedback_couple = lab.get_ai_feedback(test_answers, test_answers2, 75.5)
        print(f"✅ Couple Feedback: {feedback_couple}")
    except Exception as e:
        print(f"❌ Couple Feedback Error: {e}")
    
    print("\n3. Testing AI Insights (Solo)...")
    try:
        insights_solo = lab.get_ai_insights(test_answers)
        print(f"✅ Solo Insights: {insights_solo}")
    except Exception as e:
        print(f"❌ Solo Insights Error: {e}")
    
    print("\n4. Testing AI Insights (Couple)...")
    try:
        insights_couple = lab.get_ai_insights(test_answers, test_answers2)
        print(f"✅ Couple Insights: {insights_couple}")
    except Exception as e:
        print(f"❌ Couple Insights Error: {e}")
    
    print("\n5. Testing AI Relationship Tip (Solo)...")
    try:
        tip_solo = lab.get_ai_relationship_tip(test_answers)
        print(f"✅ Solo Tip: {tip_solo}")
    except Exception as e:
        print(f"❌ Solo Tip Error: {e}")
    
    print("\n6. Testing AI Relationship Tip (Couple)...")
    try:
        tip_couple = lab.get_ai_relationship_tip(test_answers, test_answers2, 75.5)
        print(f"✅ Couple Tip: {tip_couple}")
    except Exception as e:
        print(f"❌ Couple Tip Error: {e}")
    
    print("\n🎉 All API tests completed!")

if __name__ == "__main__":
    test_all_api_functions()
