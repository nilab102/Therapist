#!/usr/bin/env python3
"""
Enhanced Prompt Testing Framework for OMANI Therapist Voice
Tests to verify that the enhanced prompts force systematic tool usage.
"""

import asyncio
import sys
import os
from typing import Dict, List, Any
from unittest.mock import Mock, AsyncMock
import json

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.therapy_agent_manager import (
    TherapyAgentManager,
    GENERAL_THERAPY_INSTRUCTION,
    CRISIS_INTERVENTION_INSTRUCTION,
    CBT_SPECIALIST_INSTRUCTION
)

class MockTool:
    """Mock tool for testing function calls."""
    
    def __init__(self, name: str):
        self.name = name
        self.calls = []
        
    async def execute(self, action: str, **kwargs) -> str:
        call_record = {
            "action": action,
            "arguments": kwargs,
            "timestamp": asyncio.get_event_loop().time()
        }
        self.calls.append(call_record)
        return f"Mock {self.name} executed: {action} with {kwargs}"
    
    def get_tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": f"Mock {self.name} tool for testing"
            }
        }
    
    def reset_calls(self):
        """Reset call history for new test."""
        self.calls = []

class EnhancedPromptTester:
    """Test framework for enhanced therapeutic prompts."""
    
    def __init__(self):
        self.therapy_manager = TherapyAgentManager()
        self.mock_tools = {}
        self.test_results = []
        
    async def setup_mock_tools(self):
        """Set up mock tools for testing."""
        self.mock_tools = {
            "crisis_detection": MockTool("crisis_detection"),
            "cbt_techniques": MockTool("cbt_techniques"),
            "emotional_analysis": MockTool("emotional_analysis"),
            "session_management": MockTool("session_management")
        }
        
        # Register agents with mock tools
        self.therapy_manager.register_agent(
            "general_therapy",
            GENERAL_THERAPY_INSTRUCTION,
            [tool.get_tool_definition() for tool in self.mock_tools.values()],
            self.mock_tools
        )
        
        self.therapy_manager.register_agent(
            "crisis_intervention",
            CRISIS_INTERVENTION_INSTRUCTION,
            [self.mock_tools["crisis_detection"].get_tool_definition()],
            {"crisis_detection": self.mock_tools["crisis_detection"]}
        )
        
        self.therapy_manager.register_agent(
            "cbt_specialist",
            CBT_SPECIALIST_INSTRUCTION,
            [self.mock_tools["cbt_techniques"].get_tool_definition()],
            {"cbt_techniques": self.mock_tools["cbt_techniques"]}
        )
    
    def reset_tools(self):
        """Reset all mock tools for new test."""
        for tool in self.mock_tools.values():
            tool.reset_calls()
    
    async def simulate_function_call(self, function_name: str, arguments: Dict[str, Any]):
        """Simulate a function call from the LLM."""
        class MockFunctionCall:
            def __init__(self, name, args):
                self.name = name
                self.arguments = args
        
        mock_call = MockFunctionCall(function_name, arguments)
        return await self.therapy_manager.handle_function_call(mock_call)
    
    def verify_tool_called(self, tool_name: str, expected_action: str = None) -> bool:
        """Verify that a specific tool was called with expected action."""
        if tool_name not in self.mock_tools:
            return False
        
        calls = self.mock_tools[tool_name].calls
        if not calls:
            return False
        
        if expected_action:
            return any(call["action"] == expected_action for call in calls)
        
        return len(calls) > 0
    
    def get_tool_calls(self, tool_name: str) -> List[Dict[str, Any]]:
        """Get all calls made to a specific tool."""
        if tool_name not in self.mock_tools:
            return []
        return self.mock_tools[tool_name].calls
    
    async def run_test_scenario(self, scenario_name: str, test_func, expected_tools: List[str]) -> Dict[str, Any]:
        """Run a test scenario and validate results."""
        print(f"\n🧪 Testing: {scenario_name}")
        
        # Reset tools before test
        self.reset_tools()
        
        # Run the test
        try:
            await test_func()
            
            # Verify expected tools were called
            results = {
                "scenario": scenario_name,
                "status": "PASS",
                "expected_tools": expected_tools,
                "called_tools": [],
                "errors": []
            }
            
            for tool_name in expected_tools:
                if self.verify_tool_called(tool_name):
                    results["called_tools"].append(tool_name)
                    print(f"  ✅ {tool_name} was called correctly")
                else:
                    results["status"] = "FAIL"
                    results["errors"].append(f"{tool_name} was not called")
                    print(f"  ❌ {tool_name} was NOT called")
            
            # Show all tool calls for debugging
            for tool_name, tool in self.mock_tools.items():
                if tool.calls:
                    print(f"  📋 {tool_name} calls: {len(tool.calls)}")
                    for call in tool.calls:
                        print(f"    - {call['action']} with {call['arguments']}")
            
            return results
            
        except Exception as e:
            return {
                "scenario": scenario_name,
                "status": "ERROR",
                "expected_tools": expected_tools,
                "called_tools": [],
                "errors": [str(e)]
            }
    
    # ===== CRISIS DETECTION TESTS =====
    
    async def test_crisis_suicide_ideation(self):
        """Test crisis detection for suicide ideation triggers."""
        crisis_statements = [
            ("detect_crisis", {"action": "assess_risk", "user_input": "I want to kill myself"}),
            ("detect_crisis", {"action": "assess_risk", "user_input": "أريد أن أقتل نفسي"}),
            ("detect_crisis", {"action": "assess_risk", "user_input": "I want to end it all"}),
            ("detect_crisis", {"action": "assess_risk", "user_input": "There's no point in living"})
        ]
        
        for func_name, args in crisis_statements:
            await self.simulate_function_call(func_name, args)
    
    async def test_crisis_self_harm(self):
        """Test crisis detection for self-harm triggers."""
        await self.simulate_function_call("detect_crisis", {
            "action": "assess_risk", 
            "user_input": "I want to hurt myself"
        })
        await self.simulate_function_call("detect_crisis", {
            "action": "provide_immediate_support",
            "user_input": "أريد أن أذي نفسي"
        })
    
    async def test_crisis_emergency_escalation(self):
        """Test crisis escalation for imminent danger."""
        await self.simulate_function_call("detect_crisis", {
            "action": "escalate_emergency",
            "user_input": "I'm going to kill myself now"
        })
        await self.simulate_function_call("detect_crisis", {
            "action": "create_safety_plan",
            "user_input": "I have the method ready"
        })
    
    # ===== CBT TECHNIQUE TESTS =====
    
    async def test_cbt_negative_thoughts(self):
        """Test CBT technique calls for negative thought patterns."""
        thought_patterns = [
            ("apply_cbt_technique", {"technique": "thought_challenging", "thought": "I'm worthless"}),
            ("apply_cbt_technique", {"technique": "thought_challenging", "thought": "أنا فاشل"}),
            ("apply_cbt_technique", {"technique": "cognitive_restructuring", "thought": "I always fail"}),
            ("apply_cbt_technique", {"technique": "thought_challenging", "thought": "Nothing ever goes right"})
        ]
        
        for func_name, args in thought_patterns:
            await self.simulate_function_call(func_name, args)
    
    async def test_cbt_behavioral_activation(self):
        """Test CBT behavioral activation for withdrawal patterns."""
        await self.simulate_function_call("apply_cbt_technique", {
            "technique": "behavioral_activation",
            "issue": "I don't want to see anyone"
        })
        await self.simulate_function_call("apply_cbt_technique", {
            "technique": "behavioral_activation", 
            "issue": "ما أريد أسوي شيء"
        })
    
    async def test_cbt_islamic_integration(self):
        """Test Islamic CBT integration for faith-based concerns."""
        await self.simulate_function_call("apply_cbt_technique", {
            "technique": "islamic_cbt_integration",
            "religious_concern": "I'm a bad Muslim"
        })
        await self.simulate_function_call("apply_cbt_technique", {
            "technique": "islamic_cbt_integration",
            "religious_concern": "Why did Allah let this happen?"
        })
    
    # ===== EMOTIONAL ANALYSIS TESTS =====
    
    async def test_emotional_detection(self):
        """Test emotional analysis for various emotional expressions."""
        emotions = [
            ("analyze_emotion", {"analysis_type": "detect_emotions", "emotion": "I feel so sad"}),
            ("analyze_emotion", {"analysis_type": "detect_emotions", "emotion": "أنا حزين جداً"}),
            ("analyze_emotion", {"analysis_type": "detect_emotions", "emotion": "I'm really anxious"}),
            ("analyze_emotion", {"analysis_type": "emotional_intensity_assessment", "emotion": "I'm terrified"})
        ]
        
        for func_name, args in emotions:
            await self.simulate_function_call(func_name, args)
    
    async def test_emotional_cultural_analysis(self):
        """Test cultural emotional context analysis."""
        await self.simulate_function_call("analyze_emotion", {
            "analysis_type": "cultural_context_analysis",
            "emotion": "I feel ashamed in front of my family"
        })
        await self.simulate_function_call("analyze_emotion", {
            "analysis_type": "cultural_context_analysis",
            "cultural_factor": "family_honor"
        })
    
    async def test_emotional_crisis_indicators(self):
        """Test emotional analysis for crisis indicators."""
        await self.simulate_function_call("analyze_emotion", {
            "analysis_type": "crisis_emotional_indicators",
            "emotion": "I feel completely hopeless"
        })
    
    # ===== SESSION MANAGEMENT TESTS =====
    
    async def test_session_documentation(self):
        """Test session management documentation calls."""
        session_actions = [
            ("manage_session", {"action": "start_session"}),
            ("manage_session", {"action": "update_notes", "note": "Client expressed suicidal thoughts"}),
            ("manage_session", {"action": "track_therapeutic_goals", "goal": "Improve mood stability"}),
            ("manage_session", {"action": "end_session"})
        ]
        
        for func_name, args in session_actions:
            await self.simulate_function_call(func_name, args)
    
    # ===== COMPLEX SCENARIO TESTS =====
    
    async def test_complex_crisis_scenario(self):
        """Test complex crisis scenario with multiple tool calls."""
        # Simulate a complex crisis situation that should trigger multiple tools
        await self.simulate_function_call("detect_crisis", {
            "action": "assess_risk",
            "user_input": "I feel worthless and want to end everything"
        })
        await self.simulate_function_call("analyze_emotion", {
            "analysis_type": "crisis_emotional_indicators",
            "emotion": "worthless"
        })
        await self.simulate_function_call("apply_cbt_technique", {
            "technique": "thought_challenging",
            "thought": "I'm worthless"
        })
        await self.simulate_function_call("manage_session", {
            "action": "update_notes",
            "note": "Crisis intervention activated"
        })
    
    async def test_islamic_cbt_complex_scenario(self):
        """Test complex Islamic CBT scenario."""
        await self.simulate_function_call("analyze_emotion", {
            "analysis_type": "detect_emotions",
            "emotion": "religious guilt"
        })
        await self.simulate_function_call("apply_cbt_technique", {
            "technique": "islamic_cbt_integration",
            "religious_concern": "I'm not a good Muslim"
        })
        await self.simulate_function_call("apply_cbt_technique", {
            "technique": "thought_challenging",
            "thought": "Allah is disappointed in me"
        })
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all test scenarios and return comprehensive results."""
        print("🚀 Starting Enhanced Prompt Testing Framework")
        print("=" * 60)
        
        await self.setup_mock_tools()
        
        test_scenarios = [
            # Crisis Detection Tests
            ("Crisis - Suicide Ideation", self.test_crisis_suicide_ideation, ["crisis_detection"]),
            ("Crisis - Self Harm", self.test_crisis_self_harm, ["crisis_detection"]),
            ("Crisis - Emergency Escalation", self.test_crisis_emergency_escalation, ["crisis_detection"]),
            
            # CBT Technique Tests
            ("CBT - Negative Thoughts", self.test_cbt_negative_thoughts, ["cbt_techniques"]),
            ("CBT - Behavioral Activation", self.test_cbt_behavioral_activation, ["cbt_techniques"]),
            ("CBT - Islamic Integration", self.test_cbt_islamic_integration, ["cbt_techniques"]),
            
            # Emotional Analysis Tests
            ("Emotional - Detection", self.test_emotional_detection, ["emotional_analysis"]),
            ("Emotional - Cultural Analysis", self.test_emotional_cultural_analysis, ["emotional_analysis"]),
            ("Emotional - Crisis Indicators", self.test_emotional_crisis_indicators, ["emotional_analysis"]),
            
            # Session Management Tests
            ("Session - Documentation", self.test_session_documentation, ["session_management"]),
            
            # Complex Scenarios
            ("Complex - Crisis Scenario", self.test_complex_crisis_scenario, ["crisis_detection", "emotional_analysis", "cbt_techniques", "session_management"]),
            ("Complex - Islamic CBT", self.test_islamic_cbt_complex_scenario, ["emotional_analysis", "cbt_techniques"])
        ]
        
        results = {
            "total_tests": len(test_scenarios),
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "detailed_results": []
        }
        
        for scenario_name, test_func, expected_tools in test_scenarios:
            result = await self.run_test_scenario(scenario_name, test_func, expected_tools)
            results["detailed_results"].append(result)
            
            if result["status"] == "PASS":
                results["passed"] += 1
            elif result["status"] == "FAIL":
                results["failed"] += 1
            else:
                results["errors"] += 1
        
        return results
    
    def print_summary(self, results: Dict[str, Any]):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("🧪 ENHANCED PROMPT TESTING SUMMARY")
        print("=" * 60)
        
        print(f"📊 Total Tests: {results['total_tests']}")
        print(f"✅ Passed: {results['passed']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⚠️  Errors: {results['errors']}")
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if results['failed'] > 0 or results['errors'] > 0:
            print("\n🔍 FAILED/ERROR TESTS:")
            for result in results['detailed_results']:
                if result['status'] != 'PASS':
                    print(f"  ❌ {result['scenario']}: {result['status']}")
                    for error in result['errors']:
                        print(f"    - {error}")
        
        print("\n🎯 TOOL CALL VALIDATION:")
        tool_usage = {}
        for result in results['detailed_results']:
            for tool in result['called_tools']:
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        for tool, count in tool_usage.items():
            print(f"  🔧 {tool}: {count} calls")
        
        if success_rate >= 90:
            print("\n🎉 EXCELLENT: Enhanced prompts are forcing systematic tool usage!")
        elif success_rate >= 75:
            print("\n👍 GOOD: Most enhanced prompts are working, minor issues to address")
        else:
            print("\n⚠️  NEEDS IMPROVEMENT: Enhanced prompts need refinement")

async def main():
    """Run the enhanced prompt testing framework."""
    tester = EnhancedPromptTester()
    results = await tester.run_all_tests()
    tester.print_summary(results)
    
    # Save results to file
    with open("enhanced_prompt_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: enhanced_prompt_test_results.json")
    
    return results

if __name__ == "__main__":
    # Run the tests
    test_results = asyncio.run(main())
    
    # Exit with appropriate code
    if test_results["failed"] > 0 or test_results["errors"] > 0:
        sys.exit(1)
    else:
        print("\n🚀 All tests passed! Enhanced prompts are working correctly.")
        sys.exit(0) 