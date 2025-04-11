import os.path

from aiohttp.web import run_app

from data_service.web.app import setup_app

if __name__ == "__main__":
    run_app(
        setup_app(
            config_path=os.path.join(
                os.path.dirname(os.path.relpath(__file__)), "config.yaml"
            )
        )
    )
