# Conservative Q-Learning (CQL) Implementation

This repository contains an implementation of Conservative Q-Learning (CQL), developed as part of the Reinforcement Learning course (CAS4160). CQL is a cutting-edge algorithm for offline reinforcement learning that effectively learns from static datasets without requiring direct environment interaction. The implementation focuses on a Pointmass navigation environment with varying difficulty levels.

*Note: This codebase builds upon the foundational work provided by the CAS4160 teaching staff. All original contributions and materials are properly credited to their respective authors.*

## Project Overview

The implementation includes:
- Multiple difficulty levels of Pointmass environments (Easy, Medium, Hard, Very Hard)
- CQL agent implementation with configurable hyperparameters
- Training infrastructure with support for offline learning
- Performance evaluation and logging tools

## Setup


Then, run the following commands when you're under the `cql-rl/` folder:

```
conda activate [your_env]
pip install swig
pip install -r requirements.txt
pip install -e .
```

## Usage

To train a CQL agent, use the script `cas4160/scripts/run_cql.py` with various configuration options:

```bash
python cas4160/scripts/run_cql.py --env_name [PointmassEasy-v0/PointmassMedium-v0/PointmassHard-v0/PointmassVeryHard-v0] --exp_name [experiment_name]
```

Key parameters:
- `--env_name`: Choose environment difficulty
- `--cql_alpha`: CQL regularization parameter
- `--batch_size`: Training batch size
- `--dataset_size`: Size of the offline dataset


