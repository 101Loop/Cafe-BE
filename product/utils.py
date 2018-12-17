def product_image_upload(instance, filename: str)->str:
    import datetime

    filename = filename.split('.')
    extension = filename.pop(-1)
    filename = '.'.join(filename)
    filename += "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    folder = str(instance.product.name).replace(' ', '_')
    filename = "product/{pid}_{fldr}/{fname}.{ext}".format(
        pid=instance.product.id, fldr=folder, fname=filename, ext=extension)
    return filename
