from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TERMINALS",
    settings_files=['settings.yaml', '.secrets.yaml'],
)
