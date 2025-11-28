class RolePerm:
    def __init__(self, role: str, perms: list):
        self.role = role
        self.perms = perms

    def has(self, perm: str):
        return perm in self.perms