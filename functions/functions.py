from PIL import Image
import os
import time
import subprocess


def file_types_in_path(path):
    """
    :param path: path to directory to process; no default
    """
    ftypes = []
    for root, dirs, files in os.walk(path):
        for file in files:
            ext = file.split('.')[-1]
            if ext not in ftypes:
                ftypes.append(ext)
    return ftypes


def count_files_to_process(path, extension_in=None):
    """
    :param path: path to directory to process; no default
    :param extension_in: list of extensions to convert; other types will just be copied over; defaults to '.tif'
    :return: returns the number of items that will be processed
    """
    if extension_in is None:
        extension_in = ['.tif', '.tiff']  # default input extension
    i = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            in_ext = '.' + file.split('.')[-1]
            if in_ext in extension_in:
                i += 1
    return i


def convert_image_directory(path, extension_in=None, extension_out='.png', file_prefix='', file_suffix='out',
                            output_folder='./output/converted/', iter_timer=5):
    """
    :param path: path to directory to process; no default
    :param extension_in: list of extensions to convert; other types will just be copied over; defaults to '.tif'
    :param extension_out: image file type to convert into; defaults to '.png'
    :param file_prefix: custom prefix to add to each converted file; defaults to ''
    :param file_suffix: custom suffix to add to each converted file; defaults to 'out'
    :param output_folder: custom folder to add processed files to; defaults to './output/converted/'
    :param iter_timer: number of iterations to print a time stamp of progress; defaults to 5 iterations
    :return: does not return any value
    """
    if extension_in is None:
        extension_in = ['.tif', '.tiff']  # default input extension
    if file_prefix:
        if file_prefix[-1] != '_':
            file_prefix = file_prefix + '_'
    if file_suffix:
        if file_suffix[0] != '_':
            file_suffix = '_' + file_suffix
    if output_folder[-1] != '/':
        output_folder = output_folder + '/'  # unix
    extension_in = ['.' + x if x[0] != '.' else x for x in extension_in]
    if extension_out[0] != '.':
        extension_out = '.' + extension_out
    n_proc = count_files_to_process(path, extension_in)
    t_init = time.time()
    proc_count = 0
    for root, dirs, files in os.walk(path):
        for full_path in [root]:
            parent = (full_path + '/').replace('//', '/').replace('\\', '/')
            converted_path = output_folder[0:-1] + parent.replace(path, '')
            os.makedirs(converted_path, exist_ok=True)
            for file in files:
                path2file = parent + file
                in_ext = '.' + path2file.split('.')[-1]
                if in_ext in extension_in:
                    if proc_count % iter_timer == 0:  # time every n iterations
                        t_proc_start = time.time()
                        print(f"Processing file {proc_count} / {n_proc} ({round(100 * proc_count // n_proc, 2)}%)")
                    im = Image.open(path2file)
                    name = file.replace(in_ext, f'{in_ext}{file_suffix}{extension_out}')
                    rgb_im = im.convert('RGB')
                    rgb_im.save(converted_path + file_prefix + name)
                    if proc_count % iter_timer == 0:  # time every n iterations
                        t_proc_end = time.time()
                        elapsed = round(t_proc_end - t_init, 2)
                        print(f" {round(t_proc_end - t_proc_start, 2)}s (total: {round(elapsed / 60, 2)}m);    "
                              f"~{round((n_proc - proc_count) * (elapsed / (proc_count + 1)) / 60, 2)}"
                              f"m remaining")
                    proc_count += 1
                    pass
                else:
                    from_here = path2file
                    to_there = converted_path + file
                    r = subprocess.call(f'copy "{os.path.abspath(from_here)}" "{to_there}"', shell=True,
                                        stdout=open(os.devnull, 'wb'))
                    # r = subprocess.call(f'cp {from_here} {to_there}', stdout=open(os.devnull, 'wb'))  # unix
                    pass
