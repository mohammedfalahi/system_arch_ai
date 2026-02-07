"""Generate Visual Workflow Diagrams"""
import json
from typing import Dict, Any

class DiagramGenerator:
    """Generate Mermaid flowcharts from workflow plans"""
    
    def __init__(self):
        self.integration_icons = {
            'email': '📧',
            'slack': '💬',
            'database': '🗄️',
            'calendar': '📅',
            'api': '🔌',
            'notification': '🔔',
            'file': '📄',
            'http': '🌐'
        }
    
    def generate_mermaid(self, workflow_plan: Dict[str, Any]) -> str:
        """
        Generate Mermaid flowchart from workflow plan
        
        Args:
            workflow_plan: JSON workflow plan from Reasoner
            
        Returns:
            Mermaid diagram syntax
        """
        mermaid = ["graph TB"]
        mermaid.append("    Start([🚀 Start Workflow])")
        
        steps = workflow_plan.get('steps', [])
        
        for i, step in enumerate(steps):
            step_id = f"Step{i+1}"
            step_name = step.get('step_name', step.get('step', f'Step {i+1}'))
            integration = step.get('integration_needed')
            
            # Get icon for step
            icon = self._get_step_icon(integration)
            
            # Create step node
            mermaid.append(f"    {step_id}[{icon} {step_name}]")
            
            # Connect to previous step
            if i == 0:
                mermaid.append(f"    Start --> {step_id}")
            else:
                prev_step = f"Step{i}"
                mermaid.append(f"    {prev_step} --> {step_id}")
            
            # Add integration details
            if integration:
                int_icon = self.integration_icons.get(integration.lower(), '🔧')
                mermaid.append(f"    {step_id} -.-|uses| {integration.upper()}{i}({int_icon} {integration})")
        
        # Add end node
        last_step = f"Step{len(steps)}"
        mermaid.append(f"    {last_step} --> End([✅ Complete])")
        
        # Add styling
        mermaid.append("    classDef startEnd fill:#4CAF50,stroke:#2E7D32,color:#fff")
        mermaid.append("    classDef stepNode fill:#2196F3,stroke:#1565C0,color:#fff")
        mermaid.append("    class Start,End startEnd")
        mermaid.append(f"    class {','.join([f'Step{i+1}' for i in range(len(steps))])} stepNode")
        
        return '\n'.join(mermaid)
    
    def _get_step_icon(self, integration: str) -> str:
        """Get icon for step based on integration"""
        if not integration:
            return '⚙️'
        
        return self.integration_icons.get(integration.lower(), '🔧')
    
    def generate_html_diagram(self, mermaid_code: str) -> str:
        """
        Generate HTML with Mermaid diagram
        
        Args:
            mermaid_code: Mermaid syntax
            
        Returns:
            HTML string with embedded diagram
        """
        html = f"""
        <div class="mermaid">
        {mermaid_code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
        </script>
        """
        return html
