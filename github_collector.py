import requests # type:ignore

class GitHubCollector:
    def __init__(self, username):
        self.username = username
        self.base_url = f"https://api.github.com/users/{username}"

    def get_repos(self):
        url = f"{self.base_url}/repos"
        r = requests.get(url)
        return r.json()

    def get_languages(self):
        repos = self.get_repos()
        languages = {}
        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        return languages

    def get_commit_activity(self, repo_name):
        """Retorna commits semanais para cada repo."""
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/stats/commit_activity"
        r = requests.get(url)
        data = r.json()

        # Quando a API estiver processando, ela retorna None
        if not data or not isinstance(data, list):
            return []

        # Extrai apenas o número de commits semanais
        return [week["total"] for week in data]

    def extract_repo_details(self, repo):
        """Extrai dados importantes para análise qualitativa de cada repo."""
        return {
            "name": repo.get("name"),
            "size": repo.get("size", 0),  # tamanho do repositório
            "open_issues_count": repo.get("open_issues_count", 0),
            "has_readme": repo.get("has_downloads", False),  # aproximado
            "has_tests": any("test" in repo.get("name", "").lower() for _ in range(1)),  # heurística
        }

    def collect_profile_data(self):
        repos = self.get_repos()

        detailed_repos = [self.extract_repo_details(r) for r in repos]

        # Somar atividades semanais de todos os repositórios
        activity = []
        for r in repos:
            weekly = self.get_commit_activity(r["name"])
            if weekly:
                activity.append(weekly)

        # Achatar: soma commits de todos os repos por semana
        combined_activity = []
        if activity:
            weeks = zip(*activity)
            combined_activity = [sum(week) for week in weeks]

        return {
            "languages": self.get_languages(),
            "repos": detailed_repos,
            "activity": combined_activity,
        }