import json

from django.shortcuts import render
from django.http import JsonResponse

from static.utils import image_codecs, image_processor


def index(request):
    if request.method == "POST":
        JSONData = request.POST.get("data")

        imageData = json.loads(JSONData)["imageData"]
        blur_val = int(json.loads(JSONData)["blur"])
        gamma_val = float(json.loads(JSONData)["gamma"])
        hue_val = float(json.loads(JSONData)["hue"])
        saturate_val = float(json.loads(JSONData)["saturate"])
        vibrance_val = float(json.loads(JSONData)["vibrance"])
        sharpen_val = int(json.loads(JSONData)["sharpen"])

        print(gamma_val)

        header, image = image_codecs.decode_image(imageData)

        if blur_val != 0: image = image_processor.blur(image, blur_val)
        if gamma_val != 1: image = image_processor.adjust_gamma(image, gamma_val)
        if hue_val != 1: image = image_processor.adjust_hue(image, hue_val)
        if saturate_val != 1: image = image_processor.adjust_saturation(image, saturate_val)
        if vibrance_val != 1: image = image_processor.adjust_vibrance(image, vibrance_val)
        if sharpen_val != 1: image = image_processor.sharpen(image, sharpen_val)
        
        encoded_image = image_codecs.encode_image(header, image)

        return JsonResponse({
            "imageData" : encoded_image,
        })
        
    
    return render(request=request, template_name="imageprocessor/index.html", context={})