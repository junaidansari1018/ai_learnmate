from typing import List, Dict, Any, Tuple

class LearningAnalyzer:
    """
    Analyzes student quiz answers to identify conceptual gaps, estimate topic mastery,
    detect error patterns, and formulate concrete study recommendations.
    Enforces honest evidence requirements (e.g., single-question topics are marked with limited evidence).
    """

    @staticmethod
    def analyze_attempt(
        answers: List[Dict[str, Any]],
        total_questions: int
    ) -> Dict[str, Any]:
        """
        Processes answers and returns a comprehensive gap analysis report.
        """
        if not answers:
            return {
                "overall_score": 0.0,
                "overall_percentage": 0.0,
                "total_answered": 0,
                "total_correct": 0,
                "total_incorrect": 0,
                "topic_breakdown": [],
                "strong_topics": [],
                "developing_topics": [],
                "revision_topics": [],
                "limited_evidence_topics": [],
                "misconception_patterns": [],
                "actionable_recommendations": [],
                "follow_up_practice": []
            }

        total_answered = len(answers)
        total_correct = sum(1 for a in answers if a.get("is_correct", 0) == 1)
        total_incorrect = total_answered - total_correct
        total_score = sum(float(a.get("score_awarded", 1.0 if a.get("is_correct") == 1 else 0.0)) for a in answers)
        overall_percentage = round((total_score / max(1, total_answered)) * 100, 1)

        # 1. Group answers by topic
        topics_map: Dict[str, Dict[str, Any]] = {}
        for ans in answers:
            topic = ans.get("topic", "Core Concepts").strip()
            if topic not in topics_map:
                topics_map[topic] = {
                    "topic": topic,
                    "attempted": 0,
                    "correct": 0,
                    "score_sum": 0.0,
                    "wrong_answers": [],
                    "questions_details": []
                }
            
            topics_map[topic]["attempted"] += 1
            is_corr = ans.get("is_correct", 0) == 1
            if is_corr:
                topics_map[topic]["correct"] += 1
            else:
                topics_map[topic]["wrong_answers"].append(ans)
            
            topics_map[topic]["score_sum"] += float(ans.get("score_awarded", 1.0 if is_corr else 0.0))
            topics_map[topic]["questions_details"].append(ans)

        topic_breakdown = []
        strong_topics = []
        developing_topics = []
        revision_topics = []
        limited_evidence_topics = []
        misconception_patterns = []
        actionable_recommendations = []
        follow_up_practice = []

        # 2. Evaluate mastery per topic with minimum evidence constraints
        for topic_name, data in topics_map.items():
            attempted = data["attempted"]
            correct = data["correct"]
            accuracy = round((correct / attempted) * 100, 1)
            wrong_list = data["wrong_answers"]

            # Honest Evidence Check: 1 question is insufficient for confident mastery labeling
            if attempted == 1:
                mastery = "Limited Evidence"
                evidence_note = "Limited evidence: only 1 question attempted. Complete more questions to establish definitive mastery."
                needs_revision = 1 if correct == 0 else 0
                limited_evidence_topics.append({
                    "topic": topic_name,
                    "accuracy": accuracy,
                    "note": evidence_note,
                    "is_correct": correct == 1
                })
            else:
                if accuracy >= 80.0:
                    mastery = "Strong understanding"
                    evidence_note = f"Solid performance ({correct}/{attempted} correct). Key concepts well understood."
                    needs_revision = 0
                    strong_topics.append({
                        "topic": topic_name,
                        "accuracy": accuracy,
                        "attempted": attempted,
                        "correct": correct
                    })
                elif accuracy >= 50.0:
                    mastery = "Developing understanding"
                    evidence_note = f"Moderate grasp ({correct}/{attempted} correct). Minor conceptual gaps detected."
                    needs_revision = 1
                    developing_topics.append({
                        "topic": topic_name,
                        "accuracy": accuracy,
                        "attempted": attempted,
                        "correct": correct
                    })
                else:
                    mastery = "Needs revision"
                    evidence_note = f"High error rate ({correct}/{attempted} correct). Needs targeted study."
                    needs_revision = 1
                    revision_topics.append({
                        "topic": topic_name,
                        "accuracy": accuracy,
                        "attempted": attempted,
                        "correct": correct
                    })

            # Detect specific misconceptions from wrong answers
            topic_misconceptions = []
            for w in wrong_list:
                q_text = w.get("question_text", "")
                stu_ans = w.get("student_answer", "")
                corr_ans = w.get("correct_answer", "")
                explanation = w.get("explanation", "")
                
                misconception_item = {
                    "topic": topic_name,
                    "question_snippet": q_text[:80] + ("..." if len(q_text) > 80 else ""),
                    "student_submitted": stu_ans,
                    "expected_concept": corr_ans,
                    "key_takeaway": explanation
                }
                topic_misconceptions.append(misconception_item)
                misconception_patterns.append(misconception_item)

            topic_breakdown.append({
                "topic": topic_name,
                "questions_attempted": attempted,
                "questions_correct": correct,
                "accuracy_percentage": accuracy,
                "mastery_level": mastery,
                "needs_revision": needs_revision,
                "evidence_note": evidence_note,
                "misconceptions": topic_misconceptions
            })

        # Sort breakdown: weakest topics first
        topic_breakdown.sort(key=lambda x: x["accuracy_percentage"])

        # 3. Generate tailored recommendations connected directly to observed mistakes
        if revision_topics:
            for rt in revision_topics:
                actionable_recommendations.append({
                    "priority": "High",
                    "topic": rt["topic"],
                    "action": f"Re-read the lecture section on '{rt['topic']}'. Focus on foundational definitions and practice 3 basic problems.",
                    "tag": "Needs Urgent Review"
                })
                follow_up_practice.append({
                    "topic": rt["topic"],
                    "prompt": f"Practice Task: Write down the definition of '{rt['topic']}' in your own words and explain how it solves concurrent conflicts."
                })

        if developing_topics:
            for dt in developing_topics:
                actionable_recommendations.append({
                    "priority": "Medium",
                    "topic": dt["topic"],
                    "action": f"Review edge cases and tricky scenarios for '{dt['topic']}' to convert developing knowledge into mastery.",
                    "tag": "Solidify Understanding"
                })
                follow_up_practice.append({
                    "topic": dt["topic"],
                    "prompt": f"Self-Check: Can you explain the difference between mutex locks and semaphores in '{dt['topic']}'?"
                })

        if limited_evidence_topics:
            for lt in limited_evidence_topics:
                if not lt["is_correct"]:
                    actionable_recommendations.append({
                        "priority": "Medium",
                        "topic": lt["topic"],
                        "action": f"You missed the single question asked on '{lt['topic']}'. Take a dedicated mini-quiz on this topic to clarify concepts.",
                        "tag": "Verify Concept"
                    })

        if strong_topics and not revision_topics:
            actionable_recommendations.append({
                "priority": "Low",
                "topic": strong_topics[0]["topic"],
                "action": "Great work! Challenge yourself with advanced competitive or GATE-level questions on this subject.",
                "tag": "Advanced Mastery"
            })

        return {
            "overall_score": round(total_score, 1),
            "overall_percentage": overall_percentage,
            "total_answered": total_answered,
            "total_correct": total_correct,
            "total_incorrect": total_incorrect,
            "topic_breakdown": topic_breakdown,
            "strong_topics": strong_topics,
            "developing_topics": developing_topics,
            "revision_topics": revision_topics,
            "limited_evidence_topics": limited_evidence_topics,
            "misconception_patterns": misconception_patterns,
            "actionable_recommendations": actionable_recommendations,
            "follow_up_practice": follow_up_practice
        }
