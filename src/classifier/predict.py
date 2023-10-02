import torch
from src.classifier.classifier import greetClassifier
from src.model import greetattribute, greetfunction
from typing import Union
import numpy as np

class Predicter:

    def __init__(self):
        self.__classifier = greetClassifier

    def __preprocess_text(self, text: str):
        """
          Returns <class transformers.tokenization_utils_base.BatchEncoding> with the following fields:
          - input_ids: list of token ids
          - token_type_ids: list of token type ids
          - attention_mask: list of indices (0,1) specifying which tokens should considered by the model (return_attention_mask = True).
        """
        return self.__classifier.TOKENIZER.encode_plus(
            text,
            add_special_tokens=True,
            max_length=150,
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
    
    def predict(self, entity: Union[greetfunction.GreetFunction, greetattribute.GreetAttribute]):
      """
        Predicts the class label for the given entity.
        
        Args:
          entity (AbstractGreetEntity): The entity to classify.
        
        Returns:
          int: The predicted class label.
      """
      encoding = self.__preprocess_text(entity.getCode().strip())
      predict_ids = []
      predict_attention_mask = []
      # Extract IDs and Attention Mask
      predict_ids.append(encoding['input_ids'])
      predict_attention_mask.append(encoding['attention_mask'])
      predict_ids = torch.cat(predict_ids, dim=0)
      predict_attention_mask = torch.cat(predict_attention_mask, dim=0)
      with torch.no_grad():
          model = self.__classifier.get_model()
          output = model(predict_ids.to(self.__classifier.DEVICE), token_type_ids=None,
                                attention_mask=predict_attention_mask.to(self.__classifier.DEVICE))
          prediction = np.argmax(
              output.logits.cpu().numpy()).flatten().item()
      return prediction