from datetime import datetime, timezone
import json
from typing import List

from app.db.redis import RedisService
from app.services.quiz import QuizService
from sqlalchemy.ext.asyncio import AsyncSession

TTL_SECONDS = 48 * 60 * 60


class QuizResultRedisService:
    def __init__(self, db: AsyncSession, redis: RedisService):
        self.redis = redis
        self.quiz_service = QuizService(db)

    async def save_user_answers(
        self,
        user_id: int,
        company_id: int,
        quiz_id: int,
        question_answers: list[dict],
        correct_answers_map: dict[int, list[int]],
    ):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

        answers_data = []
        for item in question_answers:
            question_id = item["question_id"]
            selected = item["answers"]
            correct = correct_answers_map.get(question_id, [])

            answers_data.append(
                {
                    "question_id": question_id,
                    "answers": [
                        {"id": i, "is_correct": i in correct} for i in selected
                    ],
                }
            )

        value = {
            "user_id": user_id,
            "company_id": company_id,
            "quiz_id": quiz_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "answers": answers_data,
        }

        key = f"quiz_response:{user_id}:{quiz_id}:{timestamp}"

        await self.redis.setex(key, TTL_SECONDS, json.dumps(value))

    async def get_quiz_attempts(self, user_id: int, quiz_id: int) -> List[dict]:
        pattern = f"quiz_response:{user_id}:{quiz_id}:*"
        keys = await self.redis.keys(pattern)

        results = []
        for key in keys:
            raw = await self.redis.get(key)
            if raw:
                try:
                    results.append(json.loads(raw))
                except json.JSONDecodeError:
                    continue

        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return results

    async def get_quiz_attempts_with_text(
        self, user_id: int, quiz_id: int
    ) -> List[dict]:
        attempts = await self.get_quiz_attempts(user_id, quiz_id)
        quiz_data = await self.quiz_service.get_quiz_by_id(quiz_id)

        question_map = {
            question.id: {
                "title": question.title,
                "options": {opt.id: opt.text for opt in question.answer_options},
            }
            for question in quiz_data.questions
        }

        enriched = []
        for attempt in attempts:
            enriched_answers = []
            for answer in attempt["answers"]:
                question_data = question_map.get(answer["question_id"], {})
                selected_answers = answer["answers"]
                selected_answers_with_text = [
                    {
                        **i,
                        "answer_option_text": question_data.get("options", {}).get(
                            i["id"], ""
                        ),
                    }
                    for i in selected_answers
                ]

                enriched_answers.append(
                    {
                        "question_id": answer["question_id"],
                        "question_title": question_data.get("title", ""),
                        "selected_answers": selected_answers_with_text,
                    }
                )

            enriched.append(
                {
                    "timestamp": attempt["timestamp"],
                    "quiz_title": quiz_data.title,
                    "quiz_description": quiz_data.description,
                    "user_id": user_id,
                    "answers": enriched_answers,
                }
            )

        return enriched
