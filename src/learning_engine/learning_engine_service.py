"""
Adaptive Learning Engine Service
Continuously learns from how teams work, adapting to their unique styles and preferences
"""
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict
import json

class AdaptiveLearningEngine:
    """
    Adaptive Learning Engine - Personal assistant that evolves with the team
    Suggests smarter workflows, automates repetitive tasks, and predicts information needs
    """
    
    def __init__(self):
        self.user_profiles = {}  # User learning profiles
        self.team_profiles = {}  # Team-level patterns
        self.workflow_patterns = defaultdict(list)  # Common workflow sequences
        self.task_predictions = {}  # Next task predictions
        self.automation_rules = {}  # Automation rules learned from behavior
        
    def create_user_profile(self, 
                           user_id: str, 
                           team_id: str = None,
                           initial_preferences: Dict = None) -> Dict:
        """
        Create or update a user's learning profile
        
        Args:
            user_id: Unique user identifier
            team_id: Team identifier
            initial_preferences: Initial user preferences
            
        Returns:
            User profile dict
        """
        profile = {
            "user_id": user_id,
            "team_id": team_id,
            "skill_level": "intermediate",  # beginner, intermediate, advanced, expert
            "learning_style": "visual",  # visual, auditory, kinesthetic, reading
            "productivity_patterns": {
                "peak_hours": [],
                "break_frequency": 0,
                "task_switching_rate": 0
            },
            "preferences": initial_preferences or {},
            "workflow_history": [],
            "completed_tasks": [],
            "automation_acceptance_rate": 0.0,
            "suggestion_feedback": {
                "accepted": 0,
                "rejected": 0,
                "ignored": 0
            },
            "created_at": datetime.utcnow(),
            "last_updated": datetime.utcnow()
        }
        
        self.user_profiles[user_id] = profile
        
        # Update team profile if team_id provided
        if team_id:
            self._update_team_profile(team_id, user_id)
        
        return profile
    
    def record_workflow_event(self, 
                             user_id: str, 
                             event_type: str, 
                             event_data: Dict) -> None:
        """
        Record a workflow event for learning
        
        Args:
            user_id: User ID
            event_type: Type of event (task_started, task_completed, tool_used, etc.)
            event_data: Event details
        """
        if user_id not in self.user_profiles:
            return
        
        profile = self.user_profiles[user_id]
        
        event = {
            "timestamp": datetime.utcnow(),
            "event_type": event_type,
            "data": event_data
        }
        
        profile["workflow_history"].append(event)
        
        # Keep only last 1000 events per user
        if len(profile["workflow_history"]) > 1000:
            profile["workflow_history"] = profile["workflow_history"][-1000:]
        
        # Analyze pattern in real-time
        self._analyze_workflow_pattern(user_id, event)
        
        profile["last_updated"] = datetime.utcnow()
    
    def get_workflow_suggestions(self, 
                                user_id: str, 
                                current_context: Dict = None,
                                limit: int = 5) -> List[Dict]:
        """
        Get intelligent workflow suggestions based on learned patterns
        
        Args:
            user_id: User ID
            current_context: Current task/project context
            limit: Maximum suggestions
            
        Returns:
            List of workflow suggestions
        """
        suggestions = []
        
        if user_id not in self.user_profiles:
            return suggestions
        
        profile = self.user_profiles[user_id]
        
        # Suggestion 1: Next likely task
        next_task = self._predict_next_task(user_id, current_context)
        if next_task:
            suggestions.append({
                "type": "next_task_prediction",
                "title": f"Next: {next_task['task_name']}",
                "description": f"Based on your pattern, you typically do {next_task['task_name']} after {next_task['previous_task']}",
                "confidence": next_task['confidence'],
                "action": next_task
            })
        
        # Suggestion 2: Automation opportunity
        automation = self._find_automation_opportunity(user_id, current_context)
        if automation:
            suggestions.append({
                "type": "automation_suggestion",
                "title": "Automate this repetitive task",
                "description": f"You've done '{automation['task_name']}' {automation['frequency']} times. Automate it?",
                "confidence": automation['confidence'],
                "action": automation
            })
        
        # Suggestion 3: Optimal timing
        timing = self._get_optimal_timing(user_id, current_context)
        if timing:
            suggestions.append({
                "type": "timing_optimization",
                "title": "Best time for this task",
                "description": f"You're most productive at {timing['peak_time']} for {timing['task_type']} tasks",
                "confidence": timing['confidence'],
                "action": timing
            })
        
        # Suggestion 4: Skill development
        skill = self._suggest_skill_development(user_id)
        if skill:
            suggestions.append({
                "type": "skill_development",
                "title": "Level up your skills",
                "description": skill['description'],
                "confidence": skill['confidence'],
                "action": skill
            })
        
        # Suggestion 5: Team collaboration
        collaboration = self._suggest_collaboration(user_id)
        if collaboration:
            suggestions.append({
                "type": "collaboration_opportunity",
                "title": "Collaborate with teammates",
                "description": collaboration['description'],
                "confidence": collaboration['confidence'],
                "action": collaboration
            })
        
        # Sort by confidence and return
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        return suggestions[:limit]
    
    def get_productivity_insights(self, user_id: str) -> Dict:
        """
        Generate productivity insights for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Productivity insights report
        """
        if user_id not in self.user_profiles:
            return {"error": "User profile not found"}
        
        profile = self.user_profiles[user_id]
        history = profile["workflow_history"]
        
        # Analyze patterns
        peak_hours = self._calculate_peak_hours(history)
        task_completion_rate = self._calculate_completion_rate(history)
        avg_task_duration = self._calculate_avg_task_duration(history)
        focus_score = self._calculate_focus_score(history)
        
        return {
            "user_id": user_id,
            "productivity_score": self._calculate_productivity_score(profile),
            "peak_hours": peak_hours,
            "task_completion_rate": task_completion_rate,
            "average_task_duration_minutes": avg_task_duration,
            "focus_score": focus_score,
            "skill_level": profile["skill_level"],
            "automation_acceptance_rate": profile["automation_acceptance_rate"],
            "suggestion_acceptance_rate": self._calculate_suggestion_acceptance_rate(profile),
            "recommendations": self._generate_productivity_recommendations(profile)
        }
    
    def create_automation_rule(self, 
                              user_id: str, 
                              trigger: Dict, 
                              action: Dict,
                              name: str = None) -> Dict:
        """
        Create an automation rule based on learned patterns
        
        Args:
            user_id: User ID
            trigger: Trigger conditions
            action: Action to execute
            name: Rule name
            
        Returns:
            Created automation rule
        """
        rule_id = f"auto_{user_id}_{len(self.automation_rules)}"
        
        rule = {
            "id": rule_id,
            "user_id": user_id,
            "name": name or f"Automation Rule {len(self.automation_rules) + 1}",
            "trigger": trigger,
            "action": action,
            "enabled": True,
            "execution_count": 0,
            "success_rate": 1.0,
            "created_at": datetime.utcnow(),
            "last_executed": None
        }
        
        self.automation_rules[rule_id] = rule
        return rule
    
    def execute_automation(self, rule_id: str, context: Dict) -> Dict:
        """
        Execute an automation rule
        
        Args:
            rule_id: Rule ID
            context: Execution context
            
        Returns:
            Execution result
        """
        if rule_id not in self.automation_rules:
            return {"error": "Rule not found"}
        
        rule = self.automation_rules[rule_id]
        
        if not rule["enabled"]:
            return {"error": "Rule is disabled"}
        
        # Check if trigger conditions are met
        if not self._check_trigger_conditions(rule["trigger"], context):
            return {"status": "trigger_not_met"}
        
        # Execute action
        result = self._execute_action(rule["action"], context)
        
        # Update rule stats
        rule["execution_count"] += 1
        rule["last_executed"] = datetime.utcnow()
        if result.get("success"):
            rule["success_rate"] = (rule["success_rate"] * (rule["execution_count"] - 1) + 1) / rule["execution_count"]
        else:
            rule["success_rate"] = (rule["success_rate"] * (rule["execution_count"] - 1)) / rule["execution_count"]
        
        return result
    
    def get_team_insights(self, team_id: str) -> Dict:
        """
        Get insights for a team
        
        Args:
            team_id: Team ID
            
        Returns:
            Team insights report
        """
        if team_id not in self.team_profiles:
            return {"error": "Team profile not found"}
        
        team_profile = self.team_profiles[team_id]
        member_ids = team_profile.get("members", [])
        
        # Aggregate member insights
        member_insights = []
        for member_id in member_ids:
            if member_id in self.user_profiles:
                insights = self.get_productivity_insights(member_id)
                member_insights.append(insights)
        
        return {
            "team_id": team_id,
            "member_count": len(member_ids),
            "average_productivity_score": sum(m.get("productivity_score", 0) for m in member_insights) / max(len(member_insights), 1),
            "common_workflow_patterns": team_profile.get("common_patterns", []),
            "collaboration_score": self._calculate_collaboration_score(team_profile),
            "bottlenecks": self._identify_bottlenecks(team_profile),
            "recommendations": self._generate_team_recommendations(team_profile)
        }
    
    def _update_team_profile(self, team_id: str, user_id: str) -> None:
        """Update team profile with new member"""
        if team_id not in self.team_profiles:
            self.team_profiles[team_id] = {
                "team_id": team_id,
                "members": [],
                "common_patterns": [],
                "collaboration_events": [],
                "created_at": datetime.utcnow()
            }
        
        if user_id not in self.team_profiles[team_id]["members"]:
            self.team_profiles[team_id]["members"].append(user_id)
    
    def _analyze_workflow_pattern(self, user_id: str, event: Dict) -> None:
        """Analyze workflow patterns in real-time"""
        profile = self.user_profiles[user_id]
        history = profile["workflow_history"]
        
        if len(history) < 2:
            return
        
        # Detect sequential patterns
        last_event = history[-2]
        current_event = history[-1]
        
        pattern_key = f"{last_event['event_type']}->{current_event['event_type']}"
        self.workflow_patterns[pattern_key].append({
            "user_id": user_id,
            "timestamp": datetime.utcnow()
        })
        
        # Update skill level based on complexity
        self._update_skill_level(user_id, event)
    
    def _predict_next_task(self, user_id: str, context: Dict = None) -> Optional[Dict]:
        """Predict the next likely task"""
        profile = self.user_profiles[user_id]
        history = profile["workflow_history"]
        
        if len(history) < 3:
            return None
        
        # Simple pattern matching (in production, use ML models)
        recent_tasks = [e for e in history[-10:] if e["event_type"] == "task_completed"]
        
        if len(recent_tasks) < 2:
            return None
        
        # Find most common next task
        task_sequences = defaultdict(int)
        for i in range(len(recent_tasks) - 1):
            current = recent_tasks[i]["data"].get("task_name")
            next_task = recent_tasks[i + 1]["data"].get("task_name")
            if current and next_task:
                task_sequences[(current, next_task)] += 1
        
        if not task_sequences:
            return None
        
        most_common = max(task_sequences.items(), key=lambda x: x[1])
        confidence = min(most_common[1] / 10.0, 0.95)  # Cap at 95%
        
        return {
            "task_name": most_common[0][1],
            "previous_task": most_common[0][0],
            "confidence": confidence,
            "frequency": most_common[1]
        }
    
    def _find_automation_opportunity(self, user_id: str, context: Dict = None) -> Optional[Dict]:
        """Find opportunities for automation"""
        profile = self.user_profiles[user_id]
        history = profile["workflow_history"]
        
        # Count repeated task sequences
        task_counts = defaultdict(int)
        for event in history:
            if event["event_type"] == "task_completed":
                task_name = event["data"].get("task_name")
                if task_name:
                    task_counts[task_name] += 1
        
        # Find highly repetitive tasks
        for task_name, count in task_counts.items():
            if count >= 5:  # Done at least 5 times
                return {
                    "task_name": task_name,
                    "frequency": count,
                    "confidence": min(count / 20.0, 0.9),
                    "estimated_time_savings": count * 5  # Assume 5 minutes per task
                }
        
        return None
    
    def _get_optimal_timing(self, user_id: str, context: Dict = None) -> Optional[Dict]:
        """Get optimal timing for tasks"""
        profile = self.user_profiles[user_id]
        history = profile["workflow_history"]
        
        # Analyze when user completes tasks most efficiently
        hour_efficiency = defaultdict(list)
        for event in history:
            if event["event_type"] == "task_completed":
                hour = event["timestamp"].hour
                duration = event["data"].get("duration_minutes", 30)
                efficiency = 100 / max(duration, 1)  # Higher is better
                hour_efficiency[hour].append(efficiency)
        
        if not hour_efficiency:
            return None
        
        # Find best hour
        avg_efficiency = {hour: sum(effs) / len(effs) for hour, effs in hour_efficiency.items()}
        best_hour = max(avg_efficiency.items(), key=lambda x: x[1])[0]
        
        return {
            "peak_time": f"{best_hour:02d}:00",
            "task_type": "general",
            "confidence": 0.7,
            "efficiency_score": avg_efficiency[best_hour]
        }
    
    def _suggest_skill_development(self, user_id: str) -> Optional[Dict]:
        """Suggest skill development opportunities"""
        profile = self.user_profiles[user_id]
        
        skill_level = profile["skill_level"]
        completed_tasks = len(profile["completed_tasks"])
        
        # Simple progression logic
        if skill_level == "beginner" and completed_tasks > 10:
            return {
                "description": "You're ready to advance to intermediate level! Try more complex tasks.",
                "confidence": 0.8,
                "suggested_level": "intermediate"
            }
        elif skill_level == "intermediate" and completed_tasks > 50:
            return {
                "description": "Consider specializing in an advanced area based on your strengths.",
                "confidence": 0.75,
                "suggested_level": "advanced"
            }
        
        return None
    
    def _suggest_collaboration(self, user_id: str) -> Optional[Dict]:
        """Suggest collaboration opportunities"""
        profile = self.user_profiles[user_id]
        team_id = profile.get("team_id")
        
        if not team_id or team_id not in self.team_profiles:
            return None
        
        team_profile = self.team_profiles[team_id]
        
        # Find teammates with complementary skills
        teammates = [m for m in team_profile["members"] if m != user_id]
        
        if teammates:
            return {
                "description": f"Collaborate with {len(teammates)} team members on shared projects",
                "confidence": 0.65,
                "teammates": teammates[:3]
            }
        
        return None
    
    def _calculate_peak_hours(self, history: List[Dict]) -> List[int]:
        """Calculate user's peak productivity hours"""
        hour_productivity = defaultdict(int)
        
        for event in history:
            if event["event_type"] == "task_completed":
                hour = event["timestamp"].hour
                hour_productivity[hour] += 1
        
        if not hour_productivity:
            return [9, 10, 11, 14, 15, 16]  # Default business hours
        
        # Return top 3 hours
        sorted_hours = sorted(hour_productivity.items(), key=lambda x: x[1], reverse=True)
        return [h[0] for h in sorted_hours[:3]]
    
    def _calculate_completion_rate(self, history: List[Dict]) -> float:
        """Calculate task completion rate"""
        started = sum(1 for e in history if e["event_type"] == "task_started")
        completed = sum(1 for e in history if e["event_type"] == "task_completed")
        
        return completed / max(started, 1)
    
    def _calculate_avg_task_duration(self, history: List[Dict]) -> float:
        """Calculate average task duration"""
        durations = [e["data"].get("duration_minutes", 30) 
                    for e in history if e["event_type"] == "task_completed"]
        
        return sum(durations) / max(len(durations), 1)
    
    def _calculate_focus_score(self, history: List[Dict]) -> float:
        """Calculate focus score based on task switching"""
        if len(history) < 2:
            return 1.0
        
        switches = 0
        for i in range(1, len(history)):
            if history[i]["event_type"] != history[i-1]["event_type"]:
                switches += 1
        
        # Lower switches = higher focus
        switch_rate = switches / max(len(history), 1)
        return max(0, 1.0 - switch_rate)
    
    def _calculate_productivity_score(self, profile: Dict) -> float:
        """Calculate overall productivity score"""
        completion_rate = self._calculate_completion_rate(profile["workflow_history"])
        focus_score = self._calculate_focus_score(profile["workflow_history"])
        acceptance_rate = self._calculate_suggestion_acceptance_rate(profile)
        
        return (completion_rate * 0.4 + focus_score * 0.3 + acceptance_rate * 0.3) * 100
    
    def _calculate_suggestion_acceptance_rate(self, profile: Dict) -> float:
        """Calculate suggestion acceptance rate"""
        feedback = profile["suggestion_feedback"]
        total = feedback["accepted"] + feedback["rejected"] + feedback["ignored"]
        
        if total == 0:
            return 0.5  # Default
        
        return feedback["accepted"] / total
    
    def _generate_productivity_recommendations(self, profile: Dict) -> List[str]:
        """Generate productivity recommendations"""
        recommendations = []
        
        completion_rate = self._calculate_completion_rate(profile["workflow_history"])
        if completion_rate < 0.7:
            recommendations.append("Focus on completing started tasks before starting new ones")
        
        focus_score = self._calculate_focus_score(profile["workflow_history"])
        if focus_score < 0.6:
            recommendations.append("Reduce task switching to improve focus")
        
        if profile["automation_acceptance_rate"] < 0.3:
            recommendations.append("Consider accepting more automation suggestions to save time")
        
        return recommendations
    
    def _check_trigger_conditions(self, trigger: Dict, context: Dict) -> bool:
        """Check if automation trigger conditions are met"""
        # Simple condition checking (expand in production)
        for key, value in trigger.items():
            if context.get(key) != value:
                return False
        return True
    
    def _execute_action(self, action: Dict, context: Dict) -> Dict:
        """Execute automation action"""
        # Placeholder for action execution
        return {
            "success": True,
            "action": action,
            "result": "Action executed successfully"
        }
    
    def _calculate_collaboration_score(self, team_profile: Dict) -> float:
        """Calculate team collaboration score"""
        collaboration_events = len(team_profile.get("collaboration_events", []))
        member_count = len(team_profile.get("members", []))
        
        if member_count == 0:
            return 0.0
        
        return min(collaboration_events / (member_count * 10), 1.0)
    
    def _identify_bottlenecks(self, team_profile: Dict) -> List[str]:
        """Identify team bottlenecks"""
        bottlenecks = []
        
        # Simple bottleneck detection
        if len(team_profile.get("members", [])) > 10:
            bottlenecks.append("Large team size may slow decision-making")
        
        return bottlenecks
    
    def _generate_team_recommendations(self, team_profile: Dict) -> List[str]:
        """Generate team recommendations"""
        recommendations = []
        
        member_count = len(team_profile.get("members", []))
        if member_count > 0 and member_count < 3:
            recommendations.append("Consider expanding team for better coverage")
        
        return recommendations
    
    def _update_skill_level(self, user_id: str, event: Dict) -> None:
        """Update user's skill level based on activity"""
        profile = self.user_profiles[user_id]
        completed_count = len([e for e in profile["workflow_history"] 
                              if e["event_type"] == "task_completed"])
        
        if completed_count > 100:
            profile["skill_level"] = "expert"
        elif completed_count > 50:
            profile["skill_level"] = "advanced"
        elif completed_count > 20:
            profile["skill_level"] = "intermediate"
        elif completed_count > 5:
            profile["skill_level"] = "beginner"


# Initialize service instance
learning_engine = AdaptiveLearningEngine()
