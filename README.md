# SAVBasics
Some Python-based utilities for converting and signing save files for the 2002 *Spider-Man* video game.
See "EXAMPLES.md" for showcase screenshots and the text of a single save slot represented as JSON.

## Features
- Convert binary ".sav" files to text ".json" files to view/edit, complete with sensible categorisation and variable labelling.
- Convert text ".json" files back to binary ".sav" files to alter in-game progress/status.
- Sign binary ".sav" files with a game version-appropriate signature so that the save data will pass validation - either pick from a list of known version signatures or specify a custom one.
- Includes user/program error handling and notification.
- Includes program documentation as well as ".sav"/".json" format documentation.
- User-facing utility scripts can be run in either console input mode (user-friendly) or command line mode (automation-friendly).
- Made in Python 3; cross-platform and dependant upon only the included modules in addition to the "json", "os", "struct" and "sys" standard library modules.
- Free for anyone to reuse/redistribute however; I may continue to update this branch if I have reason to/have time, but I can only do so much.
- Currently only offers direct support for Windows save files.

## User-facing utility scripts
- **Convert:** Converts save files between the two supported formats (SAV/JSON).
- **Sign:** Alters the signature of a given SAV file - either by selected preset or custom entry.

## Usage guide
- A Python 3 interpreter is required, see [python.org](https://python.org/downloads).
- Download this repository/release. You might need to unzip it using appropriate software.
- The two MD files are documentation for those interested.
- The two PY files named Convert and Sign are the user-facing utilities listed prior.
- The PY files in the Modules directory provide functions for the utility scripts to call. These files should not be edited or deleted under normal circumstances.
- Both utilities run in console input mode by default - for instance when you double-click the scripts in a file manager in many setups. Follow the on-screen instructions.
- Both utilities can be run in command line mode. Convert requires four parameters: conversion mode ("PC_SAV_TO_JSON" or "JSON_TO_PC_SAV"), input file path, output file path and endianness (0 for little-endian, 1 for big-endian). Sign requires three parameters: input file path, signature type (either a known preset such as "WINDOWS/1.3" or a custom eight-character string such as "00:00:00") and endianness (0 for little-endian, 1 for big-endian).

## Error notices
| Error | Description |
| ----- | ----------- |
| Module import unsuccessful - [].py. | Required functionality modules failed to import. Check that the contents of the Modules directory have not been deleted or corrupted, and that the required standard library modules are present within your setup.
| Unworkable answer. | Answer to console input mode prompt was invalid, try again.
| On input. | Input file could not be opened or dumped. Check the file path is correct and that the file is accessible to other programs.
| On inter-format conversion. | Conversion process failure. Ensure the correct file types and data layouts are used - for example, an incorrectly formatted JSON file with a comma missing will raise this error. Ensure that numeric values are not set too high or too low.
| On sign. | Failed to process the input SAV file and sign it. Ensure the correct file type/layout is given as input. Ensure the input signature is a supported preset or composed of eight ASCII/compatible characters.
| On output. | Unable to save the output file at the given destination - check that the target directory exists and that write permissions are not denied.
| Bad input conversion action. | Internal safety check, shouldn't raise.
| Bad conversion conversion action. | Internal safety check, shouldn't raise.
| Bad output conversion action. | Internal safety check, shouldn't raise.
