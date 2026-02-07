"""API Discovery and Catalog System"""
from typing import List, Dict, Any
from dataclasses import dataclass
import json

@dataclass
class APIEndpoint:
    """Represents an API endpoint"""
    name: str
    provider: str
    description: str
    category: str
    method: str
    endpoint: str
    capabilities: List[str]
    authentication: str
    
class APICatalog:
    """Searchable catalog of available APIs"""
    
    def __init__(self):
        self.apis = self._load_catalog()
    
    def _load_catalog(self) -> List[APIEndpoint]:
        """Load API catalog"""
        return [
            # Communication APIs
            APIEndpoint(
                name="Slack Send Message",
                provider="Slack",
                description="Send messages to Slack channels",
                category="communication",
                method="POST",
                endpoint="/chat.postMessage",
                capabilities=["send message", "notify team", "post update", "channel communication"],
                authentication="OAuth2"
            ),
            APIEndpoint(
                name="Send Email",
                provider="Gmail/SMTP",
                description="Send email messages",
                category="communication",
                method="SMTP",
                endpoint="smtp.gmail.com",
                capabilities=["send email", "notify user", "email notification", "message delivery"],
                authentication="App Password"
            ),
            APIEndpoint(
                name="Send SMS",
                provider="Twilio",
                description="Send SMS text messages",
                category="communication",
                method="POST",
                endpoint="/Messages.json",
                capabilities=["send sms", "text message", "mobile notification"],
                authentication="API Key"
            ),
            
            # Calendar APIs
            APIEndpoint(
                name="Create Calendar Event",
                provider="Google Calendar",
                description="Create calendar events and meetings",
                category="calendar",
                method="POST",
                endpoint="/calendar/v3/calendars/primary/events",
                capabilities=["schedule meeting", "create event", "book time", "calendar invitation"],
                authentication="OAuth2"
            ),
            
            # Data APIs
            APIEndpoint(
                name="Create Database Record",
                provider="PostgreSQL/MySQL",
                description="Insert records into database",
                category="database",
                method="SQL INSERT",
                endpoint="database",
                capabilities=["store data", "save record", "database insert", "persist information"],
                authentication="Credentials"
            ),
            APIEndpoint(
                name="Update Spreadsheet",
                provider="Google Sheets",
                description="Add/update data in Google Sheets",
                category="data",
                method="POST",
                endpoint="/v4/spreadsheets",
                capabilities=["update sheet", "add row", "spreadsheet data", "log information"],
                authentication="OAuth2"
            ),
            
            # HR/User Management
            APIEndpoint(
                name="Create User Account",
                provider="Okta/AD",
                description="Create new user accounts",
                category="identity",
                method="POST",
                endpoint="/api/v1/users",
                capabilities=["create user", "provision account", "add employee", "user management"],
                authentication="API Key"
            ),
            APIEndpoint(
                name="Assign Access Rights",
                provider="IAM",
                description="Grant permissions and access",
                category="identity",
                method="POST",
                endpoint="/access/grant",
                capabilities=["grant access", "assign permissions", "provision access", "role assignment"],
                authentication="OAuth2"
            ),
        ]
    
    def search_apis(self, intent: str) -> List[APIEndpoint]:
        """
        Search for APIs matching user intent
        
        Args:
            intent: What the user is trying to do
            
        Returns:
            List of matching API endpoints
        """
        intent_lower = intent.lower()
        matches = []
        
        for api in self.apis:
            # Check if intent matches capabilities
            score = 0
            for capability in api.capabilities:
                if capability in intent_lower or intent_lower in capability:
                    score += 2
            
            # Check description
            if any(word in api.description.lower() for word in intent_lower.split()):
                score += 1
            
            if score > 0:
                matches.append((score, api))
        
        # Sort by relevance
        matches.sort(reverse=True, key=lambda x: x[0])
        
        return [api for score, api in matches]
    
    def get_apis_for_workflow(self, workflow_description: str) -> Dict[str, List[APIEndpoint]]:
        """
        Discover all APIs needed for a workflow
        
        Returns:
            Dict mapping workflow steps to API options
        """
        # Extract key actions from description
        actions = self._extract_actions(workflow_description)
        
        api_map = {}
        for action in actions:
            apis = self.search_apis(action)
            if apis:
                api_map[action] = apis[:3]  # Top 3 matches
        
        return api_map
    
    def _extract_actions(self, description: str) -> List[str]:
        """Extract action phrases from description"""
        # Simple keyword extraction
        keywords = [
            "send", "create", "update", "delete", "notify",
            "schedule", "assign", "grant", "add", "remove",
            "email", "message", "slack", "calendar", "database"
        ]
        
        actions = []
        words = description.lower().split()
        
        for i, word in enumerate(words):
            if word in keywords:
                # Get 2-3 word phrase
                phrase = ' '.join(words[i:min(i+3, len(words))])
                actions.append(phrase)
        
        return list(set(actions))
