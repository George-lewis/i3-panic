import logging
import os
import sys
from tempfile import gettempdir as tempdir

import crayons
from i3ipc import Connection

DATA_FILE = f"{tempdir()}/i3-panic"

logging.basicConfig(
    stream=sys.stdout, format="%(name)s!%(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger("i3-panic")
logger.setLevel(logging.INFO)

logger.info(crayons.white("WE'RE PANICKING"))


def main():
    i3 = Connection()

    if os.path.exists(DATA_FILE):
        logger.info(crayons.yellow("Found data file, restoring"))
        with open(DATA_FILE, "r") as file:
            windows = [
                tuple(int(x) for x in pair.split(","))
                for pair in file.read().split("\n")
                if pair
            ]
        os.remove(DATA_FILE)
        for window in windows:
            logger.info(
                crayons.green(
                    f"Moving window with id {window[0]} to workspace `{window[1]}`"
                )
            )
            i3.command(f"[con_id={window[0]}] move to workspace {window[1]}")
    else:
        logger.info(crayons.yellow("Data file not present, PANICKING"))
        workspaces = [ws.num for ws in i3.get_workspaces() if ws.visible]
        logger.info(
            crayons.red(
                f"Workspaces {','.join([f'`{ws}`' for ws in workspaces])} are visible"
                if len(workspaces) > 1
                else f"Workspace `{workspaces[0]}` is visible"
            )
        )
        for i in range(10):
            if (i + 1) not in workspaces:
                free_workspace = i + 1
                break
        windows = []
        for ws in i3.get_tree().workspaces():
            if int(ws.name) in workspaces:
                for window in ws.leaves():
                    logger.info(
                        crayons.green(
                            f"Moving window [{window.window_class} - '{window.window_title}'] to workspace `{free_workspace}`"
                        )
                    )
                    windows.append((str(window.id), ws.name))
                    window.command(
                        f"floating enable, move container to workspace {free_workspace}"
                    )
        with open(DATA_FILE, "w") as file:
            for window in windows:
                file.write(f"{window[0]},{window[1]}\n")


if __name__ == "__main__":
    main()
else:
    logger.warning(crayons.yellow("NOT RUNNING AS __main__"))
