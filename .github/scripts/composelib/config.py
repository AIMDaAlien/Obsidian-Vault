"""Compose configuration: which vaults to merge and what never gets published."""
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Source:
    name: str
    path: Path
    machine: str
    syncthing_folder: str
    path_map: dict[str, str] = field(default_factory=dict)
    attachments: str | None = None


@dataclass(frozen=True)
class Config:
    published: Path
    sources: list[Source]
    protected: list[str]
    exclude_dirs: list[str]
    exclude_ext: list[str]
    image_ext: list[str]
    syncthing_api: str


def load_config(path: Path) -> Config:
    """Read compose.yml; relative paths resolve against its directory."""
    path = Path(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    base = path.parent
    sources = [
        Source(
            name=s["name"],
            path=base / s["path"],
            machine=s["machine"],
            syncthing_folder=s["syncthing_folder"],
            path_map=dict(s.get("path_map") or {}),
            attachments=s.get("attachments"),
        )
        for s in raw["sources"]
    ]
    return Config(
        published=base / raw["published"],
        sources=sources,
        protected=list(raw["protected"]),
        exclude_dirs=list(raw["exclude_dirs"]),
        exclude_ext=list(raw["exclude_ext"]),
        image_ext=list(raw["image_ext"]),
        syncthing_api=raw["syncthing_api"],
    )
