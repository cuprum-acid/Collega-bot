# Run in Docker 🐳

- Add bot API key
- `docker build -t collega-image .`
- `docker run -d --name collega-conatiner collega-image`

## Add a new meme

- place it to an existing folder in `res/images` or specify sticker pack name
- create your category: the class must have `chance: int` and `memes: Sized`