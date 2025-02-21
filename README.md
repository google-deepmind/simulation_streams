# simulation_streams

[Simulation Streams Tech Report](https://arxiv.org/abs/2501.18668)

A development platform for simulations with large language models.
It comes with an Entity-Component-Systems approach and graphical editor.

The platform is a flask app most easily used locally in a venv,
which can be started with source setup.sh (on linux). This sets up all
dependencies and ends with instructions for the different commands for
launching the editor or command line running. The editor is displayed in a
browser.

A library of simulation configs can be found under configs,
including a market economy, a social simulation and 6 tasks from
the classical reinforcement learning literature.

## Usage examples

1 **source setup.sh**

2a **To create the local server that runs the web app:**

    ```
    python app.py configs/social_catch_game.py --metrics=configs/metrics_social_catch_game.txt --web --model='gemini-2.0-flash-exp' --api_key='your_key'
    ```

2b **To run a number of steps from the command line and return the metrics:**

    ```
    python app.py configs/social_catch_game.py --metrics=configs/metrics_social_catch_game.txt --steps=10 --model='gemini-2.0-flash-exp' --api_key='your_key'
    ```

2c **To open the editor with an empty config:**

    ```
    python app.py --web --model='gemini-2.0-flash-exp' --api_key='your_key'
    ```

2d **To use the generic code_world config with task-specific functions:**

    ```
    python app.py configs/code_world.py --web --model='gemini-2.0-pro-exp' --api_key='your_key' --task_name='maze'
    ```

This example demonstrates using the generic code_world configuration to run
a maze task. The task_name parameter imports task-specific functions from
the corresponding Python module, allowing you to implement custom
environments in pure Python while leveraging the simulation streams
framework.

## Citing Simulation Streams

If you use Simulation Streams in your work,
please cite the accompanying article:

```
@article{sunehag2025simulation,
  title={Simulation Streams: A Programming Paradigm for Controlling Large Language Models and Building Complex Systems with Generative AI.},
  author={Sunehag, Peter and Leibo, Joel Z},
  journal={arXiv preprint arXiv:2501.18668},
  year={2025}
}
```

## Disclaimer

This is not an officially supported Google product.
