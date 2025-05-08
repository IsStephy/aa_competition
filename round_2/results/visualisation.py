import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from tqdm import tqdm
import shutil


def compute_score(a, b):
    if a == 1 and b == 1:
        return 3, 3
    elif a == 0 and b == 0:
        return 1, 1
    elif a == 1 and b == 0:
        return 0, 5
    else:
        return 5, 0


def create_tournament_video(history_file='round_history.csv', output='tournament_video.mp4'):
    df = pd.read_csv(history_file)
    scores = {}
    timeline = []

    # Build timeline using ONLY main scores
    for i, row in df.iterrows():
        main_id = row['main_id']
        opponent_id = row['opponent_id']
        main_move = row['main_move']
        opp_move = row['opponent_move']

        main_pts, _ = compute_score(main_move, opp_move)

        if main_id not in scores:
            scores[main_id] = 0
        scores[main_id] += main_pts

        # Ensure opponent has a zero score entry for consistent bars
        if opponent_id not in scores:
            scores[opponent_id] = 0

        timeline.append(scores.copy())  # snapshot after this round

    # Downsample to ~500 frames
    frame_step = max(1, len(timeline) // 500)
    timeline = timeline[::frame_step]

    fig, ax = plt.subplots(figsize=(10, 6))

    def animate(frame):
        ax.clear()
        current = timeline[frame]
        sorted_items = sorted(current.items(), key=lambda x: -x[1])
        ids = [str(k) for k, _ in sorted_items]
        vals = [v for _, v in sorted_items]
        ax.barh(ids, vals, color='skyblue')
        ax.set_xlim(0, max(vals) + 10)
        ax.set_xlabel('Main Score')
        ax.invert_yaxis()

    anim = animation.FuncAnimation(fig, animate, frames=len(timeline), interval=30)

    if output.endswith('.gif'):
        anim.save(output, writer='pillow')
    else:
        if shutil.which("ffmpeg"):
            # Progress-bar-enabled writer
            class TqdmWriter(animation.writers['ffmpeg']):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.pbar = tqdm(total=len(timeline), desc="Rendering video")

                def grab_frame(self, **kwargs):
                    self.pbar.update(1)
                    super().grab_frame(**kwargs)

                def finish(self):
                    self.pbar.close()
                    super().finish()

            writer = TqdmWriter(fps=60)
            anim.save(output, writer=writer)
        else:
            print("⚠️ FFmpeg not found. Saving as GIF using Pillow.")
            anim.save(output.replace(".mp4", ".gif"), writer='pillow')

    print(f"\n🎥 Video saved as {output}")
create_tournament_video()