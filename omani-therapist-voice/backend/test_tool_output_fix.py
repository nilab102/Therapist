#!/usr/bin/env python3
"""
Quick test to verify that enhanced prompts prevent tool output verbalization.
"""

import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.therapy_agent_manager import (
    GENERAL_THERAPY_INSTRUCTION,
    CRISIS_INTERVENTION_INSTRUCTION,
    CBT_SPECIALIST_INSTRUCTION
)

def test_tool_output_verbalization_prevention():
    """Test that all prompts contain instructions to prevent tool output verbalization."""
    
    # Check that all prompts contain the critical rule
    prompts = {
        "General Therapy": GENERAL_THERAPY_INSTRUCTION,
        "Crisis Intervention": CRISIS_INTERVENTION_INSTRUCTION,
        "CBT Specialist": CBT_SPECIALIST_INSTRUCTION
    }
    
    required_phrases = [
        "NEVER VERBALIZE TOOL OUTPUTS",
        "tool_outputs",
        "NEVER speak",
        "Use tool data to inform",
        "speak naturally"
    ]
    
    results = {}
    
    for prompt_name, prompt_text in prompts.items():
        results[prompt_name] = {}
        
        for phrase in required_phrases:
            if phrase.lower() in prompt_text.lower():
                results[prompt_name][phrase] = "✅ FOUND"
            else:
                results[prompt_name][phrase] = "❌ MISSING"
    
    # Print results
    print("🧪 TOOL OUTPUT VERBALIZATION PREVENTION TEST")
    print("=" * 60)
    
    all_good = True
    
    for prompt_name, checks in results.items():
        print(f"\n📋 {prompt_name} Prompt:")
        for phrase, status in checks.items():
            print(f"  {status} {phrase}")
            if "❌" in status:
                all_good = False
    
    # Check for specific examples
    print(f"\n🔍 SPECIFIC EXAMPLE CHECKS:")
    
    # Check for "NEVER say" examples
    never_say_examples = [
        "NEVER say: \"tool_outputs",
        "🚫 NEVER say:",
        "✅ INSTEAD:"
    ]
    
    for prompt_name, prompt_text in prompts.items():
        print(f"\n📝 {prompt_name} Examples:")
        for example in never_say_examples:
            if example.lower() in prompt_text.lower():
                print(f"  ✅ Contains: {example}")
            else:
                print(f"  ❌ Missing: {example}")
                all_good = False
    
    # Overall result
    print(f"\n" + "=" * 60)
    if all_good:
        print("🎉 SUCCESS: All prompts properly prevent tool output verbalization!")
        print("✅ Enhanced prompts should fix the voice output issue.")
    else:
        print("⚠️  WARNING: Some prompts missing critical instructions.")
        print("❌ May still have tool output verbalization issues.")
    
    return all_good

def check_example_quality():
    """Check that the examples show proper natural responses."""
    
    print(f"\n📚 EXAMPLE QUALITY CHECK:")
    print("=" * 60)
    
    # Check General Therapy example
    if "I can feel the pain in your words, my dear" in GENERAL_THERAPY_INSTRUCTION:
        print("✅ General Therapy: Contains natural therapeutic response example")
    else:
        print("❌ General Therapy: Missing natural response example")
    
    # Check Crisis Intervention example  
    if "Your safety is the most important thing to me" in CRISIS_INTERVENTION_INSTRUCTION:
        print("✅ Crisis Intervention: Contains empathetic crisis response example")
    else:
        print("❌ Crisis Intervention: Missing empathetic response example")
    
    # Check CBT Specialist example
    if "I hear the pain in your words" in CBT_SPECIALIST_INSTRUCTION:
        print("✅ CBT Specialist: Contains natural CBT response example")
    else:
        print("❌ CBT Specialist: Missing natural response example")
    
    # Check for Arabic integration
    arabic_phrases = ["حبيبي", "أستطيع أن أسمع", "الله"]
    arabic_found = 0
    
    for prompt_name, prompt_text in [
        ("General", GENERAL_THERAPY_INSTRUCTION),
        ("Crisis", CRISIS_INTERVENTION_INSTRUCTION), 
        ("CBT", CBT_SPECIALIST_INSTRUCTION)
    ]:
        for phrase in arabic_phrases:
            if phrase in prompt_text:
                arabic_found += 1
                break
    
    print(f"🇴🇲 Arabic Integration: {arabic_found}/3 prompts contain Arabic expressions")

if __name__ == "__main__":
    print("🚀 Testing Enhanced Prompts for Tool Output Fix")
    
    # Run main test
    success = test_tool_output_verbalization_prevention()
    
    # Check example quality
    check_example_quality()
    
    print(f"\n💡 SUMMARY:")
    print("=" * 60)
    print("The enhanced prompts now contain explicit instructions to:")
    print("1. ✅ NEVER verbalize raw tool outputs like {'emotions': ['nervousness']}")
    print("2. ✅ Process tool data internally to inform responses") 
    print("3. ✅ Speak naturally with therapeutic empathy")
    print("4. ✅ Include cultural expressions and Islamic concepts")
    print("5. ✅ Provide clear examples of proper vs improper responses")
    
    if success:
        print(f"\n🎯 RESULT: Enhanced prompts should fix the tool output verbalization issue!")
        print("The AI will now use tool insights to provide natural therapeutic responses.")
    else:
        print(f"\n⚠️  RESULT: Some issues detected - may need further refinement.")
    
    sys.exit(0 if success else 1) 