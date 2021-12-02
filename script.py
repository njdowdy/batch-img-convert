from functions import functions as f

path = './input/test'
output_folder = './output/converted'

extension_in = ['tif']
extension_out = 'png'
file_suffix = ''
iter_timer = 1

if __name__ == "__main__":
    # entry point to the convert_image_directory function
    # f.file_types_in_path(path)  # gives an idea of what extensions are in your path to process
    f.convert_image_directory(path,
                              extension_in=extension_in,
                              extension_out=extension_out,
                              file_suffix=file_suffix,
                              output_folder=output_folder,
                              iter_timer=iter_timer)
