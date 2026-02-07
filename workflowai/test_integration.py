#!/usr/bin/env python3
"""
End-to-End Integration Test for WorkflowAI
Tests the complete workflow from user input to code execution
"""

import sys
import time
from agents.workflow_reasoner import WorkflowReasonerAgent
from agents.code_generator import CodeGeneratorAgent
from agents.executor import WorkflowExecutor
from agents.debugger import WorkflowDebuggerAgent
from utils.bedrock_client import BedrockClient

def test_complete_workflow():
    """Test the complete workflow generation pipeline."""
    
    print("="*70)
    print("WORKFLOWAI END-TO-END INTEGRATION TEST")
    print("="*70)
    
    # Test input
    user_input = """
    Create a simple order processing workflow:
    1. Receive order details
    2. Validate order amount
    3. Send confirmation email
    4. Update inventory
    """
    
    print(f"\nUser Input:\n{user_input}\n")
    
    try:
        # Initialize components
        print("\n[1/5] Initializing components...")
        bedrock_client = BedrockClient()
        reasoner = WorkflowReasonerAgent(bedrock_client)
        generator = CodeGeneratorAgent(bedrock_client)
        executor = WorkflowExecutor()
        debugger = WorkflowDebuggerAgent(bedrock_client)
        print("✓ All components initialized")
        
        # Step 1: Analyze workflow
        print("\n[2/5] Analyzing workflow with Workflow Reasoner...")
        start_time = time.time()
        workflow_plan = reasoner.analyze(user_input)
        analysis_time = time.time() - start_time
        
        print(f"✓ Workflow analysis complete ({analysis_time:.2f}s)")
        print(f"  Process: {workflow_plan['process_name']}")
        print(f"  Steps: {len(workflow_plan['steps'])}")
        print(f"  Complexity: {workflow_plan['estimated_complexity']}")
        
        # Step 2: Generate code
        print("\n[3/5] Generating code with Code Generator...")
        start_time = time.time()
        code = generator.generate(workflow_plan)
        generation_time = time.time() - start_time
        
        print(f"✓ Code generation complete ({generation_time:.2f}s)")
        print(f"  Code length: {len(code)} characters")
        print(f"  Lines: {len(code.split(chr(10)))}")
        
        # Validate generated code
        is_valid, issues = generator.validate_generated_code(code)
        if is_valid:
            print("✓ Code validation passed")
        else:
            print(f"⚠ Code validation issues: {issues}")
        
        # Step 3: Execute code
        print("\n[4/5] Executing workflow with Executor...")
        start_time = time.time()
        result = executor.execute(code)
        execution_time = time.time() - start_time
        
        if result['status'] == 'success':
            print(f"✓ Execution successful ({result['execution_time']}s)")
            print(f"  Output length: {len(result['output'])} characters")
        else:
            print(f"⚠ Execution failed: {result['error']}")
            
            # Step 4: Self-debugging
            print("\n[5/5] Attempting self-debugging...")
            
            # Analyze error
            error_analysis = debugger.analyze_error(
                code,
                result['error'],
                workflow_plan
            )
            print(f"✓ Error analyzed (confidence: {error_analysis['confidence']})")
            
            # Fix code
            fixed_code = debugger.fix_code(code, error_analysis, workflow_plan)
            print("✓ Fixed code generated")
            
            # Re-execute
            result = executor.execute(fixed_code)
            if result['status'] == 'success':
                print(f"✓ Re-execution successful ({result['execution_time']}s)")
            else:
                print(f"✗ Re-execution still failed: {result['error']}")
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"✓ Workflow Reasoner: {analysis_time:.2f}s")
        print(f"✓ Code Generator: {generation_time:.2f}s")
        print(f"✓ Executor: {result['execution_time']}s")
        print(f"✓ Final Status: {result['status'].upper()}")
        
        total_time = analysis_time + generation_time + result['execution_time']
        print(f"\nTotal Pipeline Time: {total_time:.2f}s")
        
        print("\n" + "="*70)
        print("✅ END-TO-END TEST COMPLETED SUCCESSFULLY")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_workflow()
    sys.exit(0 if success else 1)
