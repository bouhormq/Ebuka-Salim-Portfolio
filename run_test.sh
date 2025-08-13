#!/bin/bash

# Run tests inside a temporary Docker container
docker compose -f docker-compose.prod.yml run --rm -e TESTING=true myportfolio python -m unittest discover -v tests/