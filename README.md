# Run in Docker 🐳

- Add bot API key
- `docker build -t collega-image .`
- `docker run -d --name collega-conatiner collega-image`

## Add a new meme

- place it to existing folder in res/images
- or create your category: set weight in mem.py and description in get_category_text()