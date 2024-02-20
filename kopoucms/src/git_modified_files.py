import os

import git


def get_modified_directories():
    """
    Get the list of modified directories from the last commit in Git.

    Returns:
      list: List of modified directories.
    """

    repo = git.Repo(os.getcwd(), search_parent_directories=True)
    print(repo.working_dir)
    commit = repo.head.commit

    print(commit.message)
    modified_directories = set()
    for diff in repo.index.diff(None):
        print(diff.change_type, diff.a_path)
        if diff.change_type == "M" or diff.change_type == "A":
            modified_directories.add(diff.a_path)

    return list(modified_directories)


# modified_directories = get_modified_directories()
# print("Modified directories in last commit:", modified_directories)


def get_current_path():
    cwd = os.getcwd()
    repo = git.Repo(cwd, search_parent_directories=True)
    print(repo.working_dir)

    if cwd.startswith(repo.working_dir):
        return cwd[len(repo.working_dir) + 1 :]


print(get_current_path())
