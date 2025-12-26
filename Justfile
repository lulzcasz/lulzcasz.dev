export UV_ENV_FILE := ".env"

compose := "docker compose"
manage := "uv run manage.py"
minio := "docker compose exec -it storage mc"

compose *args:
    @{{compose}}

compose-up:
    @{{compose}} up -w

compose-down:
    @{{compose}} down --rmi local

manage *args:
    @{{manage}} {{args}}
    
migrate *args:
    @{{manage}} migrate {{args}}

minio-alias:
    @{{minio}} alias set myminio http://localhost:9000 minioadmin minioadmin

minio-mb:
    @{{minio}} mb myminio/lulzcasz

minio-public-bucket:
    @{{minio}} anonymous set download myminio/lulzcasz

minio-setup: minio-alias minio-mb minio-public-bucket

get-bootstrap:
    @curl --create-dirs -o lulzcasz/static/css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css
    @curl --create-dirs -o lulzcasz/static/js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/js/bootstrap.bundle.min.js

get-prism:
    @curl --create-dirs -o lulzcasz/static/js/prism.min.js https://cdn.jsdelivr.net/npm/prismjs@1.30/prism.min.js
    @curl --create-dirs -o lulzcasz/static/css/prism-coy-without-shadows.min.css https://cdn.jsdelivr.net/npm/prism-themes@1.9/themes/prism-coy-without-shadows.min.css
    @curl --create-dirs -o lulzcasz/static/js/prism-autoloader.min.js https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/autoloader/prism-autoloader.min.js
    @curl --create-dirs -o lulzcasz/static/js/prism-toolbar.min.js https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/toolbar/prism-toolbar.min.js
    @curl --create-dirs -o lulzcasz/static/css/prism-toolbar.min.css https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/toolbar/prism-toolbar.min.css
    @curl --create-dirs -o lulzcasz/static/css/prism-treeview.min.css https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/treeview/prism-treeview.min.css
    @curl --create-dirs -o lulzcasz/static/js/prism-treeview.min.js https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/treeview/prism-treeview.min.js
    @curl --create-dirs -o lulzcasz/static/js/prism-line-numbers.min.js https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/line-numbers/prism-line-numbers.min.js
    @curl --create-dirs -o lulzcasz/static/css/prism-line-numbers.min.css https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/line-numbers/prism-line-numbers.min.css
    @curl --create-dirs -o lulzcasz/static/js/prism-command-line.min.js https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/command-line/prism-command-line.min.js
    @curl --create-dirs -o lulzcasz/static/css/prism-command-line.min.css https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/command-line/prism-command-line.min.css
    @curl --create-dirs -o lulzcasz/static/js/prism-diff-highlight.min.js https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/diff-highlight/prism-diff-highlight.min.js
    @curl --create-dirs -o lulzcasz/static/css/prism-diff-highlight.min.css https://cdn.jsdelivr.net/npm/prismjs@1.30/plugins/diff-highlight/prism-diff-highlight.min.css

get-font-awesome:
    @curl --create-dirs -o lulzcasz/static/css/all.min.css https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@7.1/css/all.min.css
    @curl --create-dirs -o lulzcasz/static/webfonts/fa-solid-900.woff2 https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@7.1/webfonts/fa-solid-900.woff2
    @curl --create-dirs -o lulzcasz/static/webfonts/fa-brands-400.woff2 https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@7.1.0/webfonts/fa-brands-400.woff2
