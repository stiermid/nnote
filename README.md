# nnote

[![PyPI downloads](https://img.shields.io/pypi/dm/nnote.svg)](https://pypi.org/project/nnote/)
[![Github commits (since latest release)](https://img.shields.io/github/commits-since/stiermid/nnote/latest.svg)](https://github.com/stiermid/nnote)

<a href="https://repology.org/project/nnote/related">
	<img src="https://repology.org/badge/vertical-allrepos/nnote.svg" alt="Packaging status" align="right">
</a>

A plain, file-based note-taking CLI.

## Installation

**Arch Linux (AUR)**

```bash
yay -S nnote
```

Or with any other AUR helper, or manually via `makepkg`.

**From source**

```bash
pip install -e .
```

## Setup

```bash
nnote init
```

Prompts for a notes directory (default: `~/nnotes`) and a default editor. Config is saved to `~/.config/nnote/config.yaml`. If `$EDITOR` is set in your environment, it will be used as the editor default.

## Documentation

Full documentation is published at [stiermid.github.io/nnote](https://stiermid.github.io/nnote/).

## License

This project is licensed under the GNU General Public License v3.0 or later. See [LICENSE](LICENSE) for details.
