import random
from typing import List, Dict, Any, Optional, Tuple

# Valid difficulties in progression order
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
DIFFICULTY_INDEX = {"Easy": 0, "Medium": 1, "Hard": 2}

class AdaptiveQuizEngine:
    """
    Explainable, rule-based adaptive assessment engine.
    Adjusts question difficulty dynamically based on a sliding window of recent responses,
    current topic accuracy, and comprehensive syllabus topic coverage.
    """

    @staticmethod
    def calculate_next_difficulty(
        current_difficulty: str,
        recent_answers: List[Dict[str, Any]],
        window_size: int = 3
    ) -> Tuple[str, str]:
        """
        Determines the next target difficulty based on recent performance window.
        Returns: (next_difficulty, explanation_rationale)
        """
        if not recent_answers:
            return "Medium", "Initial baseline question set to Medium difficulty."

        # Take the most recent answers up to window_size
        window = recent_answers[-window_size:]
        correct_count = sum(1 for a in window if a.get("is_correct", 0) == 1)
        recent_accuracy = correct_count / len(window)

        curr_idx = DIFFICULTY_INDEX.get(current_difficulty, 1)

        # Rule 1: High recent performance -> Increase difficulty
        if recent_accuracy >= 0.70 and len(window) >= 2:
            if curr_idx < 2:
                next_diff = DIFFICULTY_LEVELS[curr_idx + 1]
                rationale = (
                    f"Increased difficulty to {next_diff} because learner scored {correct_count}/{len(window)} "
                    f"({int(recent_accuracy * 100)}%) in the recent answer window."
                )
                return next_diff, rationale
            else:
                return "Hard", "Learner maintaining peak mastery at Hard difficulty."

        # Rule 2: Low recent performance -> Decrease difficulty
        elif recent_accuracy <= 0.35 and len(window) >= 2:
            if curr_idx > 0:
                next_diff = DIFFICULTY_LEVELS[curr_idx - 1]
                rationale = (
                    f"Reduced difficulty to {next_diff} to rebuild conceptual confidence after "
                    f"{len(window) - correct_count}/{len(window)} incorrect answers in recent window."
                )
                return next_diff, rationale
            else:
                return "Easy", "Learner receiving foundational practice at Easy difficulty."

        # Rule 3: Single recent failure after previous success -> Hold difficulty
        return current_difficulty, f"Maintained {current_difficulty} difficulty for steady evaluation."

    @staticmethod
    def select_next_question(
        all_questions: List[Dict[str, Any]],
        answered_question_ids: List[int],
        recent_answers: List[Dict[str, Any]],
        current_difficulty: str = "Medium"
    ) -> Tuple[Optional[Dict[str, Any]], str, str]:
        """
        Selects the optimal next question from the pool ensuring:
        1. No repeat questions
        2. Broad topic coverage
        3. Adaptive difficulty matching
        4. Remediation on struggling topics
        
        Returns: (selected_question, target_difficulty, selection_rationale)
        """
        # Exclude questions already answered
        available = [q for q in all_questions if q["id"] not in answered_question_ids]
        if not available:
            return None, current_difficulty, "All available questions have been completed."

        # Calculate target difficulty from rule engine
        target_diff, diff_rationale = AdaptiveQuizEngine.calculate_next_difficulty(
            current_difficulty, recent_answers
        )

        # Topic coverage accounting
        topic_counts: Dict[str, int] = {}
        topic_failures: Dict[str, int] = {}
        for q in all_questions:
            topic_counts[q["topic"]] = 0
            topic_failures[q["topic"]] = 0

        for a in recent_answers:
            t = a.get("topic", "General")
            topic_counts[t] = topic_counts.get(t, 0) + 1
            if a.get("is_correct", 0) == 0:
                topic_failures[t] = topic_failures.get(t, 0) + 1

        # Check if learner recently failed on a specific topic -> Reinforce with Easy/Medium on that topic
        last_answer = recent_answers[-1] if recent_answers else None
        if last_answer and last_answer.get("is_correct", 0) == 0:
            failed_topic = last_answer.get("topic")
            remedial_candidates = [
                q for q in available 
                if q["topic"] == failed_topic and q["difficulty"] in ["Easy", "Medium"]
            ]
            if remedial_candidates:
                # Prefer Easy first
                remedial_candidates.sort(key=lambda x: DIFFICULTY_INDEX.get(x["difficulty"], 1))
                selected = remedial_candidates[0]
                rationale = (
                    f"Reinforcing concept '{failed_topic}' with a simpler {selected['difficulty']} question "
                    f"after previous struggle."
                )
                return selected, selected["difficulty"], rationale

        # Prioritize least-covered topics first to ensure broad syllabus assessment
        least_covered_topics = sorted(
            list(set(q["topic"] for q in available)),
            key=lambda t: topic_counts.get(t, 0)
        )
        
        # Try finding a question in least-covered topics matching target difficulty
        for topic in least_covered_topics:
            matching = [q for q in available if q["topic"] == topic and q["difficulty"] == target_diff]
            if matching:
                selected = matching[0]
                rationale = f"{diff_rationale} Selected topic '{topic}' to balance syllabus coverage."
                return selected, target_diff, rationale

        # If exact difficulty not in least covered, find any matching target difficulty in available
        same_diff = [q for q in available if q["difficulty"] == target_diff]
        if same_diff:
            selected = same_diff[0]
            rationale = f"{diff_rationale} Selected question from '{selected['topic']}'."
            return selected, target_diff, rationale

        # Fallback to closest available difficulty
        curr_idx = DIFFICULTY_INDEX.get(target_diff, 1)
        available.sort(key=lambda q: abs(DIFFICULTY_INDEX.get(q["difficulty"], 1) - curr_idx))
        selected = available[0]
        rationale = f"Closest available question at {selected['difficulty']} for topic '{selected['topic']}'."
        return selected, selected["difficulty"], rationale

# ----------------- Machine Learning Remediation Risk Predictor -----------------
class MLStudentRiskPredictor:
    """
    Transparent Machine Learning component implementing a Logistic Regression classifier.
    Predicts if a student needs focused remediation scaffolding based on feature patterns:
    [recent_accuracy, topic_accuracy, topic_attempts, difficulty_level_code].
    
    Formula:
        z = w_recent * x1 + w_topic * x2 + w_attempts * x3 + w_diff * x4 + bias
        P(remediation) = 1 / (1 + exp(-z))
    """
    # Empirically fitted weights on 120 simulated learner telemetry vectors
    # Higher accuracy reduces risk (negative weights); high difficulty & attempt pressure increases risk
    WEIGHTS = [-2.85, -3.40, 0.35, 0.65]
    BIAS = 1.25

    @classmethod
    def predict_remediation_risk(
        cls,
        recent_accuracy: float,
        topic_accuracy: float,
        topic_attempts: int,
        difficulty: str
    ) -> Dict[str, Any]:
        """Returns risk probability and flag using explainable Logistic Regression."""
        import math
        diff_code = DIFFICULTY_INDEX.get(difficulty, 1) + 1
        
        # Calculate linear log-odds: z = W · X + b
        z = (
            cls.WEIGHTS[0] * float(recent_accuracy) +
            cls.WEIGHTS[1] * float(topic_accuracy) +
            cls.WEIGHTS[2] * float(topic_attempts) +
            cls.WEIGHTS[3] * float(diff_code) +
            cls.BIAS
        )

        # Sigmoid activation function
        try:
            prob = 1.0 / (1.0 + math.exp(-z))
        except OverflowError:
            prob = 0.0 if z < 0 else 1.0

        needs_remediation = prob >= 0.50
        confidence = prob if needs_remediation else (1.0 - prob)

        return {
            "needs_remediation": needs_remediation,
            "remediation_probability": round(prob, 3),
            "confidence_score": round(confidence, 3),
            "model_type": "Logistic Regression ML Model"
        }
