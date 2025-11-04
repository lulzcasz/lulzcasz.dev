export UV_ENV_FILE := ".env"

compose := "docker compose"
manage := "uv run manage.py"

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
