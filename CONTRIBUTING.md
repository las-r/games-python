# Contributing
Thanks for contributing to **Small Games Python**!

This repository is a collection of **small Python games and remakes**, so please keep contributions simple and follow the guidelines below.

## Game Requirements
Games must follow the definition of **small** used in this repository:

* A game may require **no more than 3 files**
* Extra files should only exist when necessary (for example: word lists or small data files)

Try to keep the code **simple, readable, and self-contained**.

## Interfaces
Games are organized by **interface**.
Place your game in the correct directory.

Examples include:
* `cli` – terminal / command-line games
* `pygame` – games using pygame
* `arcade` – games using the arcade library

If your game uses a new interface that doesn't exist yet, or isn't listed in the repository, you may create an issue for it.

## Naming
* Use **lowercase filenames**, words separated by underscores if needed.
* Prefer **descriptive names**

Example:
```
cli/hangman.py
pygame/snake.py
pygame/lights_out.py
```

## Dependencies
Try to **avoid unnecessary dependencies**.

If your game requires an external library (such as pygame), it should:
* **Be clear from the folder it is placed in**
* **Be common and easy to install**
* **Be listed in a comment if needed**

## Code Style
There are **no strict formatting requirements**, but please try to:

* Write readable code
* Add comments when useful
* Avoid extremely large or complex programs

**Remember: these are meant to be small games.**

## Submitting
1. Fork the repository
2. Add your game in the **correct interface folder**
3. Open a pull request with a **short description of the game**, preferably including:
   * a basic summary
   * controls
   * and whether it's original or not

## License
By contributing, you agree that your code will be released under the MIT license.

If you have ideas for improving the repository structure, feel free to suggest them in an issue.
