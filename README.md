# s3g - A Simple Static Site Generator

A robust Python-based tool designed to transform Markdown files into a complete, static HTML website. This project was built as part of the Boot.dev curriculum to explore concepts in file I/O, recursion, and string manipulation.

## Overview

This generator automates the process of building a website from structured content. It features a custom-built Markdown-to-HTML parser and a recursive directory synchronization system to handle static assets.

### Key Features
- Markdown Parsing: Supports headers, bold text, italics, lists, links, and images.
- Recursive Static Copying: Automatically mirrors the structure of a `static` directory to a configurable `docs` directory.
- Template Injection: Injects generated HTML into a base layout for consistent site-wide branding.
- Automated Builds: Includes a shell script to clean, build, and deploy the site in one command.

## Getting Started

### Prerequisites
- Python 3.x installed on your system.

### Installation
Clone the repository:
`git clone https://github.com/wijits36/s3g`
`cd s3g`

### Running the Generator
To build the site and generate the static files in the `/docs` directory, run:
`./main.sh`

### Viewing the Site
You can view your generated site using Python's built-in HTTP server:
`cd docs`
`python3 -m http.server 8888`

Then, navigate to http://localhost:8888 in your web browser.

## Project Structure
- src/: The Python source code, including the HTML and Markdown logic.
- static/: Raw assets such as CSS files and images.
- content/: The source Markdown files used to build the site's pages.
- docs/: The destination for the final generated HTML output.
- template.html: The base HTML template used to wrap your content.

## Technical Details
This project demonstrates the use of:
- Regular Expressions: For complex string patterns in Markdown.
- Recursion: For walking through directory trees.
- Unit Testing: To ensure the reliability of the parsing logic.

## License
MIT
