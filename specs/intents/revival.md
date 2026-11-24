# Revival

I have not worked on this project for a while.

The goal of this project is to build a simple http web service using python to expose an envionment variable. I would like to evolve this design and include several best practices that I have been using more often lately.

I would like to:

* Integrate Infisical for the secret management aspect of this project, including performing secret rotation
* I would like to leverage Renovate Self Hosted mechanism for continous update of dependencies for all involve ecosystem: github-action, Dockerfile, docker-compose, pre-commit, python (uv)
* I would like to automate using semantic versionning the release process of this project
* All github action workflow need to be local to this project (stop using reusable workflow)

This project will become a canary test bed for my AI SDLC, the content does not need to be complexe but the fondation need to be stable.

Finally, I will deploy two version of this project:

* One in my local environment (*.local.mighty-muffin.io) as my STAGING env. expose to my local network only
* One via a cloudflare-tunnerl (env.mighty-muffin.io) as my PROD env. exposed to the whole internet

## Project structure

The README.md at the root of the repo needs to be a short getting started guide helping people jump in this project.

The `docs/` directory will contains all more complexe project documentation in details explaining each component.

The `specs/` directory will be used by agent for spec-driven-developpment and other agents related activities.
