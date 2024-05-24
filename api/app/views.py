from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response
import torch
from PIL import Image
from torchvision import transforms
from rest_framework.parsers import MultiPartParser


class TestView(APIView):

    def get(self, request, *args, **kwargs):

        hello_message_template = 'Hello, {}!'
        name = request.query_params.get('name', 'world')
        message = hello_message_template.format(name)

        return Response({'message': message})

class PredictDairyProductView(APIView):
    parser_classes = (MultiPartParser,)

    def __init__(self):
        super().__init__()
        self.model = torch.load('model.pth', map_location=torch.device('cpu'))
        self.model.eval()

    def post(self, request):
        
        image_url = request.FILES['image']

        if image_url is None:
            return Response({'error': 'Image URL is required'}, status=400)
        
        # Load image from URL
        image = Image.open(image_url)
        preprocess = transforms.Compose([
            transforms.Resize(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.554, 0.450, 0.343], std=[0.231, 0.241, 0.241]),
        ])

        image_tensor = preprocess(image)
        image_tensor = image_tensor.unsqueeze(0)

        # Make prediction
        with torch.no_grad():
            prediction = self.model(image_tensor)
            predicted_label = torch.argmax(prediction, dim=1).item()

        labels = ['butter', 'cheese', 'cottage cheese', 'cream', 'ice cream', 'kefir', 'milk', 'sourcream']

        return Response({'predicted_label': labels[predicted_label]})
