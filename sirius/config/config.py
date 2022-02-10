import typing as t
from collections import defaultdict
from pathlib import Path

import atoml
import attr
import desert
import marshmallow

from sirius.errors import CfgLoadError

DEFAULT_CONFIG_FILENAME = "sirius.toml"
DEFAULT_CONFIG_FILE_PATH = Path.cwd() / DEFAULT_CONFIG_FILENAME


@attr.s(auto_attribs=True, slots=True)
class DeveloperConfig:
    """Sirius developer configurations."""

    port: int = attr.ib(
        default=8080,
        metadata={
            "description": "Bind socket to this port."
        },
    )
    host: str = attr.ib(
        default="127.0.0.1",
        metadata={
            "description": "Bind socket to this host."
        },
    )
    reload: bool = attr.ib(
        default=False,
        metadata={
            "description": "Enable auto-reload."
        },
    )
    debug: bool = attr.ib(
        default=False,
        metadata={
            "description": "Enable debug mode."
        },
    )


@attr.s(auto_attribs=True, slots=True)
class Cfg:
    """Base configuration attrs class."""

    dev: DeveloperConfig = DeveloperConfig()


# build configuration
ConfigurationSchema = desert.schema_class(Cfg, meta={"ordered": True})  # noqa: N818


@attr.s(auto_attribs=True, slots=True, kw_only=True)
class Config:
    """
    Base configuration variable. Used across the entire application for configuration variables.

    - Holds two variables, default and user.
    - Default is a Cfg instance with nothing passed. It is a default instance of Cfg.
    - User is a Cfg schema instance, generated from a combination of the defaults, user provided toml/yaml.
    """

    user: Cfg
    schema: marshmallow.Schema
    default: Cfg = Cfg()


def load_toml(path) -> defaultdict:
    """Load a configuration dictionary from the specified toml file."""
    path = Path(path)

    if not path.is_file():
        raise CfgLoadError("The provided toml file path is not a valid file.")

    try:
        with open(path) as f:
            return defaultdict(lambda: marshmallow.missing, atoml.parse(f.read()).value)
    except Exception as e:
        raise CfgLoadError from e


DictT = t.TypeVar("DictT", bound=t.Dict[str, t.Any])


def _remove_extra_values(klass: type, dit: DictT) -> DictT:
    """
    Remove extra values from the provided dict which don't fit into the provided klass recursively.
    klass must be an attr.s class.
    """
    fields = attr.fields_dict(klass)
    cleared_dict = dit.copy()
    for k in dit:
        if k not in fields:
            del cleared_dict[k]
        elif isinstance(cleared_dict[k], dict):
            if attr.has((new_klass := fields.get(k, None)).type):
                cleared_dict[k] = _remove_extra_values(new_klass.type, cleared_dict[k])
            else:
                # delete this dict
                del cleared_dict[k]
    return cleared_dict


_CACHED_CONFIG: "Config" = None
_DEFAULT_CACHED_CONFIG: Cfg = Cfg()


def _load_config(file: Path) -> Config:
    """Loads a configuration from the specified file."""
    loaded_config_dict = load_toml(file)

    # HACK remove extra keeps from the configuration dict since marshmallow doesn't know what to do with them
    # CONTRARY to the marshmallow.EXCLUDE below.
    # They will cause errors.
    # Extra configuration values are okay, we aren't trying to be strict here.
    loaded_config_dict = _remove_extra_values(Cfg, loaded_config_dict)

    loaded_config_dict = ConfigurationSchema().load(
        data=loaded_config_dict, unknown=marshmallow.EXCLUDE
    )
    return Config(
        user=loaded_config_dict,
        schema=ConfigurationSchema,
        default=_DEFAULT_CACHED_CONFIG,
    )


def update_config(file: t.Optional[Path] = DEFAULT_CONFIG_FILE_PATH) -> None:
    global _CACHED_CONFIG
    _CACHED_CONFIG = _load_config(file)


def get_config() -> Config:
    return _CACHED_CONFIG
