class SkillAnalyzer:
    """
    Analisa habilidades técnicas do usuário com base em métricas do GitHub.
    A análise fica mais robusta e menos superficial.
    """

    def analyze(self, data):
        languages = data["languages"]
        repos = data["repos"]              # lista completa dos repositórios
        commit_activity = data["activity"] # commits por semana
        total_repos = len(repos)

        language_score = self.score_languages(languages)
        activity_score = self.score_activity(commit_activity)
        project_score = self.score_projects(repos)

        final_score = (language_score * 0.4) + (activity_score * 0.3) + (project_score * 0.3)

        return {
            "main_languages": self.get_main_languages(languages),
            "activity_score": activity_score,
            "project_score": project_score,
            "language_score": language_score,
            "total_repos": total_repos,
            "final_skill_level": self.map_score_to_level(final_score),
            "final_score": round(final_score, 2),
        }

    # -----------------------------
    # MÉTRICAS DE ANÁLISE
    # -----------------------------

    def score_languages(self, languages):
        """Avalia variedade e profundidade em linguagens."""
        total_languages = len(languages)
        top_usage = sum(languages.values())
        if top_usage == 0: return 0
        
        diversity_factor = min(total_languages / 5, 1)  # max 5 linguagens importa

        depth_factor = max(languages.values()) / top_usage

        return (0.6 * depth_factor + 0.4 * diversity_factor) * 10


    def score_activity(self, commit_activity):
        """Avalia consistência de commits ao longo do tempo."""
        if not commit_activity:
            return 0
        
        weekly_commits = commit_activity[-12:]  # últimas 12 semanas
        avg_commits = sum(weekly_commits) / len(weekly_commits)
        active_weeks = len([w for w in weekly_commits if w > 0])

        commit_score = min(avg_commits / 10, 1)  # normaliza
        consistency = active_weeks / len(weekly_commits)

        return (0.6 * consistency + 0.4 * commit_score) * 10


    def score_projects(self, repos):
        """Avalia qualidade dos projetos."""
        if not repos:
            return 0

        score = 0
        for r in repos:
            size = r.get("size", 0)
            issues = r.get("open_issues_count", 0)
            has_readme = r.get("has_readme", False)
            has_tests = r.get("has_tests", False)

            project_score = 0
            if size > 200:
                project_score += 0.4
            if has_readme:
                project_score += 0.2
            if has_tests:
                project_score += 0.3
            if issues > 1:
                project_score += 0.1

            score += project_score

        return min(score / len(repos), 1) * 10


    # -----------------------------
    # SUPORTE
    # -----------------------------

    def get_main_languages(self, languages):
        return sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]

    def map_score_to_level(self, score):
        if score <= 3:
            return "Iniciante"
        elif score <= 6.5:
            return "Intermediário"
        else:
            return "Avançado"