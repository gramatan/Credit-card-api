import yaml
import os

if __name__ == '__main__':
    if not os.path.exists("docs"):
        os.mkdir("docs")

    from main_auth import app
    with open("docs/cc_auth.yaml", "w", encoding="utf-8") as f:
        yaml.dump(app.openapi(), f, allow_unicode=True)

    from main_balance import app
    with open("docs/cc_balance.yaml", "w", encoding="utf-8") as f:
        yaml.dump(app.openapi(), f, allow_unicode=True)
