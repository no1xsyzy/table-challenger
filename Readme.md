Table Challenge
====

Browser-based Gomoku arena.

How-To Use
----

```bash
cd fe-svelte
yarn
yarn dev &
cd ..
cd be-svelte
poetry install
poetry run uvicorn "table_challenge_be:app" --reload & 
```

Then open [http://localhost:3000](http://localhost:3000)
