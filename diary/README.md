It should be pretty easy to get started with this if you need to reclone the repo.

Once you've cloned the repo, you can just run `gen_today.py` and it'll make the `entries` directory if it doesn't exist, make the file for today's entry, and open it if a supported editor is available.

`_generate_html.sh` should also be good to use without the old entries, but `copy_to_ftp.sh` will remove entries from the web mirror if they don't exist locally so you should make sure to copy the old entries into the `entries` folder first before running `copy_to_ftp.sh`.

In terms of dependencies, you'll need:
- The `markdown` library for python3, just run `pip3 install markdown` or whatever.
- `lftp`, get it with `brew` or `apt-get`.

You'll also want to copy the `github-markdown.css` from the root into `generated_html/` after you've run `_generate_html.sh` or `copy_to_ftp.sh` for the first time.
