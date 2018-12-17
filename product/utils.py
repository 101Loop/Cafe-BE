def product_image_upload(instance, filename: str)->str:
    import datetime

    filename = filename.split('.')
    extension = filename.pop(-1)
    filename = '.'.join(filename)
    filename += f"_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    folder = str(instance.product.name).replace(' ', '_')
    filename = f"outlet/{instance.product.id}_{folder}/{filename}.{extension}"
    return filename
