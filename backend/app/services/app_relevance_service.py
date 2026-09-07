import re


class AppRelevanceService:

    def normalize_text(self, text: str) -> str:

        if not text:
            return ""

        return text.lower().strip()

    def tokenize(self, text: str) -> set[str]:

        normalized_text = self.normalize_text(text)

        return set(re.findall(r"\b[a-z0-9]+\b", normalized_text))

    def calculate_relevance(
        self,
        keyword: str,
        app: dict,
    ) -> dict:

        normalized_keyword = self.normalize_text(keyword)

        keyword_tokens = self.tokenize(keyword)

        title = self.normalize_text(app.get("title"))

        description = self.normalize_text(app.get("description"))

        category = self.normalize_text(app.get("category"))

        # --------------------------------
        # Tokenize app data
        # --------------------------------

        title_tokens = self.tokenize(title)

        description_tokens = self.tokenize(description)

        category_tokens = self.tokenize(category)

        # --------------------------------
        # Score calculation
        # --------------------------------

        score = 0

        # Exact keyword in title

        if normalized_keyword in title:

            score += 0.6

        # Keyword tokens found in title

        title_matches = keyword_tokens & title_tokens

        if keyword_tokens:

            score += (len(title_matches) / len(keyword_tokens)) * 0.3

        # Keyword tokens found in description

        description_matches = keyword_tokens & description_tokens

        if keyword_tokens:

            score += (len(description_matches) / len(keyword_tokens)) * 0.1

        # Exact keyword in description

        if normalized_keyword in description:

            score += 0.2

        # Cap score

        score = min(score, 1.0)

        return {
            "app_id": app.get("app_id"),
            "title": app.get("title"),
            "relevance_score": round(score, 3),
            "is_relevant": score >= 0.4,
            "title_matches": list(title_matches),
            "description_matches": list(description_matches),
        }

    def filter_relevant_apps(
        self,
        keyword: str,
        apps: list[dict],
    ) -> list[dict]:

        relevant_apps = []

        for app in apps:

            relevance = self.calculate_relevance(
                keyword=keyword,
                app=app,
            )

            if relevance["is_relevant"]:

                app["relevance_score"] = relevance["relevance_score"]

                relevant_apps.append(app)

        return sorted(
            relevant_apps,
            key=lambda app: app.get(
                "relevance_score",
                0,
            ),
            reverse=True,
        )
