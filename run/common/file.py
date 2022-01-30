import base64


def return_file_content_in_base64_format(image_file):
    with open(image_file, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    return im_b64
