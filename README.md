# UPSC Question Bank

A high-quality collection of UPSC practice questions with detailed research, explanations, and insights.

## Project Structure

- `frontend/`: React + Vite + Tailwind CSS source code for the web application.
- `docs/`: Built static site for GitHub Pages (auto-generated from `build.sh`).
- `<subject_folder>/`: Contains the raw questions, split markdown files, and generated JSON files for each subject.
  - `input/`: The original source markdown file.
  - `questions/`: Split markdown files (one per question).
  - `json/`: LLM-generated JSON files containing text, options, answer, and research.
- `prompts/`: System prompts used for generating the JSON files.

## How to Add New Questions

1. Create a new folder for the subject (e.g., `polity_1`).
2. Add your questions to `polity_1/input/questions.md`.
3. Use the `splitter.py` script to split the input file into individual markdown files in `polity_1/questions/`.
4. Run your LLM processing script (e.g., `main.py` or similar) to generate the JSON files in `polity_1/json/`.
5. Run `./build.sh` to update the web application data and rebuild the site.

## Development

To run the frontend in development mode:

```bash
cd frontend
npm run dev
```

To build and update the static site:

```bash
./build.sh
```

## Deployment

The site is designed to be hosted on **GitHub Pages**. To deploy:

1. Push all changes to GitHub (including the `docs/` folder).
2. In your GitHub repository settings, go to **Pages**.
3. Under **Build and deployment**, set the source to **Deploy from a branch**.
4. Select your main branch and the folder as **`/docs`**.
5. Save, and your site will be live!
