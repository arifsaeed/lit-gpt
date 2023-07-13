import sys
from pathlib import Path

# support running without installing as a package
wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))

from scripts.download import download_from_hub
from scripts.convert_hf_checkpoint import convert_hf_checkpoint

def init_model(model,checkpoint_dir):
    download_from_hub(model)
    convert_hf_checkpoint(checkpoint_dir)  