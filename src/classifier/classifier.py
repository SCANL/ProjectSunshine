import torch
from tqdm import tqdm
import os
import requests
from transformers import RobertaTokenizer
from src.common.Singleton import Singleton
from src.common.error_handler import handle_error, ErrorSeverity


class Classifier(metaclass=Singleton):
    """
      Class for text classification using a pre-trained model.
      It utilizes the alBERTo model and the RobertaTokenizer.
    """

    __MODEL_URL = "https://huggingface.co/mantra-coding/alBERTo/resolve/main/greet-cli-model"
    TOKENIZER = RobertaTokenizer.from_pretrained(
        'microsoft/codebert-base', do_lower_case=True)
    DEVICE = torch.device('cpu')

    def __init__(self):
        """
          Constructor for the Classifier class.

          Args:
            config (Config, optional): Project configuration (to eventually specify a model version). Default: None.
        """

        model_path = os.path.join(os.path.expanduser("~"), ".greet", 'greet')
        if os.path.exists(model_path):
            self.__model = torch.load(model_path, map_location=self.DEVICE)
        else:
            try:
                os.mkdir(os.path.join(os.path.expanduser("~"), ".greet"))
            except OSError as error:
                print(error)
            self.__download_model(model_path)

    def get_model(self):
        return self.__model

    def set_model(self, value):
        self.__model = value

    def __download_model(self, model_path):
        """
        Download the model file if it doesn't exist.

        Args:
            model_path (str): Path to save the model file.
        """
        response = requests.get(self.__MODEL_URL, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            chunk_size = 1024
            mb_factor = 1024 * 1024  # Conversion factor from bytes to megabytes
            total_size_mb = total_size / mb_factor

            print("Model download progress:")
            with open(model_path, 'wb') as file, tqdm(
                desc=f"Downloading model ({total_size_mb:.2f} MB)",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress_bar.update(downloaded_size)
            print("Download complete!")
            self.__model = torch.load(model_path, map_location=self.DEVICE)
        else:
            handle_error("classifier.py", "Failed to download the model file.", ErrorSeverity.Critical, True)
