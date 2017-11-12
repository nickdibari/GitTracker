import uuid


class Dev(object):
    """
    Representation of a developer in a project repository
    @username: Developer username
    @avatar: URL of account profile picture
    @commits: Number of commits account has in the repository
    """

    def __init__(self, username, avatar_url):
        self.username = username
        self.avatar_url = avatar_url

        # Instances created on first commit sight
        self.commits = 1

        # For keeping track of same account in different repos
        self.hash = uuid.uuid4()

    def __str__(self):
        return '{}: {}'.format(self.username, self.commits)

    def __repr__(self):
        return str(self.hash)
