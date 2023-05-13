import dagger

import sys

import anyio




async def test():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        project = client.host().directory(".", exclude = [".venv", "ci", ".git"])

        # first stage
        python = (
            client.pipeline("test").container()
            .from_("python:3.10-slim")
            .with_exec(["apt", "update"])
            .with_exec(["apt", "install", "curl", "-y"])
        )
        python = await build_poetry(python)
        python = (
            python
            .with_directory("/project", project)
            .with_workdir("/project")
            .with_exec(["poetry", "config", "virtualenvs.create", "true", "--local"])
            .with_exec(["poetry", "config", "virtualenvs.in-project", "true", "--local"])
            .with_exec(["poetry", "install"])
            .with_exec(["./.venv/bin/pytest"])
            .with_exec(["./.venv/bin/ruff", "."])
        )
        
        out = await python.stdout()
        print(out)

        # python = (
        #     client.container()
        #     # pull container
        #     .from_("python:3.10-slim")
        #     .with_exec(["apt", "update"])
        #     #.with_exec(["apt", "upgrade"])
        #     .with_exec(["apt", "install", "curl", "-y"])
        #     #.with_exec(["echo", "hello"])
        #     # install poetry and add to PATH
        #     #.with_exec(["export", "POETRY_HOME=/opt/poetry"], skip_entrypoint=True)
        #     #.with_env_variable("POETRY_HOME", "/opt/poetry")
        #     #.with_exec(["curl", "-sSL", "https://install.python-poetry.org", "--output", "script.py"])
        #     #.with_exec(["python", "script.py", "--version", "1.3.2"])
        #     #.with_env_variable("PATH", "$PATH:$POETRY_HOME/bin")
        #     #.with_exec(["export", "PATH=$PATH:$POETRY_HOME/bin"])
        #     #.with_exec(["$POETRY_HOME/bin/poetry", "--version"])
        #     # .with_exec(["poetry", "config", "virtualenvs.create", "true"])
        #     # .with_exec(["poetry", "config", "virtualenvs.in-project", "true"])

        #     # add source files to container
        #     # .with_directory("/src", source)

        #     # # install dependencies
        #     #.with_exec(["poetry", "--version"])
        #     # .with_exec(["poetry", "install"])
        #     # # activate venv
        #     # .with_exec(["source", ".venv/bin/activate"])
        #     # # run linter
        #     # .with_exec(["ruff", "."])
        #     # # run tests
        #     # .with_exec(["pytest"])
        # )

        # execute
        

    

async def build_poetry(container: dagger.Container) -> dagger.Container:
    path_env_var = await container.env_variable("PATH")
    poetry_home_env_var = "/opt/poetry"
    poetry_script_path = "/script.py"
    poetry_version = "1.3.2"
    res_container = (
        container.with_env_variable("POETRY_HOME", poetry_home_env_var)
            .with_exec(["curl", "-sSL", "https://install.python-poetry.org", "--output", poetry_script_path])
            .with_exec(["python", poetry_script_path, "--version", poetry_version])
            .with_env_variable("PATH", f"{path_env_var}:{poetry_home_env_var}/bin")
    )
    return res_container

if __name__ == "__main__":
    anyio.run(test)