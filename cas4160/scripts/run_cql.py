import os
import time

from cas4160.infrastructure.rl_trainer import RL_Trainer
from cas4160.agents.cql_agent import CQLAgent
from cas4160.infrastructure.dqn_utils import (
    get_env_kwargs,
    PiecewiseSchedule,
    ConstantSchedule,
)


class Q_Trainer(object):

    def __init__(self, params):
        self.params = params

        train_args = {
            "num_agent_train_steps_per_iter": params["num_agent_train_steps_per_iter"],
            "num_critic_updates_per_agent_update": params[
                "num_critic_updates_per_agent_update"
            ],
            "train_batch_size": params["batch_size"],
            "double_q": params["double_q"],
        }

        env_args = get_env_kwargs(params["env_name"])

        self.agent_params = {**train_args, **env_args, **params}

        self.params["agent_class"] = CQLAgent
        self.params["agent_params"] = self.agent_params
        self.params["train_batch_size"] = params["batch_size"]
        self.params["env_wrappers"] = self.agent_params["env_wrappers"]

        self.rl_trainer = RL_Trainer(self.params)

    def run_training_loop(self):
        self.rl_trainer.run_training_loop(
            self.agent_params["num_timesteps"],
            collect_policy=self.rl_trainer.agent.actor,
            eval_policy=self.rl_trainer.agent.actor,
        )


def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env_name",
        default="PointmassHard-v0",
        choices=(
            "PointmassEasy-v0",
            "PointmassMedium-v0",
            "PointmassHard-v0",
            "PointmassVeryHard-v0",
        ),
    )

    parser.add_argument("--exp_name", type=str, default="todo")

    parser.add_argument("--eval_batch_size", type=int, default=1000)
    parser.add_argument("--batch_size", type=int, default=256)

    parser.add_argument("--dataset_size", type=int, default=20000)
    parser.add_argument("--dataset_name", type=str, default=None)
    parser.add_argument("--cql_alpha", type=float, default=0.0)

    parser.add_argument("--rew_shift", type=float, default=0.0)
    parser.add_argument("--rew_scale", type=float, default=1.0)

    parser.add_argument("--seed", type=int, default=2)
    parser.add_argument("--no_gpu", "-ngpu", action="store_true")
    parser.add_argument("--which_gpu", "-gpu_id", default=0)
    parser.add_argument("--scalar_log_freq", type=int, default=int(1e3))
    parser.add_argument("--save_params", action="store_true")

    args = parser.parse_args()

    # convert to dictionary
    params = vars(args)
    params["double_q"] = True
    params["num_agent_train_steps_per_iter"] = 1
    params["num_critic_updates_per_agent_update"] = 1
    params["exploit_weight_schedule"] = ConstantSchedule(1.0)
    params["video_log_freq"] = -1  # This param is not used for DQN
    params["num_timesteps"] = 50000
    params["learning_starts"] = 2000
    params["eps"] = 0.2
    ##################################
    ### CREATE DIRECTORY FOR LOGGING
    ##################################

    if params["env_name"] == "PointmassEasy-v0":
        params["ep_len"] = 50
    if params["env_name"] == "PointmassMedium-v0":
        params["ep_len"] = 150
    if params["env_name"] == "PointmassHard-v0":
        params["ep_len"] = 100
    if params["env_name"] == "PointmassVeryHard-v0":
        params["ep_len"] = 200

    logdir_prefix = "cql-rl_"
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../data")

    if not (os.path.exists(data_path)):
        os.makedirs(data_path, exist_ok=True)

    logdir = (
        logdir_prefix
        + args.exp_name
        + "_"
        + args.env_name
        + "_"
        + time.strftime("%d-%m-%Y_%H-%M-%S")
    )
    logdir = os.path.join(data_path, logdir)
    params["logdir"] = logdir
    if not (os.path.exists(logdir)):
        os.makedirs(logdir)

    print("\n\n\nLOGGING TO: ", logdir, "\n\n\n")

    trainer = Q_Trainer(params)
    trainer.run_training_loop()


if __name__ == "__main__":
    main()
