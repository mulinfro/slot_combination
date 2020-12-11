
import build_model

path = "古诗/poery_fast_nlu.txt"
model = build_model.Model(path)

model.generate_stages()
