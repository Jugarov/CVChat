from agent import CVAgent

class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, cv_id, summary, namespace, is_default=False):
        self.agents[cv_id] = {
            "agent": CVAgent(cv_id, namespace),
            "summary": summary,
            "is_default": is_default
        }

    def get_default(self):
        for cv_id, data in self.agents.items():
            if data["is_default"]:
                return cv_id
        return None

    def list(self):
        return list(self.agents.keys())

    def get(self, cv_id):
        return self.agents[cv_id]["agent"]
