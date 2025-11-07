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
    @{{minio}} mb myminio/laboratorio-do-lyc

minio-public-bucket:
    @{{minio}} anonymous set download myminio/laboratorio-do-lyc

minio-setup: minio-alias minio-mb minio-public-bucket

get-bootstrap:
    @curl --create-dirs -o laboratoriodolyc/static/css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css
    @curl --create-dirs -o laboratoriodolyc/static/js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/js/bootstrap.bundle.min.js

get-prism:
    @curl --create-dirs -o laboratoriodolyc/static/js/prism.min.js https://cdn.jsdelivr.net/npm/prismjs@1.30/prism.min.js
    @curl --create-dirs -o laboratoriodolyc/static/css/prism-coy.min.css https://cdn.jsdelivr.net/npm/prismjs@1.30/themes/prism-coy.min.css
