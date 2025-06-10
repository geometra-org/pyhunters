# PyHunters Commitizen Customization Information

## Changelog Patterns

### Tag Pattern

> *MAJOR.MINOR.PATCH*

Ex:
* 1.2.3

### Commit Message Translation

Commit messages take the form of...

> *"^(?:breaking\\|)?(feat|refactor|fix|tests|chore): (\\s.*)"*

The `breaking|` prefix indicates a breaking change and forces an increment of the MAJOR version. All other prefixes increment increment either the MINOR or PATCH version.

* `feat` (MINOR): New feature
* `refactor` (MINOR): Code refactoring
* `fix` (PATCH): Bug fix
* `tests` (PATCH): Test changes
* `chore` (PATCH): Other changes

See below how a starting tag of `1.0.0` would be incremented...

Ex:
* `feature: I'm adding a new feature and it's neat` -> 1.1.0
* `bugfix: I'm fixing a bug and it's important` -> 1.0.1
* `breaking|feature: I'm adding a new feature but it's breaking` -> 2.0.0
