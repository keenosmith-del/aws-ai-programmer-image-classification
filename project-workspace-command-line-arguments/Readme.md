# Excercise files: 

Open the below files to continue with this excercise: 

- [get_input_args.py](../data/get_input_args.py)

## Help and argument validation

From the repository root, show available options without installing inference
packages or downloading model weights:

```sh
python3 data/check_images.py --help
```

Arguments are parsed before the inference module is imported, so help exits
successfully and malformed options return argparse's usage error. Normal image
classification still requires Pillow, PyTorch, torchvision and pretrained model
weights; this change does not alter inference or model selection.

Run the standard-library regression suite from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

CLI tests run with site-packages disabled and a temporary working directory to
prove help and argument errors do not depend on ML packages or local images.
The suite also covers result-statistics edge cases. The read-only test workflow
runs it on Python 3.12 and 3.15 without installing inference packages.

