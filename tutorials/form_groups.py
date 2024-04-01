import argparse
import numpy as np
import pandas as pd


def form_groups(fp_registration: str, num_per_group: int = 5) -> None:
    registration_info = pd.read_csv(fp_registration)

    lisa_exp = registration_info["Rate your experience with LISA Data Analysis."]
    python_exp = registration_info["Rate you experience with Python."]
    group_work = registration_info["Group work"]
    names = registration_info["Name"]

    info_for_groups = []
    for le, pe, gw, name in zip(lisa_exp, python_exp, group_work, names):
        # chosen not to participate in group work
        if gw.lower() != "yes":
            continue

        le = 0 if le == "Prefer not to say" else int(le)
        pe = 0 if pe == "Prefer not to answer." else int(pe)
        total_exp = le + pe
        info_for_groups.append([name, total_exp])

    df = pd.DataFrame(
        {
            "names": [tmp[0] for tmp in info_for_groups],
            "exp": [tmp[1] for tmp in info_for_groups],
        }
    )
    df = df.sort_values("exp")

    total_groups = (df.shape[0] // num_per_group) + 1

    groups = []
    group_i = 0
    for i in range(int(df.shape[0] / 2)):
        group_i = i % total_groups
        if len(groups) < total_groups:
            groups.append([])
        groups[group_i].append(df.iloc[i])
        groups[group_i].append(df.iloc[df.shape[0] - (i + 1)])

    # odd numbered
    if df.shape[0] % 2 == 1:
        group_i = (group_i + 1) % total_groups
        groups[group_i].append(df.iloc[i + 1])

    for i, group in enumerate(groups):
        tmp = pd.concat(group, axis=1).T
        tmp["group"] = np.full(tmp.shape[0], i + 1)
        groups[i] = tmp

    output = pd.concat(groups, axis=0)

    output.to_csv("groups_for_LATW.csv")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="form groups for LATW",
    )

    parser.add_argument("filename")  # positional argument

    args = parser.parse_args()

    form_groups(args.filename)
