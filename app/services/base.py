# app/services/base_service.py
import uuid
from slugify import slugify


class BaseService:
    async def _generate_unique_slug(
        self, name: str, repo, slug_field: str = "slug", max_attempts: int = 100
    ) -> str:
        """
        Генерує унікальний slug для будь-якої моделі.

        repo — репозиторій, що має метод `find_one(**kwargs)`
        slug_field — ім'я поля slug у моделі
        max_attempts — максимальна кількість спроб для уникнення колізій
        """
        base_slug = slugify(name.strip().lower())
        slug = base_slug
        counter = 1

        while await repo.find_one(**{slug_field: slug}):
            slug = f"{base_slug}-{counter}"
            counter += 1
            if counter > max_attempts:
                # Альтернатива: можна використовувати uuid замість exception
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
                break

        return slug
