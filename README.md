# simulation_streams

A development platform for simulations with large language models.
It comes with an Entity-Component-Systems approach and graphical editor.

The platform is a flask app most easily used locally in a venv,
which can be started with source setup.sh (on linux). This sets up all
dependencies and ends with instructions for the different commands for
launching the editor or command line running. The editor is displayed in a
browser.

DO NOT SUBMIT

A library of simulation configs can be found under configs,
including a market economy, a social simulation and 6 tasks from
the classical reinforcement learning literature.

## Usage examples

1 **source setup.sh**

2a **To create the local server that runs the web app:**

    ```
    python app.py configs/social_catch_game.py --metrics=configs/metrics_social_catch_game.txt --web --model='gemini-2.0-flash-exp' --api_key='your_key'
    ```

2b **To run a number of steps on the command line and get the metrics returned:**

    ```
    python app.py configs/social_catch_game.py --metrics=configs/metrics_social_catch_game.txt --steps=10 --model='gemini-2.0-flash-exp' --api_key='your_key'
    ```

2c **To open the editor with an empty config:**

    ```
    python app.py --web --model='gemini-2.0-flash-exp' --api_key='your_key'
    ```

## Disclaimer

This is not an officially supported Google product.
