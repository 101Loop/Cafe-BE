def outlet_image_upload(instance, filename: str)->str:
    import datetime

    filename = filename.split('.')
    extension = filename.pop(-1)
    filename = '.'.join(filename)
    filename += "_" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    folder = str(instance.outlet.name).replace(' ', '_')
    filename = "outlet/{oid}_{fldr}/{fname}.{ext}".format(
        oid=instance.outlet.id, fldr=folder, fname=filename, ext=extension)
    return filename
